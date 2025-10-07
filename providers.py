# providers.py
# provide the AI Search Service

from keys import *
from openai import OpenAI
from openai.types.chat.chat_completion import Choice
import requests,re,httpx,json,time
from google import genai
from google.genai import types 
from datetime import datetime

SYSTEM_PROMPT = "Answer like an AI Search Engine. Give some references as you can."
JSON_FORMAT_STRING = 'Reply with a json like {"content":"...","references":[urls(more than 1)]}'

class ProviderConfig:
    def __init__(self, name, url, headers, build_payload, parse_response):
        self.name = name
        self.url = url
        self.headers = headers
        self.build_payload = build_payload
        self.parse_response = parse_response

def call_provider(config, query, extra=None):
    start = time.time() 
    extra = extra or {}
    
    # build payload
    if config.name == "google":
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config_google = types.GenerateContentConfig(tools=[grounding_tool])
    elif config.name != "gpt_search":
        payload = config.build_payload(query,extra) 
        
    # client mode APIs
    if config.name == "exa":
        client = OpenAI(base_url="https://api.exa.ai", api_key=config.headers["Authorization"].split(" ")[1])
        res = client.chat.completions.create(**payload)
        parsed = config.parse_response(res)
    elif config.name == "baidu":
        client = OpenAI(api_key=BAIDU_API_KEY,base_url="https://qianfan.baidubce.com/v2/ai_search")
        res = client.chat.completions.create(model="ernie-lite-pro-128k",messages=[{"role": "user", "content": query}],stream=False)
        parsed = config.parse_response(res)
        
    elif config.name == "google":
        client = genai.Client(api_key=GOOGLE_API_KEY)
        res = client.models.generate_content(model="gemini-2.5-flash",contents=query,config=config_google)
        parsed = config.parse_response(res)
    elif config.name == "gpt_search":
        client = OpenAI(base_url="https://svip.xty.app/v1", api_key = GPT_KEY, http_client=httpx.Client(base_url="https://svip.xty.app/v1",follow_redirects=True))
        res = client.chat.completions.create(model="gpt-5-search",messages = [{"role": "system","content": SYSTEM_PROMPT + JSON_FORMAT_STRING},{"role": "user","content": query}])
        parsed = _safe_json_parse(res.choices[0].message.content)
    elif config.name == "deepseek":
        client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3/bots",api_key=DEEPSEEK_KEY)
        res = client.chat.completions.create(model="bot-20250930112211-kjhmd",  messages=[{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": query}],)
        parsed = config.parse_response(res)
    elif config.name == "kimi":
        client = OpenAI(base_url="https://api.moonshot.cn/v1", api_key=MOONSHOT_KEY)
        messages=[{"role": "system","content":SYSTEM_PROMPT + JSON_FORMAT_STRING},{"role": "user","content": query}]
        def kimi_chat(messages) -> Choice:
            completion = client.chat.completions.create(model="kimi-k2-0905-preview",messages = messages,temperature=0.6,max_tokens=32768,
                tools=[{ "type": "builtin_function","function": {"name": "$web_search",},}]
            )
            return completion.choices[0]
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            choice = kimi_chat(messages)
            finish_reason = choice.finish_reason
            if finish_reason == "tool_calls":
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    tool_call_name = tool_call.function.name
                    tool_call_arguments = json.loads(
                        tool_call.function.arguments)
                    if tool_call_name == "$web_search":
                        tool_result = search_impl(tool_call_arguments)
                    else:
                        tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result),
                        "tool_call_id": tool_call.id,
                        "name": tool_call_name,
                    })
        res = choice.message.content
        parsed = _safe_json_parse(res)

    # request mode APIs
    else:
        res = requests.post(config.url, headers=config.headers, json=payload, timeout=20)
        parsed = config.parse_response(res.json())
        
    end = time.time()
    parsed["date"] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    parsed["time"] = round((end - start) * 1000, 1)
    return parsed

def search_impl(arguments: dict) -> any:
    return arguments

def _safe_json_parse(text: str):
    if not text:
        return {"content": "", "references": []}

    s = text.strip()
    s = re.sub(r"^```(?:json)?", "", s, flags=re.IGNORECASE).strip()
    s = re.sub(r"```$", "", s).strip()

    m = re.search(r"\{[\s\S]*\}", s)
    if m:
        s = m.group(0)

    urls = re.findall(r"https?://[^\s'\"]+", s)
    for i, u in enumerate(urls):
        s = s.replace(u, f"__URL_{i}__")
    s = re.sub(r"'", '"', s)
    for i, u in enumerate(urls):
        s = s.replace(f"__URL_{i}__", u)

    s = re.sub(r",(\s*[}\]])", r"\1", s)

    open_braces, close_braces = s.count("{"), s.count("}")
    if open_braces > close_braces:
        s += "}" * (open_braces - close_braces)
    open_brackets, close_brackets = s.count("["), s.count("]")
    if open_brackets > close_brackets:
        s += "]" * (open_brackets - close_brackets)

    try:
        data = json.loads(s)
    except Exception:
        s_clean = re.sub(r"[\x00-\x1f]+", "", s)
        try:
            data = json.loads(s_clean)
        except Exception:
            return {"content": s.strip(), "references": []}

    if isinstance(data, dict):
        content = str(data.get("content", "")).strip()
        refs = data.get("references", [])
        if not isinstance(refs, list):
            refs = []
        refs = [r for r in refs if isinstance(r, str) and r.strip()]
        refs = list(dict.fromkeys(refs))
        return {"content": content, "references": refs}
    else:
        return {"content": str(data), "references": []}

