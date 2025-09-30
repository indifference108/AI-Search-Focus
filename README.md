---

# AI-Search-Focus

A unified framework integrating multiple AI-powered search engine APIs for experimentation and comparison.

---

## 🔍 Supported Search Engines

| Engine                  | Status                        | Website                                                                   | API / Docs                                                                                                                              |
| ----------------------- | ----------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| GPT-5-Search            | ✅ Available                   | [chat.openai.com](https://chat.openai.com)                                | —                                                                                                                                       |
| Copilot                 | ❌ Unavailable                 | [Microsoft Copilot](https://www.microsoft.com/en-us/bing/copilot-search/) | —                                                                                                                                       |
| Google Vertex AI Search | ✅ Available                   | [Vertex AI](https://console.cloud.google.com/vertex-ai/tutorials)         | [API Key](https://console.cloud.google.com/apis/credentials/) <br> [Docs](https://ai.google.dev/gemini-api/docs/google-search?hl=zh-cn) |
| Perplexity              | ✅ Available                   | [perplexity.ai](https://www.perplexity.ai/)                               | [API Key](https://www.perplexity.ai/account/api/keys)                                                                                   |
| Bocha                   | ✅ Available                   | [bochaai.com](https://bochaai.com/)                                       | [Docs](https://bocha-ai.feishu.cn/wiki/AT9VwqsrQinss7k84LQcKJY6nDh)                                                                     |
| DeepSeek                | ✅ Available                   | [deepseek.com](https://deepseek.com/)                                     | [Doc1](https://deepseek.csdn.net/67afbce39a0a3d048dcfac68.html) <br> [Doc2](https://console.volcengine.com/)                            |
| You.com                 | ❌ Unavailable (Network Error) | [you.com](https://you.com)                                                | [API](https://api.you.com)                                                                                                              |
| Baidu                   | ❌ Unavailable                 | [chat.baidu.com](https://chat.baidu.com/)                                 | —                                                                                                                                       |
| Exa                     | ✅ Available                   | [exa.ai](https://exa.ai/)                                                 | [Dashboard](https://dashboard.exa.ai/login?redirect=/)                                                                                  |
| Tavity                  | ✅ Available                   | [tavity.com](http://tavity.com/home)                                      | [Website](http://tavity.com/home)                                                                                                       |

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

