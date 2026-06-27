import asyncio
import sys
from src.tools import tools
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

agent = None
chat_history = []
MAX_HISTORY_LEN = 20

def init_agent(api_key: str, base_url: str, model_name: str):
    global agent
    
    try:
        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model_name,
            max_completion_tokens=5000,
            temperature=0.1,
            extra_body={
                "thinking": {
                    "type": "disabled",
                },
            },
        )
    except Exception as e:
        print(f"[Error] AI模型连接失败: {e}")
        sys.exit(0)

    agent = create_deep_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "你是一个具备深度联网研究能力的AI助手。\n"
            "如果用户问的问题需要细节，请先使用 ddg_search 寻找链接，\n"
            "然后使用 browse_website 工具深入阅读排名靠前的网页，最后总结出准确的答案。\n"
            "如果用户在提问时提供了网址，请直接使用 browse_website 工具浏览该网站。\n"
            "请结合之前的对话历史，连贯地回答用户的问题。"
        ),
    )

async def run_agent(prompt: str):
    global chat_history
    
    chat_history.append({"role": "user", "content": prompt})
        
    try:
        response = await agent.ainvoke({
            "messages": chat_history
        })
        ai_reply = response['messages'][-1].content
        chat_history.append({"role": "assistant", "content": ai_reply})

        if len(chat_history) > MAX_HISTORY_LEN:
            chat_history = chat_history[-MAX_HISTORY_LEN:]
            
        return f"\n{ai_reply}\n"
    except Exception as e:
        if chat_history and chat_history[-1]["role"] == "user":
            chat_history.pop()
        return f"\n[Error] AI模型运行出错: {str(e)}"
    finally:
        await asyncio.sleep(0.2)

def clear_memory():
    global chat_history
    print("\n[System] 记忆已清空，新一轮对话已开始。")
    chat_history.clear()

def undo_last_chat() -> bool:
    global chat_history
    
    if len(chat_history) >= 2:
        chat_history.pop()
        chat_history.pop()
        return True
        
    elif len(chat_history) == 1:
        chat_history.clear()
        return True
        
    return False
