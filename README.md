---

<h1 align="center">🤖 AI-Search-Focus</h1>

  A unified framework integrating multiple AI-powered search engine APIs for experimentation and comparison.

---

## 🔍 Supported Search Engines

| Engine                  | Status                        | Website                                                                   | API / Docs                                                                                                                              | AI Model / Provider                 | Search Engine             |
| ----------------------- | ----------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------- |
| GPT-5-Search            | ✅ Available                   | [chat.openai.com](https://chat.openai.com)                                | —                                                                                                                                       | GPT-5 (OpenAI)                      | OpenAI Search             |
| Copilot                 | ❌ Unavailable                 | [Microsoft Copilot](https://www.microsoft.com/en-us/bing/copilot-search/) | —                                                                                                                                       | GPT-4 / Prometheus Hybrid           | Bing / Edge               |
| Google Vertex AI Search | ✅ Available                   | [Vertex AI](https://console.cloud.google.com/vertex-ai/tutorials)         | [API Key](https://console.cloud.google.com/apis/credentials/) <br> [Docs](https://ai.google.dev/gemini-api/docs/google-search?hl=zh-cn) | Gemini 2.5 Flash (Google Vertex AI) | Google Search             |
| Perplexity              | ✅ Available                   | [perplexity.ai](https://www.perplexity.ai/)                               | [API Key](https://www.perplexity.ai/account/api/keys)                                                                                   | Sonar (Large) / Claude-like         | Perplexity Engine         |
| Bocha                   | ✅ Available                   | [bochaai.com](https://bochaai.com/)                                       | [Docs](https://bocha-ai.feishu.cn/wiki/AT9VwqsrQinss7k84LQcKJY6nDh)                                                                     | Unknown                             | Bocha Search              |
| DeepSeek                | ✅ Available                   | [deepseek.com](https://deepseek.com/)                                     | [Doc1](https://deepseek.csdn.net/67afbce39a0a3d048dcfac68.html) <br> [Doc2](https://console.volcengine.com/)                            | DeepSeek Chat (VolcEngine Bot)      | DeepSeek Search           |
| Kimi                    | ✅ Available                   | [moonshot.cn](https://moonshot.cn/)                                       | [Docs](https://platform.moonshot.cn/docs/guide/use-web-search)                                                                                                    | Kimi-k2 (Moonshot AI)               | Kimi Web Search (Builtin) |
| You.com                 | ❌ Unavailable (Network Error) | [you.com](https://you.com)                                                | [API](https://api.you.com)                                                                                                              | YouChat AI (Claude-like)            | You.com Search            |
| Baidu                   | ❌ Unavailable                 | [chat.baidu.com](https://chat.baidu.com/)                                 | —                                                                                                                                       | Ernie Bot / 文心一言                    | Baidu Search              |
| Exa                     | ✅ Available                   | [exa.ai](https://exa.ai/)                                                 | [Dashboard](https://dashboard.exa.ai/login?redirect=/)                                                                                  | Exa AI Model                        | Exa Search Engine         |
| Tavity                  | ✅ Available                   | [tavity.com](http://tavity.com/home)                                      | [Website](http://tavity.com/home)                                                                                                       | Unknown                             | Tavity Search             |                                                               
---

## 🚀 Getting Started

1. Copy your API keys into `keys.py`.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Choose the Providers:
   open your websearch.py and choose which engine you would like to use
   ```Python
   providers = [
        ("Exa", exa_config),
        ("GPT-5-Search", gpt_search_config),
        ("Google", google_config),
        ("Bocha", bocha_config),
        ("Perplexity", perplexity_config),
        ("Tavily", tavily_config),
        ("Deepseek",deepseek_config),
        # ("You",youcom_config)
    ]
   ```

5. Run experiments:

   ```bash
   python websearch.py
   ```

---

## 📂 File Structure Overview

Here's a brief introduction to the main files and folders in this project, to help you navigate and understand the framework easily. 🧭

| File / Folder | Description | Notes |
|---------------|-------------|-------|
| `README.md` | Project overview and usage instructions | Always up-to-date guide |
| `keys.py` | Store your API keys for different search engines 🔑 | **Do not commit real keys** |
| `providers.py` | Configuration for each AI search engine provider | Add new engines here |
| `queries.py` | Example queries used for testing / experiments | Can be extended for batch experiments |
| `websearch.py` | Main script to run experiments and fetch results 🌐 | Uses selected providers to query and output JSON |
| `requirements.txt` | Python dependencies 📦 | Install with `pip install -r requirements.txt` |
| `ai_search_results.json` | Example or actual search results from experiments | Useful for reference and testing |

✨ **Tips**:  
- Keep `keys.py` secure, use placeholders in public repos.  
- You can add new engines by updating `providers.py` and `websearch.py`.  
- `ai_search_results.json` can be used for demo or testing without hitting real APIs.  
---
## 📝 Input Instructions

To run queries in this framework, you simply fill in the Python array in `queries.py`. 🎯

| File | Description | Notes |
|------|-------------|-------|
| `queries.py` | Contains the list of queries for experiments or testing | Edit the `queries` array directly in Python |

✨ **Tips**:  
- You can add as many queries as you want in the array.  
- Ensure each query is a valid string.  
- The framework will process all queries in the array sequentially and save the results in JSON format.
---
## 🖼 Example Output

Below is an example of the framework's output for a query. Sensitive data has been replaced with safe placeholders.

```json
{
  "query": "what date is it today?",
  "results": {
    "Bocha": [
      {
        "date": "2025-09-29 18:08:06",
        "time": 6838.9,
        "content": "",
        "references": [
          "https://example.com/ref1",
          "https://example.com/ref2",
          "https://example.com/ref3"
        ]
      }
    ],
    "Google": [
      {
        "date": "2025-09-29 18:09:10",
        "time": 4123.5,
        "content": "Today's date is Monday, September 29, 2025.",
        "references": [
          "https://example.com/ref1",
          "https://example.com/ref2"
        ]
      }
    ],
    "Tavity": [
      {
        "date": "2025-09-29 18:10:00",
        "time": 5234.7,
        "content": "Today's date is September 29, 2025. It is Monday. The year 2025 is not a leap year.",
        "references": [
          "https://example.com/ref1",
          "https://example.com/ref2",
          "https://example.com/ref3",
          "https://example.com/ref4"
        ]
      }
    ]
  }
}
```

💡 **Notes:**

* `query` shows the user input.
* `results` contains output from each search engine.
* `references` lists source links (here replaced with safe placeholders).

---

## ⚖️ Ethics & Responsible Use

This project is intended for **academic and defensive research only**. Do **not** use prompts or methods for malicious purposes.

---

## 📩 Responsible Disclosure

If you find a security issue, contact: `indifference.mao@outlook.com`
We will respond within **7 business days**. Please **do not publicly disclose issues** until they are resolved.

---

## 🔐 Secrets Policy

This repository **never includes API keys**.
If you find exposed credentials, please notify the maintainers immediately.

