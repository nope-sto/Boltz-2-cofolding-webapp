# 🧬 Boltz (v2.2.0) Webapp – Flask Interface for Protein, DNA, RNA, and SMILES Prediction

A web-based Flask application for submitting biomolecular sequences (proteins, DNA, RNA, or SMILES), validating inputs, generating FASTA files, and running **Boltz** predictions with real-time status tracking and downloadable results.

---

## 🚀 Features

- ✅ Sequence validation for **protein, DNA, RNA, and SMILES** inputs  
- ⚙️ Automatic FASTA file generation  
- 🧠 Runs **Boltz** prediction via command line (`boltz predict`)  
- 🧾 Real-time prediction status updates via Flask endpoints  
- 💾 Download results as `.cif`, `.zip`, or `.log` files  
- 🧩 Multi-sequence input support (chain A–Z)  
- 🧠 Optional physical potential usage (`--use_potentials`)  
- 🖥️ GPU detection and error handling for NVIDIA/CUDA setup  
- 🔒 Thread-safe job queue and per-job logging  

---

## 🧱 Project Structure

```
project/
│
├── app.py                    # Main Flask web application
├── templates/
│   └── index.html            # Frontend template for sequence input
├── inputs/                   # FASTA files generated from form input
├── outputs/                  # Prediction output folders
│   ├── output_<timestamp>/
│   │   ├── boltz_job_<timestamp>.log
│   │   └── boltz_results_input_<timestamp>/
│   │       └── predictions/
│   │           └── input_<timestamp>_model_0.cif

```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/boltz-webapp.git
cd boltz-webapp
```

### 2️⃣ Create a Virtual Conda Environment

```bash
conda create - n boltz-webapp
conda activate boltz-webapp
```

### 3️⃣ Install Dependencies
Start by installing the desired version of Boltz-2 according to their GitHub description (https://github.com/jwohlwend/boltz).
Afterwards install remaining dependencies if needed.

---

## 🧬 GPU Requirements

This application requires GPU access for `boltz predict` to run efficiently.  
To verify your setup:

```bash
nvidia-smi
```

If this fails, install NVIDIA drivers and CUDA toolkit.

---

## 🖥️ Running the WebApp (preferably in a screen session)

```bash
screen -S boltz-webapp-screen
```

```bash
conda activate boltz-webapp
```

```bash
python app.py
```

The app will start at:

```
http://0.0.0.0:8009
```

or locally at:

```
http://localhost:8009
```

---

## 🌐 API Endpoints

### `/`  
**Method:** `GET`  
Renders the input form (`index.html`).

---

### `/submit`  
**Method:** `POST`  
Starts a new Boltz prediction job.

#### Form Parameters:
| Parameter | Type | Description |
|------------|------|-------------|
| `primary_sequence` | `string` | Main biomolecule sequence |
| `primary_type` | `string` | Type: `protein`, `dna`, `rna`, or `smiles` |
| `use_physical_potentials` | `bool` | Optional checkbox |
| `additional_input[]` | `string[]` | Additional sequences |
| `input_type[]` | `string[]` | Matching types for each additional input |

#### Example Response:
```json
{
  "status": "Prediction started",
  "timestamp": 1731339164
}
```

---

### `/status/<timestamp>`  
**Method:** `GET`  
Returns prediction progress and messages from the internal status queue.

#### Example Response:
```json
{
  "status": [
    "Initializing prediction...",
    "Running multiple sequence alignment (MSA)...",
    "Running Boltz inference...",
    "Prediction completed successfully!",
    "download_ready:1731339164"
  ]
}
```

---

### `/download_cif/<timestamp>`  
**Method:** `GET`  
Downloads the `.cif` structure file produced by Boltz.

---

### `/download_zip/<timestamp>`  
**Method:** `GET`  
Downloads all output files as a ZIP archive.

---

### `/download_log/<timestamp>`  
**Method:** `GET`  
Downloads the job-specific log file.

---

### `/structures/<timestamp>.cif`  
**Method:** `GET`  
Serves `.cif` file directly for browser visualization.

---

## 🧩 Sequence Validation Rules

| Entity Type | Valid Characters |
|--------------|------------------|
| **Protein** | `A C D E F G H I K L M N P Q R S T V W Y` |
| **DNA** | `A T C G` |
| **RNA** | `A U C G` |
| **SMILES** | `C N O H S P F e Z n Ca Mg cnospi@[]\/()+-=#%:1234567890l` |

Invalid inputs are rejected with detailed error messages in the JSON response.

---

## 🧾 Logging

All logs are timestamped and stored in:
```
outputs/output_<timestamp>/boltz_job_<timestamp>.log
```

The main app log:
```
boltz_app.log
```

---

## 🧠 Example Workflow

1. Launch the app: `python app.py`  
2. Open the web interface in your browser  
3. Paste your primary protein/DNA/RNA/SMILES sequence  
4. (Optional) Add more sequences  
5. Click **Submit**  
6. Monitor progress via `/status/<timestamp>`  
7. Download results (`CIF`, `ZIP`, `LOG`) when ready  

---

## 🧩 Example Command (Internal)

The backend executes something similar to:
```bash
boltz predict input_1731339164.fasta --use_msa_server --out_dir outputs/output_1731339164
```
If the user checked *"Use physical potentials"*, the flag `--use_potentials` is appended.

---

## 🛡️ Error Handling

- GPU check failure → `Error: No GPU access detected. Ensure NVIDIA drivers and CUDA are installed.`
- Invalid characters → Descriptive validation error  
- Missing output/CIF/log → HTTP 404 with message  
- Subprocess timeout → `Error: Boltz process timed out`  

---

## 🔐 CORS Support

Cross-Origin Resource Sharing (CORS) is enabled via:
```python
from flask_cors import CORS
CORS(app)
```

This allows secure AJAX polling of job statuses from other domains.

---

## 🧑‍💻 Development Notes

- Written in **Python 3.8+**
- Uses **threading** for background prediction jobs
- Loggers are dynamically created per job
- Safe for concurrent predictions
- Suitable for deployment with **Gunicorn** or **uWSGI**

---

## 📜 License

This project is distributed under the MIT License.  
Feel free to modify and adapt it for your own workflow.


## 🧠 Citation

If you use complexes generated with this tool for publications, posters, or presentations, please cite the following publications and acknowledge Dr. Peter Stockinger for providing access to this web app.

Mirdita et al. (2022) ColabFold: Making protein folding accessible to all (https://www.nature.com/articles/s41592-022-01488-1)
 
Wohlwend et al. (2024). Boltz-1: Democratizing biomolecular interaction modeling (https://doi.org/10.1101/2024.11.19.624167)

Passaro et al. (2025) Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction (https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1)

### ✨ Author
**Peter Stockinger**  
🌐 LinkedIn: https://www.linkedin.com/in/peter-stockinger/
