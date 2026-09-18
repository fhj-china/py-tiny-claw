# cmd/claw/main.py
# 对应 Go 版: cmd/claw/main.go
# 第 5 章: 接入真实大模型 (智谱 GLM, 走 OpenAI 兼容协议) + 真实 Tool Registry + read_file 工具。
# 运行方式 (在 py-tiny-claw 目录下):
#   Windows PowerShell:  $env:ZHIPU_API_KEY="你的key"; python -m cmd.claw.main
#   Linux/macOS:         ZHIPU_API_KEY=xxx python -m cmd.claw.main

import logging
import os
import sys

from internal.engine.loop import AgentEngine
from internal.provider.openai import new_zhipu_openai_provider
from internal.tools.read_file import ReadFileTool
from internal.tools.registry import new_registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                    datefmt="%Y/%m/%d %H:%M:%S")
log = logging.getLogger(__name__)


def main():
    if not os.getenv("ZHIPU_API_KEY"):
        sys.exit("请先导出 ZHIPU_API_KEY 环境变量")

    work_dir = os.getcwd()

    # 真实大脑：智谱 GLM（OpenAI 兼容协议）。glm-4.5-air 若未开通可换 glm-4-flash
    llm_provider = new_zhipu_openai_provider("glm-4.5-air")

    # 真实手脚：动态 Tool Registry，挂载 read_file 物理工具
    registry = new_registry()
    registry.register(ReadFileTool(work_dir))

    # enable_thinking=True: 慢思考(适合复杂任务); False: 直接行动(省 Token)
    eng = AgentEngine(llm_provider, registry, work_dir, True)

    prompt = "请读取当前工作区中的 hello.txt 文件，并用中文总结文件内容。"
    try:
        eng.run(prompt)
    except Exception as e:
        sys.exit(f"引擎运行崩溃: {e}")


if __name__ == "__main__":
    main()
