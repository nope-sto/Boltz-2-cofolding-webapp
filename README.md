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

