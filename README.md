# Hale-Hosa Kannada RAG

A **Retrieval-Augmented Generation (RAG)** system for translating and modernizing **Hale Kannada (Old Kannada)** into **Hosa Kannada (Modern Kannada)**.

The system uses **ChromaDB** as a vector database to retrieve relevant Hale Kannada → Hosa Kannada examples from a cleaned parallel dataset. These retrieved examples are then provided as context to an **LLM**, which generates the final Hosa Kannada translation.

---

## 📌 Project Overview

Hale Kannada contains historical vocabulary, grammatical forms, and expressions that may not be well understood by modern language models.

A normal LLM may produce incorrect translations when it encounters rare or archaic forms.

This project addresses this problem using **Retrieval-Augmented Generation**.

Instead of asking the LLM to translate only from its pretrained knowledge, the system first searches a domain-specific knowledge base containing Hale Kannada → Hosa Kannada examples.

### Core Pipeline

```text
User
  ↓
Hale Kannada Input
  ↓
Vector / Database Search
  ↓
Relevant Hale → Hosa Examples
  ↓
LLM
  ↓
Hosa Kannada Output
```

---

## 🧠 How the RAG Pipeline Works

### Step 1 — User Input

The user enters a Hale Kannada word, sentence, or paragraph.

Example:

```text
ಅವಳ್ ಮನಂ
```

---

### Step 2 — Query Embedding

The input is converted into a vector representation using an embedding model.

```text
Hale Kannada Input
        ↓
Embedding Model
        ↓
Query Vector
```

The vector represents the semantic meaning of the input.

---

### Step 3 — Vector Database Search

The query vector is searched against the vectors stored in **ChromaDB**.

The database contains Hale Kannada → Hosa Kannada examples extracted from the cleaned dataset.

```text
                    ChromaDB
        ┌────────────────────────────┐
        │ Hale Kannada               │
        │ Hosa Kannada               │
        │ Embedding                  │
        │ Metadata                   │
        └────────────────────────────┘
                    ↑
                    │
              Similarity Search
                    │
               Query Vector
```

---

### Step 4 — Retrieve Relevant Examples

ChromaDB returns the most relevant examples.

For example:

```text
Hale Kannada: ಅವಳ್
Hosa Kannada: ಅವಳು

Hale Kannada: ಮನಂ
Hosa Kannada: ಮನಸ್ಸು
```

These retrieved examples are the **RAG context**.

They are stored in the vector database first and retrieved only when required by a query.

---

### Step 5 — Send Context to the LLM

The retrieved examples are combined with the user's input and provided to the LLM.

Conceptually:

```text
System Instruction:
Translate Hale Kannada into Hosa Kannada.

Retrieved Context:

Hale Kannada: ಅವಳ್
Hosa Kannada: ಅವಳು

Hale Kannada: ಮನಂ
Hosa Kannada: ಮನಸ್ಸು

User Input:

ಅವಳ್ ಮನಂ
```

The LLM uses the retrieved examples as additional knowledge when generating the translation.

---

### Step 6 — Hosa Kannada Output

The LLM generates the final modern Kannada translation.

```text
ಅವಳು ಮನಸ್ಸು
```

The exact output depends on the input and the retrieved context.

---

# 🏗️ System Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │  Hale Kannada Input │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Embedding Model   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Hale →     │
                    │ Hosa Examples       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        LLM          │
                    │                     │
                    │ Input + RAG Context │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Hosa Kannada      │
                    │      Output         │
                    └─────────────────────┘
```

---

# 📊 Dataset

The project uses a cleaned **Hale Kannada → Hosa Kannada parallel dataset**.

The cleaned dataset is organized into training, validation, and test data.

Example:

```text
cleaned_datasets/
├── train_final.csv
├── validation_final.csv
└── test_final.csv
```

Each record contains a Hale Kannada source and its corresponding Hosa Kannada form.

Example:

```text
Hale Kannada → Hosa Kannada

