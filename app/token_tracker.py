from dataclasses import dataclass

@dataclass
class TokenTracker:
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 0
    estimated_cost_usd: float = 0.0

    def add(self, input_tokens, output_tokens, input_rate, output_rate):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.calls += 1
        self.estimated_cost_usd += (
            input_tokens / 1_000_000 * input_rate
            + output_tokens / 1_000_000 * output_rate
        )

    def as_dict(self):
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "calls": self.calls,
            "estimated_cost_usd": self.estimated_cost_usd,
        }
