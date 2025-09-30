import json
import pandas as pd
json_file = "ai_search_results.json"
xlsx_file = "ai_search_results.xlsx"
with open(json_file, "r", encoding="utf-8") as f:
    db = json.load(f)
rows = []
for entry in db:
    query = entry.get("query")
    results = entry.get("results", {})
    for engine, history_list in results.items():
        if not isinstance(history_list, list):
            history_list = [history_list]
        for record in history_list:
            rows.append({
                "query": query,
                "engine": engine,
                "date": record.get("date"),
                "time": record.get("time"),
                "content": record.get("content"),
                "references": ", ".join(record.get("references", [])) 
            })
df = pd.DataFrame(rows)
df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce", format="%y-%m-%d %H:%M:%S")
df.sort_values(by=["query", "engine", "date_parsed"], inplace=True)
df.drop(columns=["date_parsed"], inplace=True)
df.to_excel(xlsx_file, index=False, engine="openpyxl")
print(f"Saved Excel file: {xlsx_file}")