def parse_bocha_response(resp):
    content_list = []
    references = []
    for msg in resp.get("messages", []):
        if not isinstance(msg, dict):
            continue 
        msg_type = msg.get("type")
        if msg_type == "answer":
            content_list.append(msg.get("content", ""))
        elif msg_type == "source":
            raw_content = msg.get("content")
            if not raw_content:
                continue
            try:
                parsed = json.loads(raw_content)
            except Exception:
                continue
            if isinstance(parsed, list):
                for item in parsed:
                    url = item.get("url")
                    if url:
                        references.append(url)
            elif isinstance(parsed, dict):
                if "value" in parsed:
                    for item in parsed["value"]:
                        url = item.get("url")
                        if url:
                            references.append(url)
    return {
        "content": "\n".join(content_list),
        "references": references
    }
    
def parse_exa_response(r):
    content = r.choices[0].message.content
    references = re.findall(r'\[([^\]]+)\]\((https?://.*?)\)', content)
    references_list = list(dict.fromkeys([url for _, url in references]))
    def repl(m):
        return m.group(1) 
    content_simplified = re.sub(r'\[([^\]]+)\]\((https?://.*?)\)', repl, content)
    return {
        "content": content_simplified,
        "references": references_list
    }
    
def parse_baidu_response(r):
    content = ""
    references = []
    try:
        if hasattr(r, "choices") and r.choices:
            content = r.choices[0].message.content.strip()
        if hasattr(r, "references"):
            references = [ref.get("url") for ref in getattr(r, "references", []) if isinstance(ref, dict) and ref.get("url")]
        elif hasattr(r.choices[0].message, "references"):
            refs = getattr(r.choices[0].message, "references", [])
            if isinstance(refs, list):
                references = [ref.get("url") for ref in refs if isinstance(ref, dict) and ref.get("url")]
        references = list(dict.fromkeys(references))
    except Exception as e:
        content = f"[ParseError] {e}\nRaw: {str(r)[:300]}"
        references = []

    return {"content": content, "references": references}

# =================  Baidu   ====================
baidu_config = ProviderConfig(
    name="baidu",
    url=None,  
    headers=None,
    build_payload=lambda query, extra: {},
    parse_response=parse_baidu_response
)
# ================ GPT-5 Search =================
gpt_search_config = ProviderConfig(
    name="gpt_search",
    url=None,
    headers=None,
    build_payload=lambda query, extra: {},
    parse_response=None,
)

# ================= Perplexity =================
perplexity_config = ProviderConfig(
    name="perplexity",
    url="https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    },
    build_payload=lambda query, extra: {
        "model": "sonar",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": query}],
        "search_domain": "perplexity"
    },
    parse_response=lambda r: {
        "content": r["choices"][0]["message"]["content"],
        "references": r.get("citations", [])
    }
)

# =================    Exa     =================
exa_config = ProviderConfig(
    name="exa",
    url=None,
    headers={"Authorization": f"Bearer {EXA_API_KEY}"},
    build_payload=lambda query, extra: dict(
        model="exa",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        extra_body={"text": True}
    ),
    parse_response = parse_exa_response
)

# =================  Tavily   =================
tavily_config = ProviderConfig(
    name="tavily",
    url="https://api.tavily.com/search",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TAVILY_API_KEY}"
    },
    build_payload=lambda query, extra: {
        "query": query,
        "include_answer": "basic"
    },
    parse_response=lambda r: {
        "content": r.get("answer", "").strip(),
        "references": list({
            item.get("url") for item in r.get("results", []) if item.get("url")
        })
    }
)

# =================  Google  =================
google_config = ProviderConfig(
    name="google",
    url = None,
    headers = None,
    build_payload=lambda model,query,config: {
        "gemini-2.5-flash",query,config
    },
    parse_response=lambda r: {
        "content": r.text,
        "references": [
            x.web.uri 
            for x in r.candidates[0].grounding_metadata.grounding_chunks
        ] if r.candidates and r.candidates[0].grounding_metadata and r.candidates[0].grounding_metadata.grounding_chunks else []
    }
)

# =================   Bocha  ==================
bocha_config = ProviderConfig(
    name="bocha",
    url="https://api.bochaai.com/v1/ai-search",
    headers={
        "Authorization": f"Bearer {BOCHA_API_KEY}",
        "Content-Type": "application/json"
    },
    build_payload=lambda query, extra: {
        "query": query,
        "freshness": "noLimit",
        "answer": True,
        "stream": False
    },
    parse_response=parse_bocha_response
)

# =================  Deepseek  =================
deepseek_config = ProviderConfig(
    name="deepseek",
    url=None,
    headers=None,
    build_payload=lambda query, extra: {
    },
    parse_response=lambda r: {
        "content": r.choices[0].message.content,
        "references": [ref["url"] for ref in getattr(r, "references", []) if ref.get("url")]
    }
)

# =================  Kimi (Moonshot)  =================
kimi_config = ProviderConfig(
    name="kimi",
    url=None,        
    headers=None,     
    build_payload=lambda query, extra: {}, 
    parse_response=lambda r: {}            
)
