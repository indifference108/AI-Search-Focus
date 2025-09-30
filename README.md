---

# AI-Search-Framework

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

3. Run experiments:

   ```bash
   python run_experiments.py
   ```

---

## 🖼 Example Output

Below is an example of the framework's output for a query. Sensitive data has been replaced with safe placeholders.

```json
{
  "query": "what date is it today?",
  "results": {
    "Google": {
      "content": "Today's date is Monday, September 29, 2025.",
      "references": []
    },
    "Tavity": {
      "content": "Today's date is September 29, 2025. It is Monday. The year 2025 is not a leap year.",
      "references": [
        "https://example.com/date1",
        "https://example.com/date2",
        "https://example.com/date3",
        "https://example.com/date4"
      ]
    },
    "Perplexity": {
      "content": "It is Monday, September 29, 2025.",
      "references": []
    }
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

