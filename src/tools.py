from langchain.tools import tool
from cloakbrowser import launch_async
from ddgs import DDGS

@tool
async def ddg_search(query: str, max_results: int = 3) -> str:
    """
    当你想查询实时信息或寻找某个特定网站的链接时使用此工具。
    传入的 query 应当是精简的搜索关键词，禁止传入长句子。
    """

    print(f"\n[Tool] 搜索资料: {query}")

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if not results:
                return "未找到相关搜索结果。"
            
            formatted_results = []
            for r in results:
                formatted_results.append(f"标题: {r.get('title')}\n链接: {r.get('href')}\n摘要: {r.get('snippet')}\n")

            return "\n===\n".join(formatted_results)
    except Exception as e:
        return f"搜索失败: {str(e)}"

@tool
async def browse_website(url: str) -> str:
    """
    当通过搜索获得了具体网址（URL），且需要深入阅读该网页的详细具体内容时，调用此工具。
    此工具拥有极强的反爬绕过能力，采用异步非阻塞 I/O 运行。
    """

    print(f"\n[Tool] 浏览网站: {url}")

    try:
        browser = await launch_async(
            headless=True, 
            humanize=True, 
            human_preset="default"
        )
        
        page = await browser.new_page()
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")

        page_text = await page.locator("body").inner_text()
        await browser.close()

        cleaned_text = "\n".join([line.strip() for line in page_text.splitlines() if line.strip()])
        return f"--- 网页内容开始 ({url}) ---\n{cleaned_text[:4000]}\n--- 网页内容结束 ---"
            
    except Exception as e:
        return f"\n[Error] 无法浏览该网页，错误原因: {str(e)}"

tools = [
    ddg_search,
    browse_website,
]
