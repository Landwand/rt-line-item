import requests
import json
import bearer_token

account_id = "y5lRP"
token = bearer_token.token
rt_number = "91785"

url = f""
headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
rt_url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles/{rt_number}?include%5B%5D=allowed_gateways&include%5B%5D=contacts&include%5B%5D=invoice_profile_customized_email&include%5B%5D=late_fee&include%5B%5D=late_reminders&include%5B%5D=lines&include%5B%5D=presentation&include%5B%5D=system&include%5B%5D=tracking&include%5B%5D=project_format&include%5B%5D=total_accrued_revenue"

get_response = requests.get(rt_url, data=None, headers=headers)
# print ("Type: ",type(get_response))
# print (bool(get_response))
# print (get_response.text)
# print (get_response.status_code)
# print ("JSON ", get_response.json)


if get_response.status_code == 200:

    json_data = get_response.json()
    lines = json_data['response']['result']['invoice_profile']['lines']

    for line_number, line in enumerate(lines, start=1):
        print(f"Line number: {line_number}")
        print("------------------------")
        print(json.dumps(line, indent=2))
        print("     ")

else:
   code = get_response.status_code
   message = get_response.text
   print(f" Error code: {code} : {get_response.json()['response']['errors'][0]['message']}")