import logging
import os

import google.generativeai as genai

logger = logging.getLogger(__name__)

PROMPT = """Generate a concise summary (maximum 100 words) of the following procurement document.
Focus on the key procurement details: what is being procured, from whom, key terms, and any notable conditions.

Document:
{text}

Summary:"""


class GeminiSummaryService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def generate_summary(self, text: str) -> str:
        truncated = text[:15000]
        prompt = PROMPT.format(text=truncated)
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error("Summary generation failed: %s", e)
            return ""
