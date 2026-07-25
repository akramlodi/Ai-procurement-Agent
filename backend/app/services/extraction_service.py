import json
import logging
import os

import google.generativeai as genai

logger = logging.getLogger(__name__)

PROMPT = """Extract structured procurement information from the following document.
Return a JSON object with these fields (use null for missing fields):

Common fields:
- supplier_name (string)
- price (number, no currency symbol)
- currency (string, e.g. "USD", "EUR")
- warranty (string, e.g. "3 years")
- delivery_days (number)
- payment_terms (string)
- compliance_score (number 0-100 if mentioned)

Additionally extract any category-specific technical details as extra fields
(e.g. processor, ram, storage, display, battery, support_level).

Document:
{text}

Return ONLY the JSON object, no markdown fences, no other text."""


class GeminiExtractionService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def extract_procurement_info(self, text: str) -> dict:
        truncated = text[:15000]
        prompt = PROMPT.format(text=truncated)
        try:
            response = self.model.generate_content(prompt)
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.error("Failed to parse extraction JSON")
            return {}
        except Exception as e:
            logger.error("Extraction failed: %s", e)
            return {}
