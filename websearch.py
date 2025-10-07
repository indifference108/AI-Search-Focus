# websearch.py
import logging,json,os,time,warnings
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from providers import *  
from queries import queries  
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_search_results.log"),
    ]
)

# we use this json file as a database
json_file = "ai_search_results.json"
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    db = []
query_index = {entry["query"]: entry for entry in db}

if __name__ == "__main__":
    providers = [
        # ("Exa", exa_config),
        # ("GPT-5-Search", gpt_search_config),
        # ("Google", google_config),
        # ("Bocha", bocha_config),
        # ("Perplexity", perplexity_config),
        # ("Tavily", tavily_config),
        # ("Deepseek",deepseek_config),
        # ("Kimi",kimi_config)
        ("Baidu",baidu_config),
    ]

    for query in tqdm(queries, desc="Processing Queries", ncols=100):
        query_result = {"query": query, "results": {}}
        with ThreadPoolExecutor(max_workers=len(providers)) as executor:
            future_to_name = {
                executor.submit(call_provider, config, query, extra={"maxResults": 5}): name
                for name, config in providers
            }
            for future in as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    result = future.result()
                    engine_result = {
                        "date": result["date"],     
                        "time": result["time"],     
                        "content": result["content"],
                        "references": result["references"]
                    }
                    logging.info(f"Success: {name} processed query '{query}' successfully.")
                    
                except Exception as e:
                    engine_result = {
                        "date": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
                        "time": 0,
                        "content": "",
                        "references": [],
                        "error": str(e)
                    }
                    logging.error(f"Error with {name} on query '{query}': {e}")
                    
                if query in query_index:
                    existing_results = query_index[query]["results"]
                    if name in existing_results:
                        if isinstance(existing_results[name], list):
                            existing_results[name].append(engine_result)
                        else:
                            existing_results[name] = [existing_results[name], engine_result]
                    else:
                        existing_results[name] = [engine_result]
                else:
                    query_result["results"][name] = [engine_result]
                    db.append(query_result)
                    query_index[query] = query_result

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Saved: {json_file}")
