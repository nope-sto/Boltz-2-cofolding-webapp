# ⚛️ Boltz (v2.2.0) Webapp

A modern web interface for **biomolecular complex prediction** — supporting **Protein**, **DNA**, **RNA**, and **Small Molecules (SMILES)**.

---

## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/boltz-webapp.git
cd boltz-webapp
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend Flask server:

```bash
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🧬 Frontend Overview

The frontend is built using **HTML5**, **Tailwind CSS**, and **jQuery**.

### Features

- Dynamic form handling for primary and additional biomolecular inputs  
- Live status updates during prediction runs  
- Download links for CIF, ZIP, and Log files  
- Clean responsive design with Tailwind styling  

### Example Snippet

```html
<select name="primary_type" required class="w-full p-3 border border-gray-200 rounded-lg">
  <option value="protein">Protein Sequence</option>
  <option value="dna">DNA Sequence</option>
  <option value="rna">RNA Sequence</option>
  <option value="smiles">SMILES String</option>
</select>
```

You can dynamically add new input fields using:

```javascript
$('#add-input').click(function() {
  const newInput = `
    <div class="input-group flex flex-col md:flex-row md:items-start gap-3 mt-2">
      <select name="input_type[]" class="w-full md:w-1/3 p-3 border border-gray-200 rounded-lg">
        <option value="protein">Protein Sequence</option>
        <option value="dna">DNA Sequence</option>
        <option value="rna">RNA Sequence</option>
        <option value="smiles">SMILES String</option>
      </select>
      <textarea name="additional_input[]" rows="3" class="w-full p-3 border border-gray-200 rounded-lg"></textarea>
      <button type="button" class="remove-input bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700">Remove</button>
    </div>`;
  $('#additional-inputs').append(newInput);
});
```

---

## ⚙️ Backend API

### `POST /submit`  
Submits the user-provided sequences to the prediction engine.

**Payload Example:**

```bash
primary_type=protein
primary_sequence=MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGP
additional_input[]=ATGCCTGAAGTGA
input_type[]=dna
use_physical_potentials=true
```

**Response Example:**
```json
{
  "timestamp": "20251111-153210",
  "message": "Job submitted successfully."
}
```

---

### `GET /status/<timestamp>`  
Polls the server for prediction progress.

**Response Example:**
```json
{
  "status": [
    "Info: Starting prediction pipeline",
    "Model running...",
    "CIF file created successfully."
  ]
}
```

---

### `GET /download_zip/<timestamp>`  
Downloads all generated output files as a ZIP archive.

---

## 🧠 Key UI Features

- ✅ Add or remove multiple input types dynamically  
- ✅ Use optional physical potentials toggle  
- ✅ Real-time job status updates with auto-refresh every 2 seconds  
- ✅ Download CIF, ZIP, and log files when jobs complete  
- ✅ Error and info messages displayed inline with colors  

---

## 🧩 Technologies Used

| Layer | Technology |
|-------|-------------|
| Frontend | HTML5, Tailwind CSS, jQuery |
| Backend | Flask (Python) |
| Data Handling | JSON, AJAX |
| Output | CIF, ZIP, Log Files |

---

## 📘 Citation & Acknowledgments

If you use **Boltz Webapp** results for publications, please cite:

- Mirdita *et al.* (2022). *ColabFold: Making protein folding accessible to all*. [Nature Methods](https://www.nature.com/articles/s41592-022-01488-1)  
- Wohlwend *et al.* (2024). *Boltz‑1: Democratizing biomolecular interaction modeling*. [bioRxiv](https://doi.org/10.1101/2024.11.19.624167)  
- Passaro *et al.* (2025). *Boltz‑2: Towards Accurate and Efficient Binding Affinity Prediction*. [bioRxiv](https://doi.org/10.1101/2025.03.12.624167)

---

## 🧑‍💻 Author

**Dr. Peter Stockinger**  
LinkedIn: [linkedin.com/in/peter-stockinger](https://www.linkedin.com/in/peter-stockinger/)  

© 2025 Boltz Webapp  
