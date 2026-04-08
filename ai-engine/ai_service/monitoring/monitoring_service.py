import os 
from dotenv import load_dotenv

load_dotenv()

class MonitoringService:

  VERSION = os.getenv("AI_MONITORING_VERSION")
  AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "unknown")
  AI_PROMPT_VERSION = os.getenv("AI_PROMPT_VERSION", "unknown")
  AI_GUARDRAIL_VERSION = os.getenv("AI_GUARDRAIL_VERSION", "unknown")

  # Price per million tokens (e.g. gpt-4o-mini)
  COST_INPUT_PER_1M: float = 0.15
  COST_OUTPUT_PER_1M: float = 0.60

  def estimate_cost(self, tokens_input: int, tokens_output: int) -> float:
    # Cost in dollars: (tokens / 1,000,000) * price_per_million
    input_cost: float = (tokens_input / 1_000_000) * self.COST_INPUT_PER_1M
    output_cost: float = (tokens_output / 1_000_000) * self.COST_OUTPUT_PER_1M
    
    total_cost: float = input_cost + output_cost
    # Round to avoid floating point errors
    # 10 decimals allow keeping precision (0.15/1M = 0.00000015)
    return round(total_cost, 10)

  def enrich(
        self,
        decision: dict,
        *,
        tokens_input: int,
        tokens_output: int,
        latency_ms: int,
        rag_enabled: bool,
        guardrail_triggered: str | None,
        cache_hit: bool,
    ) -> dict:

        meta = {
            "model": self.AI_MODEL_NAME,
            "prompt_version": self.AI_PROMPT_VERSION,
            "monitoring_version": self.VERSION,
            "guardrail_version": self.AI_GUARDRAIL_VERSION,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "estimated_cost": self.estimate_cost(tokens_input, tokens_output),
            "latency_ms": latency_ms,
            "rag_enabled": rag_enabled,
            "guardrail_triggered": guardrail_triggered,
            "cache_hit": cache_hit,
        }

        return {
            "decision": decision,
            "meta": meta,
        }