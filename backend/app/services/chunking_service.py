import re


class ChunkingService:
    def __init__(self, target_tokens: int = 650, overlap_tokens: int = 100):
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def chunk_text(self, text: str) -> list[str]:
        paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

        chunks: list[str] = []
        current_parts: list[str] = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self._estimate_tokens(para)

            if current_tokens + para_tokens > self.target_tokens and current_parts:
                chunks.append("\n\n".join(current_parts))

                overlap_parts: list[str] = []
                overlap_count = 0
                for part in reversed(current_parts):
                    pt = self._estimate_tokens(part)
                    if overlap_count + pt > self.overlap_tokens:
                        break
                    overlap_parts.insert(0, part)
                    overlap_count += pt

                current_parts = overlap_parts
                current_tokens = overlap_count

            current_parts.append(para)
            current_tokens += para_tokens

        if current_parts:
            chunks.append("\n\n".join(current_parts))

        return chunks if chunks else [text] if text.strip() else []

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return len(text) // 4
