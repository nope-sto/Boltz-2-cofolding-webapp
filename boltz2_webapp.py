from flask import Flask, request, render_template, jsonify, send_file, send_from_directory
import os
import subprocess
import threading
import time
from pathlib import Path
from queue import Queue
import zipfile
import io
import logging
from flask_cors import CORS

app = Flask(__name__)

# Directory for storing input and output files
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Queue to store Boltz status updates
status_queue = Queue()

def validate_sequence(data, entity_type, logger):
    """Validate input sequences based on entity type."""
    logger.debug(f"Validating {entity_type} sequence: {data[:50]}...")
    if not data.strip():
        logger.error(f"Empty sequence provided for {entity_type}")
        return False, "Empty sequence provided"
    if not data:
        logger.error("Input data is empty or None.")
        return False, "Invalid input: data is empty or None"

    clean_data = ''.join(c for c in data if not c.isspace())

    if entity_type == "protein":
        valid_chars = set("ACDEFGHIKLMNPQRSTVWY")
        invalid_chars = set(c for c in clean_data.upper() if c not in valid_chars)
        if invalid_chars:
            logger.error(f"Invalid characters in protein sequence: {data[:50]}... Unsupported: {''.join(sorted(invalid_chars))}")
            return False, f"Invalid protein sequence: contains unsupported characters: {''.join(sorted(invalid_chars))}"

    elif entity_type in ("dna", "rna"):
        valid_chars = set("ATCG" if entity_type == "dna" else "AUCG")
        invalid_chars = set(c for c in clean_data.upper() if c not in valid_chars)
        if invalid_chars:
            logger.error(f"Invalid characters in {entity_type} sequence: {data[:50]}... Unsupported: {''.join(sorted(invalid_chars))}")
            return False, f"Invalid {entity_type} sequence: contains unsupported characters: {''.join(sorted(invalid_chars))}"

    elif entity_type == "smiles":
        valid_chars = set("CNOHSPFeZnCaMgcnospi@[]\\/()+-=#%:1234567890l")
        invalid_chars = set(c for c in clean_data if c not in valid_chars)
        if invalid_chars:
            logger.error(f"Invalid SMILES string: {data[:50]}... Unsupported characters: {''.join(sorted(invalid_chars))}")
            return False, f"Invalid SMILES string: contains unsupported characters: {''.join(sorted(invalid_chars))}"

    else:
        logger.error(f"Unknown entity type: {entity_type}")
        return False, f"Unknown entity type: {entity_type}"
    return True, ""

def generate_fasta(sequences, output_path, logger):
    """
    Generate a FASTA file for Boltz.
    Format: >A|ENTITY_TYPE\nSEQUENCE
    """
    logger.debug(f"Generating FASTA file at {output_path}")
    chain_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if len(sequences) > len(chain_letters):
        logger.error(f"Too many sequences: {len(sequences)}. Max {len(chain_letters)} supported.")
        return False, "Too many sequences provided"
    
    try:
        with open(output_path, "w") as f:
            for i, seq in enumerate(sequences):
                chain_id = chain_letters[i]
                entity_type = seq["type"]
                sequence = seq["data"].strip()
                f.write(f">{chain_id}|{entity_type}\n{sequence}\n")
        
        with open(output_path, "r") as f:
            fasta_content = f.read()
        logger.debug(f"FASTA file content:\n{fasta_content}")
        return True, ""
    except Exception as e:
        logger.error(f"Failed to generate FASTA file: {str(e)}")
        return False, f"Failed to generate FASTA file: {str(e)}"

def check_gpu_access(logger):
    """Check if GPU is available."""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logger.debug(f"GPU access confirmed:\n{result.stdout}")
            return True
        else:
            logger.error(f"GPU access failed:\n{result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error checking GPU access: {str(e)}")
        return False

