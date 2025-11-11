# 🧬 Boltz (v2.2.0) WebApp

A complete Flask-based web application for **biomolecular complex prediction** using the **Boltz** modeling framework.  
It provides a modern, TailwindCSS-powered user interface for submitting **protein**, **DNA**, **RNA**, or **SMILES** sequences, validates the input, generates FASTA files, and runs `boltz predict` in the background with real-time status tracking and downloadable results.

---

## ✨ Overview

**Boltz WebApp (v2.2.0)** is designed to make biomolecular structure prediction simple and interactive.  
It supports:
- 🧩 Multi-chain and hybrid inputs (protein–DNA, protein–RNA, protein–ligand)
- ✅ Sequence validation for different molecule types
- ⚙️ Automated FASTA file generation
- 🧠 GPU-enabled Boltz predictions (`boltz predict`)
- 📡 Real-time status polling (via `/status/<timestamp>`)
- 💾 Download options for `.cif`, `.zip`, and `.log` files
- 🧾 Clean and responsive **Tailwind UI**
- 🔒 Background job threading and per-run logging

---

## 🧱 Project Structure
boltz-webapp/
│
├── app.py # Flask backend
├── templates/
│ └── index.html # Frontend (TailwindCSS + jQuery)
├── inputs/ # Auto-generated FASTA files
├── outputs/ # Prediction results
│ ├── output_<timestamp>/
│ │ ├── boltz_job_<timestamp>.log
│ │ └── boltz_results_input_<timestamp>/
│ │ └── predictions/input_<timestamp>_model_0.cif
└── requirements.txt


---

## 🧩 Frontend Design

The frontend is written in **HTML + TailwindCSS + jQuery** and uses a **clean, card-based layout** optimized for clarity and responsiveness.

### 💡 Key UI Components

- **Primary Sequence Input:**  
  Choose entity type (`protein`, `dna`, `rna`, `smiles`) and paste sequence.  
- **Additional Inputs:**  
  Dynamically add or remove extra chains/components (A–Z).  
- **“Use Physical Potentials” Checkbox:**  
  Adds the `--use_potentials` flag for Boltz inference.  
- **Status Window:**  
  Displays live progress updates fetched via AJAX polling.  
- **Download Section:**  
  Provides links for `.cif`, `.zip`, and `.log` once prediction finishes.

### 🎨 Styling Highlights

- Framework: **TailwindCSS** via CDN  
- Font: `Inter` (system fallback: Helvetica, Arial)  
- Button Gradients:  
  - `.btn-primary`: teal gradient (Boltz branding)  
  - `.btn-secondary`: indigo gradient for downloads  
- Focus styling for all inputs, checkboxes, and buttons  
- Subtle container shadows (`.container-shadow`)  
- Color-coded status messages:
  - `.error` → red (`#E53E3E`)
  - `.success` → green-teal (`#234E52`)
  - `.info` → indigo (`#5A67D8`)

---

## 🧠 Backend Logic (Flask)

The backend serves routes for user interaction, file generation, Boltz execution, and status updates.

| Route | Method | Description |
|--------|---------|-------------|
| `/` | GET | Render the HTML front page |
| `/submit` | POST | Validate sequences, generate FASTA, and start a Boltz job |
| `/status/<timestamp>` | GET | Fetch live status updates |
| `/download_cif/<timestamp>` | GET | Download CIF file |
| `/download_zip/<timestamp>` | GET | Download all results as ZIP |
| `/download_log/<timestamp>` | GET | Download log file |
| `/structures/<timestamp>.cif` | GET | Serve CIF for 3D viewer integration |

---

## 🧪 Sequence Validation

Input sequences are validated according to entity type:

| Entity Type | Allowed Characters |
|--------------|--------------------|
| **Protein** | `A C D E F G H I K L M N P Q R S T V W Y` |
| **DNA** | `A T C G` |
| **RNA** | `A U C G` |
| **SMILES** | `C N O H S P F e Z n C a M g c n o s p i @ [ ] \ / ( ) + - = # % : 1-9 l` |

Invalid or empty sequences trigger descriptive error messages.

---

## 🧰 Installation


---

## 🧩 Frontend Design

The frontend is written in **HTML + TailwindCSS + jQuery** and uses a **clean, card-based layout** optimized for clarity and responsiveness.

### 💡 Key UI Components

- **Primary Sequence Input:**  
  Choose entity type (`protein`, `dna`, `rna`, `smiles`) and paste sequence.  
- **Additional Inputs:**  
  Dynamically add or remove extra chains/components (A–Z).  
- **“Use Physical Potentials” Checkbox:**  
  Adds the `--use_potentials` flag for Boltz inference.  
