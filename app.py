import requests
import json

account_id = "y5lRP"
token = "eyJraWQiOiJhMTlPSlR5aVlKOXhPM3FoWnhWeE1KZE5ZNXJ4cUhpQzBSTUY0TWRheGtjIiwiYWxnIjoiUlMyNTYifQ.eyJqdGkiOiIzOTg1NDMxNGZjYzdmYmUxNDY5NWE2NzdjYmUzNDMwODJhY2NlMDY4N2VjZDM4YmJkZmZiZGFiZmQyMTgwODE0IiwiaWF0IjoxNzA1NDYxNDE1LCJleHAiOjE3MDU1MDQ2MTUsInN1YiI6IlNtdXhJZGVudGl0eTszNjM5MCIsImNsaWVudF9pZCI6IjAwNDYzMzQwNzFiOWZjMzM2NWQ4NDBkNWQ0NjNhYjg1NDIzMjMxMGU4YWU2YTE0N2FhMTI4NmRkZWViZmU1OTQiLCJzY29wZSI6InByb2ZpbGU6d3JpdGUgY3JlZGVudGlhbHM6d3JpdGUgYWRtaW46YWxsIiwiYXV0aC5mcmVzaGJvb2tzLmNvbS9zdWJfdHlwZSI6InJlc291cmNlX293bmVyIiwiYXV0aC5mcmVzaGJvb2tzLmNvbS9wdWJsaWNfYXBpX3ZlcnNpb24iOiIyMDE5LTA3LTEwIn0.fO5-4xUDu0pzKsTkCAr7kINtBuvFFLkRwS0m3pmWirqNJ5RuP536Qg_DfAjQsZuTlk80UgvRWYo4WeJc_P2C-xge2fie1rhACzFbiComZyhRwyKuFe83LT-E1hY0oUecKC2fbhH39H_VZTKhhP3g6sGZhGzBheA9StZcK6z_5fBIE0J9L6fRaQAAOimEw1fn4barFR2oGwAPAsLUFyEmFVF4Mx7ATBpoLjitvU28OmlHYfJqFN1J6i3uUrqNpo6MLpHv3MGR0m0_EEDWzxVs4jivSI2oAOvk_yG4wzgVmEeti-r-njDUWUChZ9Ml2QBo5o0uQvCBsm8Xa5X2qnvTjg"
rt_number = "91785"

url = f""
headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
rt_url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles/{rt_number}?include%5B%5D=allowed_gateways&include%5B%5D=contacts&include%5B%5D=invoice_profile_customized_email&include%5B%5D=late_fee&include%5B%5D=late_reminders&include%5B%5D=lines&include%5B%5D=presentation&include%5B%5D=system&include%5B%5D=tracking&include%5B%5D=project_format&include%5B%5D=total_accrued_revenue"


get_response = requests.get(rt_url, data=None, headers=headers)


json_data = get_response.json()


lines = json_data['response']['result']['invoice_profile']['lines']

for line_number, line in enumerate(lines, start=1):
    print(f"Line number: {line_number}")
    print("------------------------")
    print(json.dumps(line, indent=2))
    print("     ")

