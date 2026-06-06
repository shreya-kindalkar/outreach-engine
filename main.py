from services.ocean import search_companies

results = search_companies("openai.com")

for company in results["companies"]:
    print(
        f"{company['company'].get('name')} - "
        f"{company['company'].get('domain')}"
    )