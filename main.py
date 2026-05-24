#!/usr/bin/env python3
"""
Smart Research Agent - AI科研假设生成与验证系统
多智能体架构: HypothesisEngine + ToolOrchestrator + KnowledgeGraph + FeedbackRefinement

用法:
  python main.py demo                    # 演示模式(不调用真实API)
  python main.py research --topic "..."  # 完整研究流程
  python main.py stats                   # 显示系统统计
"""
import sys
import os
import argparse
import asyncio

# 确保src在路径中
sys.path.insert(0, os.path.dirname(__file__))


def print_banner():
    print("=" * 55)
    print("  Smart Research Agent - AI科研假设生成与验证系统")
    print("  Research Agent Multimodal v1.0")
    print("=" * 55)
    print()


def demo_mode(agent):
    """演示模式: 不调用真实API，展示系统能力"""
    print("[模式] 演示模式 (demo)")
    print()

    # 模拟输入
    task = "为什么Transformer在医学影像上效果比CNN好?"
    context = {"modality": "medical_imaging", "domain": "radiology"}

    print(f"输入任务: {task}")
    print(f"上下文: {context}")
    print()

    # 模拟假设生成
    print("[1/4] 假设生成引擎 (HGE)")
    hypotheses = [
        "Transformer自注意力机制能捕获医学影像中的长距离依赖关系",
        "多头注意力可以同时建模不同尺度的病灶特征",
        "位置编码使模型学习到器官的解剖结构信息",
        "预训练ViT权重迁移学习效果优于CNN",
    ]
    for i, h in enumerate(hypotheses, 1):
        print(f"  H{i}: {h}")
    print()

    # 模拟工具规划
    print("[2/4] 工具链编排 (TCO)")
    tools = ["PubMed搜索", "arXiv检索", "数据可视化", "统计分析", "文献综述"]
    for t in tools:
        print(f"  -> {t}")
    print()

    # 模拟一致性检查
    print("[3/4] 知识图谱一致性检查 (LCC)")
    checks = [
        ("H1方向性", "PASS", "注意力机制与影像特征兼容"),
        ("H2量纲检查", "PASS", "多头数量在合理范围"),
        ("H3结构约束", "PASS", "位置编码符合解剖学先验"),
        ("H4对比学习", "WARN", "预训练分布与医学影像存在gap"),
    ]
    for name, status, msg in checks:
        icon = "✅" if status == "PASS" else "⚠️"
        print(f"  {icon} [{status}] {name}: {msg}")
    print()

    # 模拟反馈修正
    print("[4/4] 反馈修正引擎 (FRE)")
    print("  修正: H4预训练权重从ImageNet迁移改为医学影像域自适应")
    print("  置信度: 0.65 -> 0.82")
    print()

    print("=" * 55)
    print("  演示完成!")
    print("  使用 --research 模式运行真实研究流程")
    print("=" * 55)


async def research_mode(agent, topic, max_iterations):
    """完整研究流程"""
    print(f"[模式] 完整研究 (topic: {topic})")
    print()

    context = {"modality": "auto", "domain": "general"}
    print(f"[Research Agent] 初始化...")
    print(f"[Research Agent] 最大迭代: {max_iterations}")
    print()

    try:
        result = await agent.run(topic, context)
        print()
        print("=" * 55)
        print("  研究完成!")
        print(f"  最终假设: {result.statement}")
        print(f"  置信度: {result.confidence:.2f}")
        print(f"  生成方法: {result.generation_method}")
        print("=" * 55)
    except Exception as e:
        print(f"[错误] 研究失败: {e}")
        print("[提示] 尝试 demo 模式: python main.py demo")


def stats_mode(agent):
    """显示系统统计"""
    print("[模式] 系统统计")
    print()
    print(f"  假设引擎: HypothesisGenerator (已加载)")
    print(f"  工具编排器: ToolChainOrchestrator (已加载)")
    print(f"  知识图谱检查器: KnowledgeGraphChecker (已加载)")
    print(f"  反馈修正引擎: FeedbackRefinementEngine (已加载)")
    print()
    print(f"  历史假设数: {len(agent.conversation_history)}")
    print(f"  最大迭代: {agent.config.max_iterations}")
    print(f"  置信度阈值: {agent.config.confidence_threshold}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Smart Research Agent - AI科研假设生成与验证系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py demo                        # 演示模式
  python main.py research --topic "AI医疗"    # 完整研究
  python main.py stats                        # 系统统计
        """,
    )
    parser.add_argument(
        'mode',
        nargs='?',
        default='demo',
        choices=['demo', 'research', 'stats'],
        help='运行模式 (默认: demo)',
    )
    parser.add_argument(
        '--topic', '-t',
        default='Transformer在医学影像中的应用优势分析',
        help='研究主题',
    )
    parser.add_argument(
        '--max-iterations', '-i',
        type=int,
        default=5,
        help='最大迭代次数 (默认: 5)',
    )
    parser.add_argument(
        '--confidence', '-c',
        type=float,
        default=0.8,
        help='置信度阈值 (默认: 0.8)',
    )

    args = parser.parse_args()
    print_banner()

    # 初始化Agent
    try:
        from src.core.research_agent import ResearchAgent, AgentConfig
        config = AgentConfig(
            max_iterations=args.max_iterations,
            confidence_threshold=args.confidence,
        )
        agent = ResearchAgent(config)
        print("[系统] 核心模块加载成功")
    except ImportError as e:
        print(f"[错误] 模块导入失败: {e}")
        print("[错误] 请检查 src/core/ 目录是否完整")
        sys.exit(1)

    # 执行对应模式
    if args.mode == 'demo':
        demo_mode(agent)
    elif args.mode == 'research':
        asyncio.run(research_mode(agent, args.topic, args.max_iterations))
    elif args.mode == 'stats':
        stats_mode(agent)


if __name__ == '__main__':
    main()