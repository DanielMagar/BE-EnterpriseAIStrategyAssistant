from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest
from llm_client import send_chat

app = FastAPI(title="Enterprise AI Backend")

# 👇 Add this
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
INTRO_KEYWORDS = ["hi", "hello", "hey", "greetings"]
POLITE_WORDS = ["thanks", "thank you", "ok", "okay", "great", "goodbye", "bye"]

ALLOWED_KEYWORDS = [
    "ai",
    "llm",
    "tooling",
    "architecture",
    "telecom",
    "churn",
    "roadmap",
    "automation",
    "cost",
    "roi",
    "strategy",
    "enterprise",
    "python", "java", 
    "node", 
    "c#", "go", 
    "ruby", 
    "php", 
    "scala", 
    "kotlin", 
    "swift",
     "frontend", "backend", "fullstack", "devops", "data engineering", "machine learning", "deep learning"
]

def is_relevant(text: str):
    return any(keyword in text.lower() for keyword in ALLOWED_KEYWORDS)


@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.conversation[-1].text.strip().lower()

    # 0️⃣ Greeting handling
    if user_message in INTRO_KEYWORDS:
        return {
            "provider_used": request.provider,
            "response": "Hello! I'm your enterprise AI consultant specializing in Tooling Equivalence Mapping. How can I assist you today?"
        }
    # 1️⃣ Polite closing handling
    if user_message in POLITE_WORDS:
        return {
            "provider_used": request.provider,
            "response": "You're welcome. If you have more questions about Tooling Equivalence Mapping, feel free to ask."
        }

    # 2️⃣ Domain restriction
    if not is_relevant(user_message):
        return {
            "provider_used": request.provider,
            "response": "This system only answers questions related to Tooling Equivalence Mapping."
        }

    # 3️⃣ Call LLM if valid
    response = send_chat(
        conversation=request.conversation,
        provider=request.provider
    )

    return {
        "provider_used": request.provider,
        "response": response
    }