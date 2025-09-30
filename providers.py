# providers.py
# provide the AI Search Service

from keys import *
from openai import OpenAI
import requests,re,httpx,json,time
from google import genai
from google.genai import types 
from datetime import datetime

SYSTEM_PROMPT = "Answer like an AI Search Engine. Give some references as you can."

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
    elif config.name == "google":
        client = genai.Client(api_key=GOOGLE_API_KEY)
        res = client.models.generate_content(model="gemini-2.5-flash",contents=query,config=config_google)
        parsed = config.parse_response(res)
    elif config.name == "gpt_search":
        client = OpenAI(base_url="https://svip.xty.app/v1", api_key = GPT_KEY, http_client=httpx.Client(base_url="https://svip.xty.app/v1",follow_redirects=True))
        res = client.chat.completions.create(model="gpt-5-search",messages = [{"role": "system","content": SYSTEM_PROMPT + "Reply with a json like {'content':' ','references': [urls(more than 1)]}"},{"role": "user","content": query}])
        parsed = json.loads(res.choices[0].message.content)
    elif config.name == "deepseek":
        client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3/bots",api_key=DEEPSEEK_KEY)
        res = client.chat.completions.create(model="bot-20250930112211-kjhmd",  messages=[{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": query}],)
        parsed = config.parse_response(res)
    # request mode APIs
    else:
        res = requests.post(config.url, headers=config.headers, json=payload, timeout=20)
        parsed = config.parse_response(res.json())
        
    end = time.time()
    parsed["date"] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    parsed["time"] = round((end - start) * 1000, 1)
    return parsed

def parse_bocha_response(resp):
    content_list = []
    references = []
    for msg in resp.get("messages", []):
        if not isinstance(msg, dict):
            continue 
        msg_type = msg.get("type")
        content_type = msg.get("content_type")
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

# =================  You.com   =================
youcom_config = ProviderConfig(
    name="you.com",
    url="https://api.you.com/v1/agents/runs",
    headers={
        "Authorization": f"Bearer {YOUCOM_API_KEY}",
        "Content-Type": "application/json"
    },
    build_payload=lambda query, extra: {
        "agent": extra.get("agent", "express"),
        "input": query,
        "tools": [
            {"type": "web_search", "trigger": extra.get("trigger", "force")}
        ]
    },
    parse_response=lambda r: {
        "content": next(
            (o["text"] for o in r.get("output", []) if o.get("type") == "message.answer"),
            ""
        ),
        "references": [
            item.get("url")
            for o in r.get("output", [])
            if o.get("type") == "web_search.results"
            for item in o.get("content", [])
            if "url" in item
        ]
    }
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
