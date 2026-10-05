from fastapi import FastAPI
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Customer support RAG")

class UserQuestion(BaseModel):
    question : str

ai_model = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature = 0.4)

knowledge_base = [
    "Customers can cancel an order within 30 minutes of placing it.",
    "Standard delivery takes 3 to 5 business days.",
    "Express delivery takes 1 to 2 business days.",
    "Refunds are processed within 5 to 7 business days after cancellation.",
    "Customers can contact support from Monday to Friday, 9 AM to 6 PM."
]

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = FAISS.from_texts(
    knowledge_base,
    embeddings
)

@app.post("/support")
def customer_support(user_question: UserQuestion):
    documents = vector_db.similarity_search(
        user_question.question,
        k=2
    )
    context = "\n".join(
        document.page_content
        for document in documents
    )
    prompt = f"""
    You are a customer support AI assistant.

    Answer the customer's question using ONLY the provided context.

    If the context does not contain enough information to answer
    the question, say "I don't know."

    Context:
    {context}

    Customer question:
    {user_question.question}
    """
    response = ai_model.invoke(prompt)

    return {
        "answer": response.content
    }
