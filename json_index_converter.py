import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load JSON file
with open("Ecommerce-FAQ-Chatbot-Dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract Q/A pairs
qa_list = data["questions"]

# Convert each item into a LangChain Document
docs = []
for item in qa_list:
    question = item.get("question", "")
    answer = item.get("answer", "")

    # Combine for better embedding meaning
    content = f"Question: {question} | Answer: {answer}"

    docs.append(Document(page_content=content))

# Create embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Build FAISS index
db = FAISS.from_documents(docs, embeddings)

# Save index locally
db.save_local("index")

print("✅ JSON → FAISS Index Created Successfully!")
print("📁 Saved at folder: 'index/'")

