import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "gemini").lower()
    gemini_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "9000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "800"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "2"))
    max_transcript_words: int = int(os.getenv("MAX_TRANSCRIPT_WORDS", "50000"))
    gemini_input_cost_per_1m: float = float(os.getenv("GEMINI_INPUT_COST_PER_1M", "0"))
    gemini_output_cost_per_1m: float = float(os.getenv("GEMINI_OUTPUT_COST_PER_1M", "0"))
    openai_input_cost_per_1m: float = float(os.getenv("OPENAI_INPUT_COST_PER_1M", "0"))
    openai_output_cost_per_1m: float = float(os.getenv("OPENAI_OUTPUT_COST_PER_1M", "0"))
    @property
    def model_name(self):
        return self.gemini_model if self.llm_provider == "gemini" else self.openai_model
settings = Settings()