def run_boltz_prediction(fasta_path, output_dir, status_queue, timestamp, use_physical_potentials=False):
    """
    Run Boltz prediction and capture terminal output to a job-specific log.
    """
    job_log_file = output_dir / f"boltz_job_{timestamp}.log"
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.FileHandler(job_log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    logger.debug(f"Starting Boltz prediction with FASTA: {fasta_path}, output: {output_dir}, use_physical_potentials: {use_physical_potentials}")
    
    if not check_gpu_access(logger):
        error_msg = "Error: No GPU access detected. Ensure NVIDIA drivers and CUDA are installed."
        status_queue.put(error_msg)
        logger.error(error_msg)
        return
    
    cmd = [
        "boltz", "predict",
        str(fasta_path),
        "--use_msa_server",
        "--out_dir", str(output_dir)
    ]
    
    if use_physical_potentials:
        cmd.append("--use_potentials")
    
    logger.debug(f"Executing command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        status_queue.put("Starting Boltz prediction...")
        while process.poll() is None:
            stdout_line = process.stdout.readline().strip()
            stderr_line = process.stderr.readline().strip()
            if stdout_line:
                status_queue.put(stdout_line)
                logger.debug(f"Boltz stdout: {stdout_line}")
                if "generating MSA" in stdout_line.lower():
                    status_queue.put("Running multiple sequence alignment (MSA)...")
                elif "running inference" in stdout_line.lower():
                    status_queue.put("Running Boltz inference...")
                elif "completed" in stdout_line.lower():
                    status_queue.put("Prediction completed!")
            if stderr_line:
                if any(keyword in stderr_line.lower() for keyword in ["msa server", "error", "failed", "exception"]):
                    status_queue.put(f"Error: {stderr_line}")
                    logger.error(f"Boltz stderr: {stderr_line}")
                else:
                    status_queue.put(f"Info: {stderr_line}")
                    logger.info(f"Boltz info: {stderr_line}")
            time.sleep(0.1)
        
        stdout, stderr = process.communicate(timeout=300)
        if stdout:
            for line in stdout.splitlines():
                line = line.strip()
                if line:
                    status_queue.put(line)
                    logger.debug(f"Boltz stdout (post): {line}")
        if stderr:
            for line in stderr.splitlines():
                line = line.strip()
                if line:
                    if any(keyword in line.lower() for keyword in ["msa server", "error", "failed", "exception"]):
                        status_queue.put(f"Error: {line}")
                        logger.error(f"Boltz info (post): {line}")
                    else:
                        status_queue.put(f"Info: {line}")
                        logger.info(f"Boltz info (post): {line}")
        
        cif_file = output_dir / f"boltz_results_input_{fasta_path.stem}/predictions/input_{fasta_path.stem}/input_{fasta_path.stem}_model_0.cif"
        if process.returncode == 0:
            for _ in range(300):
                if cif_file.exists():
                    status_queue.put("Prediction finished successfully. CIF file created.")
                    logger.info(f"Boltz prediction completed successfully, CIF file: {cif_file}")
                    break
                time.sleep(0.1)
            else:
                status_queue.put("Prediction finished, but CIF file not found.")
                logger.warning(f"Boltz prediction completed, but CIF file missing: {cif_file}")
        else:
            status_queue.put(f"Error: Prediction failed with return code {process.returncode}")
            logger.error(f"Boltz prediction failed with return code {process.returncode}")
    except subprocess.TimeoutExpired:
        status_queue.put("Error: Boltz process timed out")
        logger.error("Bolz process timed out")
        process.kill()
    except Exception as e:
        error_msg = f"Error: Unexpected error running Boltz: {str(e)}"
        status_queue.put(error_msg)
        logger.exception(error_msg)

@app.route('/')
def index():
    """Render the input form."""
    logger = logging.getLogger('boltz_app')
    if not logger.handlers:
        handler = logging.FileHandler('boltz_app.log')
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    logger.debug("Rendering index.html")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission, generate FASTA, and run Boltz."""
    timestamp = int(time.time())
    output_dir = OUTPUT_DIR / f"output_{timestamp}"
    try:
        output_dir.mkdir(exist_ok=True)
    except Exception as e:
        error_msg = f"Failed to create output directory: {str(e)}"
        logger = logging.getLogger('boltz_app')
        if not logger.handlers:
            handler = logging.FileHandler('boltz_app.log')
            handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
            logger.addHandler(handler)
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500
    
    job_log_file = output_dir / f"boltz_job_{timestamp}.log"
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    if not logger.handlers:
        handler = logging.FileHandler(job_log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    logger.debug("Received form submission")
    sequences = []
    primary_sequence = request.form.get('primary_sequence')
    primary_type = request.form.get('primary_type')
    use_physical_potentials = request.form.get('use_physical_potentials') == 'on'  # Checkbox value
    
    if not primary_sequence or not primary_sequence.strip():
        error_msg = "At least one non-empty sequence is required"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 400
    is_valid, error_msg = validate_sequence(primary_sequence, primary_type, logger)
    if not is_valid:
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 400
    
    sequences.append({"type": primary_type, "data": primary_sequence})
    
    additional_inputs = request.form.getlist('additional_input[]')
    input_types = request.form.getlist('input_type[]')
    
    for data, input_type in zip(additional_inputs, input_types):
        if data and data.strip():
            is_valid, error_msg = validate_sequence(data, input_type, logger)
            if not is_valid:
                logger.error(error_msg)
                return jsonify({"error": error_msg}), 400
            sequences.append({"type": input_type, "data": data})
    
    fasta_path = INPUT_DIR / f"input_{timestamp}.fasta"
    try:
        success, error_msg = generate_fasta(sequences, fasta_path, logger)
        if not success:
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 500
    except Exception as e:
        error_msg = f"Unexpected error generating FASTA file: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500
    
    status_queue.put("Initializing prediction...")
    try:
        threading.Thread(
            target=run_boltz_prediction,
            args=(fasta_path, output_dir, status_queue, timestamp, use_physical_potentials),  # Pass checkbox value
            daemon=True
        ).start()
    except Exception as e:
        error_msg = f"Failed to start prediction thread: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500
    
    logger.info(f"Prediction started for timestamp {timestamp}")
    return jsonify({"status": "Prediction started", "timestamp": timestamp})

@app.route('/status/<timestamp>')
def status(timestamp):
    """Return the latest status updates and check for CIF file."""
    output_dir = OUTPUT_DIR / f"output_{timestamp}"
    cif_file = output_dir / f"boltz_results_input_{timestamp}/predictions/input_{timestamp}/input_{timestamp}_model_0.cif"
    
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    if not logger.handlers:
        handler = logging.FileHandler(output_dir / f"boltz_job_{timestamp}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    status_messages = []
    while not status_queue.empty():
        status_messages.append(status_queue.get())
    
    if cif_file.exists():
        if not any(msg == "Prediction completed successfully!" for msg in status_messages):
            status_messages.append("Prediction completed successfully!")
        if not any(msg == f"download_ready:{timestamp}" for msg in status_messages):
            status_messages.append(f"download_ready:{timestamp}")
        logger.info(f"CIF file found for timestamp {timestamp}: {cif_file}")
    elif not status_messages:
        status_messages.append("Prediction in progress...")
    
    logger.debug(f"Status requested for timestamp {timestamp}: {status_messages}")
    return jsonify({"status": status_messages})

@app.route('/download_cif/<timestamp>')
def download_cif(timestamp):
    """Serve the CIF file."""
    output_dir = OUTPUT_DIR / f"output_{timestamp}"
    cif_file = output_dir / f"boltz_results_input_{timestamp}/predictions/input_{timestamp}/input_{timestamp}_model_0.cif"
    
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    if not logger.handlers:
        handler = logging.FileHandler(output_dir / f"boltz_job_{timestamp}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    logger.debug(f"CIF download requested for timestamp {timestamp}")
    if not output_dir.exists():
        error_msg = "Output directory not found"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 404
    
    if not cif_file.exists():
        error_msg = "CIF file not found. Prediction may not have completed."
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 404
    
    logger.info(f"Serving CIF file for timestamp {timestamp}")
    return send_file(
        cif_file,
        mimetype="chemical/x-cif",
        as_attachment=True,
        download_name=f"input_{timestamp}_model_0.cif"
    )

@app.route('/download_zip/<timestamp>')
def download_zip(timestamp):
    """Serve a zipped file containing all files in the output directory."""
    output_dir = OUTPUT_DIR / f"output_{timestamp}"
    
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    if not logger.handlers:
        handler = logging.FileHandler(output_dir / f"boltz_job_{timestamp}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    logger.debug(f"ZIP download requested for timestamp {timestamp}")
    if not output_dir.exists():
        error_msg = "Output directory not found"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 404
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(output_dir)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    logger.info(f"Serving ZIP file for timestamp {timestamp}")
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"boltz_output_{timestamp}.zip"
    )

@app.route('/download_log/<timestamp>')
def download_log(timestamp):
    """Serve the log file."""
    output_dir = OUTPUT_DIR / f"output_{timestamp}"
    log_file = output_dir / f"boltz_job_{timestamp}.log"
    
    logger = logging.getLogger(f"boltz_job_{timestamp}")
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logger.addHandler(handler)
    
    logger.debug(f"Log download requested for timestamp {timestamp}")
    if not output_dir.exists():
        error_msg = "Output directory not found"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 404
    
    if not log_file.exists():
        error_msg = "Log file not found."
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 404
    
    logger.info(f"Serving log file for timestamp {timestamp}")
    return send_file(
        log_file,
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"boltz_job_{timestamp}.log"
    )

@app.route('/structures/<timestamp>.cif')
def serve_cif_file(timestamp):
    subfolder = f"output_{timestamp}/boltz_results_input_{timestamp}/predictions/input_{timestamp}"
    filename = f"input_{timestamp}_model_0.cif"
    return send_from_directory(OUTPUT_DIR / subfolder, filename, mimetype='chemical/x-cif')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009, debug=False)
    CORS(app)