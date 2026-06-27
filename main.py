import asyncio
import sys
import os
import json
import src.agent as agent

config_path = f"config.json"

if not os.path.exists(config_path):
    config = {
        "model": {
            "api_key": "your-deepseek-api-key",
            "base_url": "https://api.deepseek.com",
            "model_name": "deepseek-v4-flash",
        },
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    sys.exit(0)

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

agent.init_agent(
    api_key=config["model"]["api_key"], 
    base_url=config["model"]["base_url"], 
    model_name=config["model"]["model_name"],
)

async def main():
    print()
    while True:
        user = input("[User] ")

        if user.strip() in ["/exit", "/quit"]:
            print()
            break
        elif user.strip() == "/clear":
            agent.clear_memory()
            continue
        elif user.strip() == "/undo":
            if agent.undo_last_chat():
                print("\n[System] 已撤销上一轮对话记忆。\n")
            else:
                print("\n[System] 当前没有可以撤销的对话历史。\n")
            continue
        elif user.strip().startswith("/"):
            print("\n[System] 指令不存在\n")
            continue
        elif user.strip():
            res = await agent.run_agent(user)
            print(res)
            continue

if sys.platform == 'win32':
    from asyncio.proactor_events import _ProactorBasePipeTransport
    
    old_del = _ProactorBasePipeTransport.__del__
    def silence_windows_pipe_error(self):
        try: 
            old_del(self)
        except: 
            pass
    _ProactorBasePipeTransport.__del__ = silence_windows_pipe_error

try: 
    asyncio.run(main())
except: 
    pass
