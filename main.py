from services.ocean import search_companies

companies = search_companies("openai.com")

for company in companies:
    print(company)