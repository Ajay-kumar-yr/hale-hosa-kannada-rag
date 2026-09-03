# Hale-Hosa Kannada RAG

A Retrieval-Augmented Generation (RAG) pipeline for **Hale Kannada (Old Kannada) → Hosa Kannada (Modern Kannada)** translation and text modernization.

The project combines **ChromaDB-based semantic retrieval** with **IndicTrans2** to retrieve relevant Hale Kannada → Hosa Kannada examples before generating the final modern Kannada translation.

---

## 📌 Project Overview

Hale Kannada contains many archaic words, grammatical forms, and expressions that are different from modern Kannada.

A standard translation model may struggle with rare or historically used forms.

This project addresses this problem using a **Retrieval-Augmented Generation pipeline**:

```text
Hale Kannada Input
       │
       ▼
Text Preprocessing
       │
       ▼
Embedding Generation
       │
       ▼
ChromaDB Vector Database
       │
       ▼
Retrieve Similar Hale Kannada Examples
       │
       ▼
Retrieved Hale → Hosa Context
       │
       ▼
IndicTrans2
       │
       ▼
Hosa Kannada Output
```

---

## 🎯 Objectives

* Translate Hale Kannada into Hosa Kannada.
* Improve translation of rare and archaic words.
* Retrieve similar examples from the cleaned dataset.
* Use semantic search instead of only exact word matching.
* Combine retrieval with the IndicTrans2 translation model.
* Provide a reusable RAG pipeline for Hale Kannada modernization.

---

## 🧠 Technologies Used

| Technology                | Purpose                     |
| ------------------------- | --------------------------- |
| Python                    | Core programming language   |
| IndicTrans2               | Neural machine translation  |
| ChromaDB                  | Vector database             |
| Sentence Transformers     | Text embeddings             |
| PyTorch                   | Deep learning framework     |
| Hugging Face Transformers | Model loading and inference |
| Pandas                    | Dataset processing          |
| Flask                     | Optional web/API layer      |

---

## 📂 Project Structure

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
├── embeddings/
│   └── ...
│
├── scripts/
│   ├── prepare_data.py
│   ├── build_vector_db.py
│   └── retrieve.py
│
├── app.py
├── rag_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The exact structure may change as the project develops.

---

## 📊 Dataset

The project uses a cleaned Hale Kannada → Hosa Kannada parallel dataset.

Each training example follows the general format:

```text
Hale Kannada → Hosa Kannada
```

Example:

```text
Hale Kannada:
ಅವಳ್

Hosa Kannada:
ಅವಳು
```

Another example:

```text
Hale Kannada:
ಮನಂ

Hosa Kannada:
ಮನಸ್ಸು
```

The cleaned dataset is used as the knowledge source for semantic retrieval.

---

## 🔍 How RAG Works

### 1. Load the Dataset

The cleaned CSV files are loaded using Pandas.

```text
train_final.csv
validation_final.csv
test_final.csv
```

---

### 2. Create Embeddings

Hale Kannada text is converted into numerical vectors using an embedding model.

Conceptually:

```text
Hale Kannada text
        ↓
Embedding Model
        ↓
Vector representation
```

Semantically similar texts should have similar vector representations.

---

### 3. Store Vectors in ChromaDB

The embeddings and corresponding Hale Kannada → Hosa Kannada examples are stored in ChromaDB.

```text
ChromaDB

ID
 │
 ├── Hale Kannada text
 ├── Hosa Kannada translation
 └── Embedding vector
```

This allows fast semantic retrieval.

---

### 4. Retrieve Relevant Examples

When a user enters a new Hale Kannada sentence:

```text
ಅವಳ್ ಮನಂ
```

the system searches ChromaDB for similar examples.

For example:

```text
Retrieved examples:

ಅವಳ್ → ಅವಳು

ಮನಂ → ಮನಸ್ಸು
```

These examples become the retrieval context.

---

### 5. Translation with IndicTrans2

The retrieved examples are combined with the input and passed to the translation pipeline.

```text
Input:
ಅವಳ್ ಮನಂ

Retrieved Context:
ಅವಳ್ → ಅವಳು
ಮನಂ → ಮನಸ್ಸು

        ↓

IndicTrans2

        ↓

Output:
ಅವಳು ಮನಸ್ಸು
```

