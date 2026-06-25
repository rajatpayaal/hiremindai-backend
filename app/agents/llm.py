from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


def get_gemini_chat() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=0.2,
    )

