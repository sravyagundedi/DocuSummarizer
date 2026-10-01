from .chunking import build_chunks
from .llm_client import LLMClient
from .prompts import (
    SUMMARY_PROMPT,
    MERGE_PROMPT,
    DECISIONS_PROMPT,
    ACTIONS_PROMPT,
    RISKS_PROMPT,
    TOPICS_PROMPT,
)
from .schemas import StructuredExtraction
from .token_tracker import TokenTracker


class DocuSummarizer:
    def __init__(self, settings):
        self.settings = settings
        self.client = LLMClient(settings)
        self.tracker = TokenTracker()

    def _record(self, response):
        if self.settings.llm_provider == "gemini":
            input_cost = self.settings.gemini_input_cost_per_1m
            output_cost = self.settings.gemini_output_cost_per_1m
        else:
            input_cost = self.settings.openai_input_cost_per_1m
            output_cost = self.settings.openai_output_cost_per_1m

        self.tracker.add(
            response.input_tokens,
            response.output_tokens,
            input_cost,
            output_cost,
        )

    def run(self, transcript, progress_callback=None):
        # ---------------------------------------------------------
        # 1. Validate transcript size
        # ---------------------------------------------------------
        words = len(transcript.split())

        if words > self.settings.max_transcript_words:
            raise ValueError(
                f"Transcript exceeds "
                f"{self.settings.max_transcript_words:,} words."
            )

        # ---------------------------------------------------------
        # 2. Build transcript chunks
        # ---------------------------------------------------------
        chunks = build_chunks(
            transcript,
            self.settings.chunk_size,
            self.settings.chunk_overlap,
        )

        if not chunks:
            raise ValueError("No usable transcript chunks were created.")

        # ---------------------------------------------------------
        # 3. Summarize each chunk
        # ---------------------------------------------------------
        summaries = []

        for i, chunk in enumerate(chunks, 1):
            if progress_callback:
                progress_callback(
                    20 + int(40 * i / len(chunks)),
                    f"Summarizing chunk {i}/{len(chunks)}...",
                )

            response = self.client.generate(
                SUMMARY_PROMPT.format(chunk=chunk.text)
            )

            self._record(response)
            summaries.append(response.text)

        # ---------------------------------------------------------
        # 4. Merge summaries ONLY when there are multiple chunks
        # ---------------------------------------------------------
        if len(summaries) == 1:
            # No need to make another Gemini API request.
            # The only chunk summary is already the final summary.
            final_summary = summaries[0]

            if progress_callback:
                progress_callback(
                    65,
                    "Using single chunk summary...",
                )

        else:
            if progress_callback:
                progress_callback(
                    65,
                    "Merging chunk summaries...",
                )

            merge_response = self.client.generate(
                MERGE_PROMPT.format(
                    summaries="\n\n---\n\n".join(summaries)
                )
            )

            self._record(merge_response)
            final_summary = merge_response.text

        # ---------------------------------------------------------
        # 5. Extract structured information
        # ---------------------------------------------------------
        prompts = {
            "decisions": DECISIONS_PROMPT,
            "actions": ACTIONS_PROMPT,
            "risks": RISKS_PROMPT,
            "topics": TOPICS_PROMPT,
        }

        extraction = {}

        for name, prompt in prompts.items():
            response, raw_response = self.client.generate_structured(
                prompt.format(transcript=transcript),
                StructuredExtraction,
                self.settings.max_retries,
            )

            self._record(raw_response)

            extraction[name] = [
                item.model_dump()
                for item in getattr(response, name)
            ]

        # ---------------------------------------------------------
        # 6. Complete
        # ---------------------------------------------------------
        if progress_callback:
            progress_callback(
                100,
                "Analysis complete.",
            )

        return {
            "summary": final_summary,
            "decisions": extraction["decisions"],
            "actions": extraction["actions"],
            "risks": extraction["risks"],
            "topics": extraction["topics"],
            "usage": self.tracker.as_dict(),
            "warnings": [],
        }