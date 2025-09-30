# sort
import json
import pandas as pd
from collections import OrderedDict
json_file = "ai_search_results.json"
with open(json_file, "r", encoding="utf-8") as f:
    db = json.load(f)

for entry in db:
    results = entry.get("results", {})
    for engine, history_list in results.items():
        if not isinstance(history_list, list):
            history_list = [history_list]
        history_list.sort(
            key=lambda x: pd.to_datetime(
                x.get("date"), format="%y-%m-%d %H:%M:%S", errors="coerce"
            ) if x.get("date") else pd.NaT
        )
        none_items = [h for h in history_list if h.get("date") is None]
        non_none_items = [h for h in history_list if h.get("date") is not None]
        results[engine] = none_items + non_none_items
    sorted_results = OrderedDict(sorted(results.items(), key=lambda x: x[0].lower()))
    entry["results"] = sorted_results

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

