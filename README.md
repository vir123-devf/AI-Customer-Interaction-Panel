# 🎤 **AI Customer Interaction Panel**


### **AI Intern Project – Voice-Enabled Customer Support Bot**

This project implements an **AI-powered Voice Bot** that listens to customer queries, understands them, retrieves answers from an e-commerce FAQ dataset, and responds using text-to-speech.

It integrates:

* **Whisper ASR** (Speech-to-Text)
* **Cohere LLM**
* **FAISS RAG**
* **Streamlit UI**
* **Supabase Logging**

to provide a complete, real-time, voice-based customer support system.

---

## 🔗 **Links**

* **Live Demo:** [https://ai-customer-interaction-panel.streamlit.app/](https://ai-customer-interaction-panel.streamlit.app/)

[![Click Here](https://placehold.co/800x450?text=Click+Here+to+Watch+Video&font=roboto)](https://youtu.be/YzrXrdS268k)



---

## 📸 **Screenshots**

### **Main Interaction Page**

<img width="1916" height="832" alt="Main Interaction Page" src="https://github.com/user-attachments/assets/9b4ce257-7646-44ef-8df4-f63fc6e39ef0" />

---

### **Supabase Table Preview**

<img width="1860" height="762" alt="Supabase Table Preview" src="https://github.com/user-attachments/assets/0ac09535-b3c0-469c-b62b-1d9cda21db6f" />

---

### **PDF Download Example**

<img width="1029" height="773" alt="PDF Sample" src="https://github.com/user-attachments/assets/c655185d-cae5-40ac-a754-e312b2e7ea10" />

---

## 📌 **Dataset Source (Kaggle)**

This project uses the dataset:

**📂 Ecommerce-FAQ-Chatbot-Dataset.json**
Kaggle Link:
[https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset](https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset)

It contains structured question–answer pairs used to build the **RAG (Retrieval-Augmented Generation)** knowledge base.

---

## 🚀 **Project Overview**

**Title:** *AI Customer Interaction Panel*
**Goal:** Build a voice-enabled AI assistant capable of:

✔ Listening to customer queries
✔ Converting speech → text using Whisper
✔ Understanding the query via NLP
✔ Retrieving accurate answers using FAISS vector search
✔ Generating reliable responses using Cohere LLM
✔ Speaking the answer back using gTTS
✔ Storing all conversation logs to Supabase (PostgreSQL)

---

## 🔥 **Key Features**

### 🗣️ 1. Speech-to-Text (Whisper ASR)

* Converts voice input into text.
* Powered by **OpenAI Whisper (HuggingFace pipeline)**.

### 🧠 2. Natural Language Understanding

* Embedding model: `sentence-transformers/all-mpnet-base-v2`
* Vector database: **FAISS**
* Retrieves the top-k relevant FAQ entries.

### 🤖 3. Response Generation (LLM)

* Uses **Cohere "command-r-plus"** model.
* Strict RAG behavior:

  * Uses only retrieved context
  * Returns **“I don’t know”** if answer missing

### 🔊 4. Text-to-Speech (gTTS)

* Converts bot-generated responses into playable audio.

### 🗄️ 5. Supabase Integration (Cloud Storage)

All interactions are stored in a Supabase PostgreSQL table:

```json
{
  "user_message": "...",
  "bot_message": "...",
  "created_at": "..."
}
```

### 💬 6. Streamlit User Interface

* Clean UI panel
* Press mic → speak → bot replies automatically
* Chat history display
* PDF export of conversations
* Custom background support

---

## 🧠 **System Architecture**

<img width="1663" height="677" alt="image" src="https://github.com/user-attachments/assets/ffbff2fc-d783-4fbb-a7fd-82d1c9288210" />

---

## 📂 **Project Structure**

```
📦 AI-Customer-Interaction-Panel/
│
├── main.py                        # Full Streamlit voice bot app
├── json_index_converter.py        # Converts Kaggle JSON → FAISS DB
├── Ecommerce-FAQ-Chatbot-Dataset.json
├── requirements.txt
├── Background.png                 # Optional UI background
├── index/                         # Saved FAISS embeddings
│   ├── index.faiss
│   └── index.pkl
└── README.md
```

---

## 🛠️ **Installation & Setup Guide**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/AI-Customer-Interaction-Panel.git
cd AI-Customer-Interaction-Panel
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file:

```
COHERE_API_KEY=your_cohere_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
```

### 5️⃣ Create FAISS embeddings (first-time only)

```bash
python json_index_converter.py
```

### 6️⃣ Run the Streamlit app

```bash
streamlit run main.py
```

---

## 🧩 **File Descriptions**

### **main.py**

* Handles Streamlit UI
* Takes voice input
* Converts to text (Whisper)
* Performs similarity search (FAISS)
* Generates answer via Cohere
* Converts text-to-speech via gTTS
* Logs interactions to Supabase
* Allows PDF export of chat

### **json_index_converter.py**

* Loads Kaggle dataset
* Converts each FAQ Q/A into LangChain Document
* Generates embeddings using MPNet
* Builds and saves FAISS index

### **requirements.txt**

Includes dependencies for:

* Streamlit UI
* Cohere API
* FAISS
* Whisper ASR
* Huggingface Transformers
* gTTS
* Supabase client
* ReportLab PDF generator

---

## 📘 **RAG Prompt Used**

The core RAG behavior:

```
- Use ONLY the provided content.
- Do NOT generate answers outside the context.
- If answer not found → reply: "I don't know"
```

This ensures:
✔ No hallucinations
✔ High factual accuracy
✔ Fully grounded responses

---

## 🏁 **Conclusion**

The **AI Customer Interaction Panel** is a complete, production-ready prototype of a voice-based customer support system integrating:

* Whisper ASR
* FAISS Vector Search
* Cohere LLM
* gTTS
* Supabase Logging
* Streamlit Interactive UI

This is ideal for:

* E-commerce customer support
* Automated helpdesks
* Voiced FAQ systems
* AI-driven interactive kiosks
   

> **“Dreams become reality when innovation meets action.”**  
> *— Inspired by Dr. APJ Abdul Kalam*


### **Crafted with ❤️ by *Virendra Badgotya***
