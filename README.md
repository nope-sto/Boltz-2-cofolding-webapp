# 🧩 Markdown Code Formatting Guide

This guide shows how to write and render code or bash commands properly in **Markdown** using backticks (`).

---

## 🧩 Inline Code

Use **one backtick** on each side of your code snippet:

```markdown
Use `python script.py` to run the program.
```

**Rendered result:**  
> Use `python script.py` to run the program.

---

## 💻 Multiline Code Blocks

Use **three backticks** (```) before and after your code block.

### Example:

```bash
# This is a bash command
cd /path/to/project
python main.py
```

**Rendered result:**

```bash
# This is a bash command
cd /path/to/project
python main.py
```

---

## 📜 Specifying a Language

After the opening backticks, you can add a language name for syntax highlighting:

- `bash` → for shell commands  
- `python` → for Python code  
- `html`, `javascript`, `json`, etc.

### Example for Python

```python
def greet(name):
    print(f"Hello, {name}!")
```

**Rendered result:**

```python
def greet(name):
    print(f"Hello, {name}!")
```

---

## ✅ Quick Reference

| Purpose | Markdown | Result |
|----------|-----------|---------|
| Inline code | \`code\` | `code` |
| Code block | \`\`\`bash ... \`\`\` | ```bash echo "Hello" ``` |
| Python block | \`\`\`python ... \`\`\` | ```python print("Hello") ``` |

---

### 📘 Notes

- You can use any language keyword (e.g., `json`, `cpp`, `html`, etc.) for syntax highlighting.
- Backticks must be straight (`), not curly (‘ or ’).
- To display triple backticks *inside* a Markdown document, use a `<pre>` block or escape them.

---

**Created by:** GPT‑5  
**File:** markdown_code_reference.md  
