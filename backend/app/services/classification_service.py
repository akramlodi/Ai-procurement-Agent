import logging
import os

import google.generativeai as genai

logger = logging.getLogger(__name__)

DOCUMENT_TYPES = [
    "Purchase Request",
    "Technical Specification",
    "Supplier Quotation",
    "Contract",
    "Procurement Policy",
    "Other",
]

PROMPT = """Classify the following procurement document into exactly one of these categories:
{types}

Return ONLY the category name, nothing else.

Document:
{text}
"""


class GeminiClassificationService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def classify_document(self, text: str) -> str:
        truncated = text[:15000]
        prompt = PROMPT.format(types="\n".join(f"- {t}" for t in DOCUMENT_TYPES), text=truncated)
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            for doc_type in DOCUMENT_TYPES:
                if doc_type.lower() in result.lower():
                    return doc_type
            return "Other"
        except Exception as e:
            logger.error("Classification failed: %s", e)
            return "Other"