The actual output depends on the model and retrieved context.

---

## 🤖 IndicTrans2

This project uses **AI4Bharat IndicTrans2** as the translation model.

Model:

```text
ai4bharat/indictrans2-indic-indic-dist-320M
```

IndicTrans2 provides multilingual translation capabilities for Indian languages and is used here as the translation backbone.

---

## 🗃️ Vector Database

**ChromaDB** is used to store and retrieve the embedded Hale Kannada examples.

The database allows the system to perform semantic similarity searches such as:

```text
Query
  ↓
Embedding
  ↓
ChromaDB
  ↓
Top-K similar examples
```

This is particularly useful for rare or uncommon Hale Kannada forms.

---

## 🔄 Complete Pipeline

```text
                  ┌─────────────────────┐
                  │  Cleaned Dataset    │
                  │ Hale → Hosa pairs   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Embedding Model    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     ChromaDB        │
                  │   Vector Database   │
                  └──────────┬──────────┘
                             │
                             │
User Input ───────► Embedding
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Semantic Retrieval  │
                  │      Top-K          │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Retrieved Context   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    IndicTrans2      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Hosa Kannada      │
                  └─────────────────────┘
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ajay-kumar-yr/hale-hosa-kannada-rag.git
cd hale-hosa-kannada-rag
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 📦 Required Packages

The project requires packages such as:

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

The final versions should be maintained in:

```text
requirements.txt
```

---

## 🚀 Building the Vector Database

After preparing the cleaned dataset, run:

```powershell
python scripts/build_vector_db.py
```

This will:

1. Load the cleaned dataset.
2. Extract Hale Kannada text.
3. Generate embeddings.
4. Create the ChromaDB collection.
5. Store the embeddings and translation pairs.

---

## 🔎 Testing Retrieval

To test semantic retrieval:

```powershell
python scripts/retrieve.py
```

Example query:

```text
ಅವಳ್ ಮನಂ
```

The system returns the most relevant Hale Kannada → Hosa Kannada examples from ChromaDB.

---

## 🌐 Running the Application

If the Flask application is enabled:

```powershell
python app.py
```

The application can then be accessed locally through the Flask server.

---

## 🧪 Example

### Input

```text
ಅವಳ್ ಮನಂ
```

### Retrieved Context

```text
ಅವಳ್ → ಅವಳು
ಮನಂ → ಮನಸ್ಸು
```

### Generated Output

```text
ಅವಳು ಮನಸ್ಸು
```

The purpose of retrieval is to provide the translation model with relevant examples that may help with archaic vocabulary and forms.

---

## 📈 Future Improvements

* Fine-tune IndicTrans2 specifically for Hale Kannada → Hosa Kannada.
* Improve the embedding model for Kannada historical text.
* Add metadata-based retrieval.
* Add hybrid search combining lexical and semantic retrieval.
* Add reranking for retrieved examples.
* Evaluate RAG vs. non-RAG translation quality.
* Add BLEU, chrF, and semantic evaluation.
* Build a user-friendly web interface.
* Support paragraph-level historical Kannada translation.
* Add human evaluation by Kannada language experts.

---

## 🔬 Research Direction

The project can be extended into a research-oriented system for **historical Kannada text modernization**.

Potential research questions include:

* Does RAG improve translation of rare Hale Kannada words?
* Which embedding model performs best for Kannada?
* How many retrieved examples provide the best performance?
* Does hybrid retrieval outperform semantic-only retrieval?
* How does RAG compare with a fine-tuned IndicTrans2 model?
* Can human-reviewed examples improve retrieval quality?

---

## 📌 Project Status

**Current Stage:** RAG pipeline development

Planned components:

* [x] Cleaned parallel dataset
* [ ] Embedding generation
* [ ] ChromaDB vector database
* [ ] Semantic retrieval
* [ ] IndicTrans2 integration
* [ ] End-to-end RAG pipeline
* [ ] Evaluation
* [ ] Web interface

---

## 👨‍💻 Author

**Ajay Kumar Y R**

GitHub:
`https://github.com/Ajay-kumar-yr`

---

## 📜 License

This project is intended for research and educational purposes.

Check the licenses of the datasets, embedding models, and IndicTrans2 before redistributing them or using the system commercially.