ಅವಳ್ → ಅವಳು
ಮನಂ → ಮನಸ್ಸು
ಅವರ್ → ಅವರು
ಇವರ್ → ಇವರು
```

The dataset serves as the primary knowledge source for the RAG vector database.

---

# 🗃️ ChromaDB

**ChromaDB** is used as the vector database.

The database stores:

* Hale Kannada text
* Corresponding Hosa Kannada translation
* Embeddings
* Metadata

Conceptually, one stored record looks like:

```text
Document:
ಅವಳ್

Metadata:
{
    "hosa_kannada": "ಅವಳು"
}

Embedding:
[0.123, -0.045, 0.891, ...]
```

The embedding allows the system to find semantically similar historical Kannada text.

---

# 🤖 Large Language Model

The LLM is responsible for generating the final Hosa Kannada output using:

1. The user's Hale Kannada input
2. Relevant examples retrieved from ChromaDB
3. The translation instructions

The general process is:

```text
User Input
    +
Retrieved Examples
    +
Translation Instructions
    ↓
   LLM
    ↓
Hosa Kannada
```

The LLM can therefore use domain-specific examples that may not be available in its pretrained knowledge.

---

# 🔄 Complete RAG Flow

```text
                    CLEANED DATASET
                           │
                           ▼
                   Extract Hale-Hosa
                         Pairs
                           │
                           ▼
                    Generate Embeddings
                           │
                           ▼
                       ChromaDB
                           │
                           │
                           │
User ────────► Hale Kannada Query
                           │
                           ▼
                    Generate Query
                       Embedding
                           │
                           ▼
                    Similarity Search
                           │
                           ▼
                  Top-K Relevant Examples
                           │
                           ▼
                  Build RAG Context
                           │
                           ▼
                         LLM
                           │
                           ▼
                    Hosa Kannada
```

---

# 📂 Project Structure

```text
hale-hosa-kannada-rag/
│
├── cleaned_datasets/
│   ├── train_final.csv
│   ├── validation_final.csv
│   └── test_final.csv
│
├── chroma_db/
│   └── ...
│
├── scripts/
│   ├── prepare_data.py
│   ├── build_vector_db.py
│   └── retrieve.py
│
├── rag_pipeline.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The structure can be updated as additional components are implemented.

---

# ⚙️ Installation

## 1. Clone the Repository

```powershell
git clone https://github.com/Ajay-kumar-yr/hale-hosa-kannada-rag.git
cd hale-hosa-kannada-rag
```

## 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 📦 Main Dependencies

The project uses packages such as:

```text
torch
transformers
sentence-transformers
chromadb
pandas
numpy
flask
python-dotenv
```

The exact package versions should be maintained in:

```text
requirements.txt
```

---

# 🏃 Running the Pipeline

## Step 1 — Prepare the Dataset

Place the cleaned datasets inside:

```text
cleaned_datasets/
```

For example:

```text
cleaned_datasets/
├── train_final.csv
├── validation_final.csv
└── test_final.csv
```

---

## Step 2 — Build ChromaDB

Run:

```powershell
python scripts/build_vector_db.py
```

This process:

```text
CSV Dataset
    ↓
Hale Kannada Text
    ↓
Embedding Model
    ↓
Embeddings
    ↓
ChromaDB
```

---

## Step 3 — Test Retrieval

Run:

```powershell
python scripts/retrieve.py
```

Enter a Hale Kannada query.

The system returns the most relevant Hale Kannada → Hosa Kannada examples.

---

## Step 4 — Run the RAG Pipeline

Run:

```powershell
python rag_pipeline.py
```

The pipeline performs:

```text
Input
 ↓
Embedding
 ↓
ChromaDB Search
 ↓
Retrieve Top-K Examples
 ↓
Create Context
 ↓
LLM
 ↓
Hosa Kannada
```

---

# 🌐 Web Application

A Flask-based interface can be added to expose the RAG pipeline through a web application.

