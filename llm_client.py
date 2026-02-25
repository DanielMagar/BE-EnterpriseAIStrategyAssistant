from openai import OpenAI
from google import genai
from config import OPENAI_API_KEY, GEMINI_API_KEY, OPENAI_MODEL, GEMINI_MODEL


def to_openai_messages(conversation):
    formatted = []

    for msg in conversation:

        # Ensure dict format
        if not isinstance(msg, dict):
            msg = msg.model_dump()

        role = msg["role"]

        # Normalize role names
        if role == "bot":
            role = "assistant"

        formatted.append({
            "role": role,
            "content": msg["text"]
        })

    return formatted


def to_gemini_contents(conversation):
    contents = []
    system_instruction = None

    for msg in conversation:

        # Normalize to dict
        if not isinstance(msg, dict):
            msg = msg.model_dump()

        role = msg["role"]
        text = msg["text"]

        if role == "system":
            system_instruction = text
            continue

        if role in ["assistant", "bot"]:
            role = "model"

        contents.append({
            "role": role,
            "parts": [{"text": text}]
        })

    if system_instruction and contents:
        contents[0]["parts"][0]["text"] = (
            f"{system_instruction}\n\n" + contents[0]["parts"][0]["text"]
        )

    return contents


def send_chat(conversation, provider: str):

    DOMAIN_SYSTEM_PROMPT = """
You are a senior enterprise AI strategy consultant.
You provide structured, business-focused insights on:
- AI adoption strategy
- Telecom use cases
- ROI modeling
- Cost savings
- Enterprise architecture
- Tooling and ecosystem comparison

If the question is unrelated to enterprise AI strategy, respond with:
"This system only answers enterprise AI strategy and architecture questions."
"""

    # Create new conversation (DO NOT mutate original)
    final_conversation = [
        {"role": "system", "text": DOMAIN_SYSTEM_PROMPT}
    ] + conversation

    if provider == "openai":
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=to_openai_messages(final_conversation)
        )

        return response.choices[0].message.content

    elif provider == "gemini":
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=to_gemini_contents(final_conversation)
        )

        return response.text

    else:
        raise ValueError("Unsupported provider")