#!/bin/bash
# Smart Research Agent 启动脚本
# 用法:
#   ./start.sh demo                  # 演示模式
#   ./start.sh research --topic "..."  # 完整研究
#   ./start.sh stats                 # 系统统计

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python
if ! command -v python3 &>/dev/null; then
    echo "[错误] 未找到 python3"
    exit 1
fi

# 虚拟环境
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "[Smart Research Agent] 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# 安装依赖
echo "[Smart Research Agent] 安装依赖..."
pip install -q -r requirements.txt

# 运行
python3 main.py "$@"