Run:

```powershell
python app.py
```

The web application can provide:

```text
┌─────────────────────────────────────┐
│       Hale → Hosa Kannada           │
├─────────────────────────────────────┤
│                                     │
│  Enter Hale Kannada:                │
│                                     │
│  ಅವಳ್ ಮನಂ                          │
│                                     │
│             [ Translate ]            │
│                                     │
├─────────────────────────────────────┤
│  Hosa Kannada:                      │
│                                     │
│  ಅವಳು ಮನಸ್ಸು                       │
└─────────────────────────────────────┘
```

---

# 🧪 Example

### Input

```text
ಅವಳ್ ಮನಂ
```

### Retrieved Context

```text
Hale Kannada: ಅವಳ್
Hosa Kannada: ಅವಳು

Hale Kannada: ಮನಂ
Hosa Kannada: ಮನಸ್ಸು
```

### LLM Input

```text
Translate the following Hale Kannada into Hosa Kannada.

Use the retrieved examples as supporting context.

Retrieved examples:

ಅವಳ್ → ಅವಳು
ಮನಂ → ಮನಸ್ಸು

Input:
ಅವಳ್ ಮನಂ
```

### Output

```text
ಅವಳು ಮನಸ್ಸು
```

---

# 🎯 Objectives

* Build a domain-specific RAG system for historical Kannada.
* Retrieve relevant Hale Kannada → Hosa Kannada examples.
* Improve LLM translation using retrieved examples.
* Handle rare and archaic Kannada vocabulary.
* Create a reusable knowledge base using ChromaDB.
* Evaluate the effect of retrieval on translation quality.
* Provide a foundation for historical Kannada text modernization.

---

# 📈 Evaluation

Future evaluation can compare:

### Baseline

```text
Hale Kannada
      ↓
LLM
      ↓
Hosa Kannada
```

### RAG

```text
Hale Kannada
      ↓
ChromaDB
      ↓
Retrieved Examples
      ↓
LLM
      ↓
Hosa Kannada
```

Metrics that can be considered include:

* BLEU
* chrF
* Exact Match
* Semantic Similarity
* Human Evaluation
* Terminology Accuracy

The goal is to determine whether retrieval improves translation of archaic and rare forms.

---

# 🔬 Future Improvements

* Fine-tune IndicTrans2 specifically for Hale Kannada → Hosa Kannada.
* Compare RAG with fine-tuned IndicTrans2.
* Implement hybrid keyword + semantic retrieval.
* Add a reranking model.
* Improve Kannada-specific embeddings.
* Add metadata filtering.
* Experiment with different Top-K values.
* Add human-reviewed translation examples.
* Evaluate multiple LLMs.
* Build a Flask-based production API.
* Add paragraph-level translation.
* Add historical vocabulary lookup.
* Create a complete web interface.

---

# 🔗 Related Project

The fine-tuning/translation work is maintained separately in:

**Hale to Hosa Kannada**

```text
https://github.com/Ajay-kumar-yr/hale-to-hosa-kannada
```

This RAG repository focuses specifically on:

```text
Retrieval + Knowledge Base + LLM
```

while the other project focuses on:

```text
Dataset + Fine-tuning + Translation Model
```

---

# 📌 Project Status

**Status:** 🚧 Under Development

### Components

* [x] Cleaned Hale Kannada → Hosa Kannada dataset
* [ ] Embedding generation
* [ ] ChromaDB vector database
* [ ] Semantic retrieval
* [ ] RAG context construction
* [ ] LLM integration
* [ ] End-to-end translation
* [ ] Evaluation
* [ ] Flask web application

---

# 👨‍💻 Author

**Ajay Kumar Y R**

GitHub:
`https://github.com/Ajay-kumar-yr`

---

# 📜 License

This project is intended for research and educational purposes.

The licenses of the datasets, embedding models, LLMs, and other third-party components should be checked before redistribution or commercial use.
