import logging
import os

import numpy as np
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class HuggingFaceEmbeddingService:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("HF_TOKEN"))

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for text in texts:
            try:
                result = self.client.feature_extraction(text, model=MODEL)
                arr = np.array(result)
                if arr.ndim == 2:
                    arr = np.mean(arr, axis=0)
                embeddings.append(arr.tolist())
            except Exception as e:
                logger.error("Embedding generation failed for chunk: %s", e)
                embeddings.append([0.0] * 384)
        return embeddings
