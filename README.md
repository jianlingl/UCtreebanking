# Project Overview

This repository provides tools and resources for converting and unifying linguistic treebanks, with a specific focus on transforming **Universal Dependencies (UD)** structures into **Universal Constituency (UC)** representations and harmonizing existing constituency treebanks. Below are detailed descriptions of the components included in this repository:

## 1. Open Data
The `open_data` directory contains the UC-formatted files that we generated from the original UD treebanks. Due to data licensing restrictions, the unified versions of existing constituency treebanks are not included in this repository. For more details on accessing these resources, please refer to the documentation or contact us directly.

---

## 2. Universal Dependency Conversion
### **UD to UC Conversion**
- The script [`/UD2UC/UD2UC_convert.py`](UD2UC/UD2UC_convert.py) facilitates the conversion of UD treebanks into UC representations.
- It handles all necessary transformations and label mapping, making the process seamless and reproducible.

### **PTCB Treebank Reversion**
- The script [`/UD2UC/pctb_convert.py`](UD2UC/pctb_convert.py) enables the reversion of **PTCB** (Penn Chinese Treebank) files back into the UC format, allowing for bidirectional conversions between treebank representations.

---

## 3. Existing Treebanks Unification
The script [`/unify_exist/unify_label_tag.py`](unify_exist/unify_label_tag.py) is designed to unify the labels and tags of existing constituency treebanks. It harmonizes treebanks with diverse annotation styles into a consistent format, making them more compatible with universal standards.

---

## 4. Label Processing
All scripts include robust label processing capabilities. Users have the flexibility to:
- **Map existing labels** based on predefined mappings, or
- **Regenerate labels** using the **[Stanza](https://stanfordnlp.github.io/stanza/)** toolkit for greater precision and adaptability.

---

## How to Use
Please refer to the individual script documentation for detailed usage instructions. This repository is intended to support linguistic research, syntactic treebank development, and natural language processing applications.

---

## Contact
For any questions or additional details, feel free to raise an issue in this repository or contact me directly: jianlingl@tju.edu.cn.