- **Status Window:**  
  Displays live progress updates fetched via AJAX polling.  
- **Download Section:**  
  Provides links for `.cif`, `.zip`, and `.log` once prediction finishes.

### 🎨 Styling Highlights

- Framework: **TailwindCSS** via CDN  
- Font: `Inter` (system fallback: Helvetica, Arial)  
- Button Gradients:  
  - `.btn-primary`: teal gradient (Boltz branding)  
  - `.btn-secondary`: indigo gradient for downloads  
- Focus styling for all inputs, checkboxes, and buttons  
- Subtle container shadows (`.container-shadow`)  
- Color-coded status messages:
  - `.error` → red (`#E53E3E`)
  - `.success` → green-teal (`#234E52`)
  - `.info` → indigo (`#5A67D8`)

---

## 🧠 Backend Logic (Flask)

The backend serves routes for user interaction, file generation, Boltz execution, and status updates.

| Route | Method | Description |
|--------|---------|-------------|
| `/` | GET | Render the HTML front page |
| `/submit` | POST | Validate sequences, generate FASTA, and start a Boltz job |
| `/status/<timestamp>` | GET | Fetch live status updates |
| `/download_cif/<timestamp>` | GET | Download CIF file |
| `/download_zip/<timestamp>` | GET | Download all results as ZIP |
| `/download_log/<timestamp>` | GET | Download log file |
| `/structures/<timestamp>.cif` | GET | Serve CIF for 3D viewer integration |

---

## 🧪 Sequence Validation

Input sequences are validated according to entity type:

| Entity Type | Allowed Characters |
|--------------|--------------------|
| **Protein** | `A C D E F G H I K L M N P Q R S T V W Y` |
| **DNA** | `A T C G` |
| **RNA** | `A U C G` |
| **SMILES** | `C N O H S P F e Z n C a M g c n o s p i @ [ ] \ / ( ) + - = # % : 1-9 l` |

Invalid or empty sequences trigger descriptive error messages.

---

## 🧰 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/boltz-webapp.git
cd boltz-webapp

```bash
git clone https://github.com/yourusername/boltz-webapp.git
cd boltz-webapp

### 2️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt
Example requirements.txt:
flask
flask-cors

### 4️⃣ Install Boltz
Please follow the installation guide from the Boltz GitHub repository (https://github.com/jwohlwend/boltz).

🖥️ Running the App
python app.py
The application runs by default at:
http://localhost:8009
⚡ Prediction Flow
User submits form from web UI.
Flask validates sequences and creates a F+
ASTA file under /inputs/.
A background thread runs:
boltz predict <fasta> --use_msa_server --out_dir outputs/output_<timestamp> [--use_potentials]
Progress is logged and streamed to /status/<timestamp>.
Once complete, /download_* endpoints allow users to retrieve results.
🧾 Logging and Output
Application Log: boltz_app.log
Job Logs: outputs/output_<timestamp>/boltz_job_<timestamp>.log
Output Models:
outputs/output_<timestamp>/boltz_results_input_<timestamp>/predictions/input_<timestamp>_model_0.cif
🧬 GPU Requirements
The app automatically checks for GPU availability using:
`nvidia-smi!
If unavailable, an error will be logged and returned via /status/<timestamp>:
Error: No GPU access detected. Ensure NVIDIA drivers and CUDA are installed.
### 🧩 Example Workflow
Open the webapp.
Select Protein Sequence and paste your sequence.
Add optional DNA/RNA/SMILES chains.
Check “Use Physical Potentials” (optional).
Click Run Prediction.
Watch progress in the Status section.
When complete, download the .cif, .zip, or .log files.
### 🧠 Frontend Technology Summary
Technology	Purpose
HTML5	UI structure
TailwindCSS	Styling framework
jQuery 3.6	AJAX polling and dynamic DOM manipulation
Flask Jinja2	Template rendering
CORS	Enables cross-origin requests for AJAX updates
🧩 Example Screenshots
(Add screenshots of your app interface here if available.)
### 📚 Citations
If you use results generated from this tool, please cite:
Mirdita et al. (2022). ColabFold: Making protein folding accessible to all. Nature Methods
Wohlwend et al. (2024). Boltz-1: Democratizing biomolecular interaction modeling. bioRxiv
Passaro et al. (2025). Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction. bioRxiv
Please also acknowledge Dr. Peter Stockinger for providing access to this web application.
### 📜 License
Distributed under the MIT License.
You are free to modify, reuse, or integrate it into your own workflow.
### 👨‍💻 Author
Dr. Peter Stockinger
🔗 LinkedIn Profile
