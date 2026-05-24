"""Research Agent Core"""
import asyncio
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from src.core.hypothesis_engine import Hypothesis, ConsistencyCheck, KnowledgeGraphChecker, HypothesisGenerator
from src.core.tool_orchestrator import ToolChainOrchestrator, ToolRegistry, ToolState, ToolResult


@dataclass
class AgentConfig:
    max_iterations: int = 5
    confidence_threshold: float = 0.8
    tool_timeout: float = 30.0
    enable_visual_feedback: bool = True


class FeedbackRefinementEngine:
    """Feedback Refinement Engine (FRE)"""
    def refine(self, hypothesis: Hypothesis, check: ConsistencyCheck, feedback: Dict) -> Hypothesis:
        if check.passed:
            return hypothesis
        hypothesis.confidence *= 0.9
        return hypothesis


class ResearchAgent:
    """
    Research Agent: 假设生成->工具链执行->视觉反馈->假设修正 完整闭环
    """
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.hypothesis_engine = HypothesisGenerator()
        self.orchestrator = ToolChainOrchestrator(registry=ToolRegistry())
        self.lcc = KnowledgeGraphChecker()
        self.fre = FeedbackRefinementEngine()
        self.conversation_history: List[Hypothesis] = []

    async def run(self, task: str, context: Dict[str, Any]) -> Hypothesis:
        hypotheses = self.hypothesis_engine.generate(task, context, top_k=3)
        current = hypotheses[0] if hypotheses else None
        if not current:
            raise ValueError("No hypothesis generated")
        for iteration in range(self.config.max_iterations):
            plan = self.orchestrator.plan(current.statement, self.orchestrator.registry.list_tools())
            if not plan:
                break
            results = await self.orchestrator.execute_plan(plan)
            visualization = self._extract_visual(results)
            check = self.lcc.check(current)
            if check.passed and current.confidence >= self.config.confidence_threshold:
                break
            current = self.fre.refine(current, check, visualization)
            self.orchestrator.reset()
        self.conversation_history.append(current)
        return current

    def _extract_visual(self, results: List[ToolResult]) -> Dict:
        fb = {}
        for r in results:
            if r.output and isinstance(r.output, dict):
                if "chart_description" in r.output:
                    fb["chart"] = r.output["chart_description"]
        return fb

    def get_history(self) -> List[Hypothesis]:
        return self.conversation_history
