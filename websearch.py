import logging,json
from queries import queries
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from providers import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_search_results.log"),
    ]
)

if __name__ == "__main__":
    providers = [
        # ("GPT-5-Search", gpt_search_config),
        # ("Google", google_config),
        # ("Bocha", bocha_config),
        # ("Perplexity", perplexity_config),
        # ("Exa", exa_config),
        # ("Tavily", tavily_config),
        # ("Deepseek",deepseek_config)
        # ("You.com", youcom_config),
    ]
    results_json = []

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
                    query_result["results"][name] = {
                        "content": result["content"],
                        "references": result["references"],
                    }
                    logging.info(f"Success: {name} processed query '{query}' successfully.")
                except Exception as e:
                    logging.error(f"Error with {name} on query '{query}': {e}")
                    query_result["results"][name] = {
                        "content": "",
                        "references": [],
                        "error": str(e)
                    }
        results_json.append(query_result)
    json_file = "ai_search_results.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results_json, f, ensure_ascii=False, indent=2)

    print(f"Saved: {json_file}")
