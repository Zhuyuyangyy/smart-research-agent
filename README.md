# Research Agent Multimodal

**AI for Science Hypothesis Generation + Verification System**

Paper: papers/03_research_agent_multimodal/

## Core Innovation

First system to truly close the loop: Hypothesis Generation -> Tool Execution -> Visual Feedback -> Hypothesis Refinement.

## 5 Core Modules

| Module | Name | Function |
|--------|------|----------|
| MPL | Multi-Modal Perception Layer | Encode images + text + data |
| HGE | Hypothesis Generation Engine | Generate physically feasible hypotheses |
| TCO | Tool Chain Orchestrator | State-machine driven tool planning |
| LCC | Logical Consistency Checker | KG-based physics + dimension checks |
| FRE | Feedback Refinement Engine | Iterative hypothesis correction |

## Code Structure

src/core/
  hypothesis_engine.py  - HGE + KG Checker + Hypothesis data structures
  tool_orchestrator.py - TCO: state machine + topological sort + tool registry
  research_agent.py     - FRE + main agent loop

## Patent

专利技术交底书.md - Full patent disclosure with 4 innovation points

## Quick Start



## 4 Innovation Points

1. **MHG**: Multi-modal hypothesis generation (not just Q&A)
2. **TCO**: State-machine tool orchestration with dependency resolution
3. **MM Feedback**: Visual feedback loop for hypothesis correction
4. **LCC**: Knowledge graph constraint checking for logical consistency
