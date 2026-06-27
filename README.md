# AI搜索助手

### 如何使用
- 电脑必须具备一下解释器
    - Python > 3.9
    - uv > 0.11.24 ( 推荐，可选 )

- 如果使用pip安装
```powershell
python -m venv .venv
pip install -r requirements.txt
./run
```

- 如果使用uv安装
```powershell
uv init
uv sync
./run_uv
```

- 在 `C:/Users/你的用户名/.auto-search-assistant/config.json` 中更改成你想要的AI模型
```json
{
    "model": {
        "api_key": "你的API KEY",
        "base_url": "AI访问地址",
        "model_name": "你想要的AI模型"
    }
}
```
