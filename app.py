# app.py
from flask import Flask, render_template,Response,request,stream_with_context
import time
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq
from src.helper import download_embeddings
from src.prompt import system_prompt

app = Flask(__name__)

load_dotenv()
# -------------------------
# Load Embeddings
# -------------------------
embeddings = download_embeddings()

# -------------------------
# Load FAISS Index (FAST)
# -------------------------
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# -------------------------
# Prompt Template
# -------------------------
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

MODEL_NAME = os.getenv("MODEL_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
Groq_llm_model = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=0.1
)


question_answering_chain = create_stuff_documents_chain(
    llm=Groq_llm_model,
    prompt=prompt_template
)

rag_chain = create_retrieval_chain(
    retriever,
    question_answering_chain
)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    print("User:", msg)
    def generate():
        for chunk in rag_chain.stream({"input": msg}):
            if "answer" in chunk:
                text = chunk["answer"]
                for char in text:
                    yield char
                    time.sleep(0.02)  # typing speed control

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
