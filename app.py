import requests
import json
import account_details


account_id = account_details.account_id
token = account_details.token
rt_number = "91785"

def make_get_request(url=None):
    # print(f"make_get_request started: token {token}, account_id {account_id}")
    # print(f"URL = {url}")
    # print("")
    headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
    get_response = requests.get(url, data=None, headers=headers)
    response_list = []

    if get_response.status_code == 200:
        json_data = get_response.json()

        # lines = json_data['response']['result']['invoice_profile']['lines']
        # for line_number, line in enumerate(lines, start=1):
        #     print(f"Line number: {line_number}")
        #     print("------------------------")
        #     print(json.dumps(line, indent=2))
        #     print("     ")

        pages = int(get_response['response']['result']['pages'])
        per_page = int(get_response['response']['result']['per_page'])
        per_page = int(get_response['response']['result']['per_page'])
        current_page = get_response['response']['result']['page']

        print("pages: ", pages)
        print("per page: ", per_page)
        print("total amt = ", per_page * pages)
        # get_response = json.dumps(get_response, indent=2)

        
        if pages == 1:
            response_list.append(get_response)
            return response_list
        
        # else: add data from pages 2+
        for page in range(1, pages + 1):
            page_url = f"{url}?page={page}"
            page_response = make_get_request(page_url)
            current_page = page_response['response']['result']['page']
            print("pages: ", pages)
            print("per page: ", per_page)
            print("total amt = ", per_page * pages)

    else:
        code = get_response.status_code
        message = get_response.text
        print(f"Error code {code} : {get_response.json()['response']['errors'][0]['message']}")
        print ("Check the bearer token and account hash")
    return json_data
    


def get_rt_list():
    url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles"
    get_response = make_get_request(url)
    # print(get_response)
    # total_rt_count = sum(len(page['invoice_profiles']) for page in get_response)
    # print("Total RTs:", total_rt_count)

    pages = int(get_response['response']['result']['pages'])
    per_page = int(get_response['response']['result']['per_page'])
    per_page = int(get_response['response']['result']['per_page'])
    current_page = get_response['response']['result']['page']

    print("pages: ", pages)
    print("per page: ", per_page)
    print("total amt = ", per_page * pages)
    # get_response = json.dumps(get_response, indent=2)

    for page in range(1, pages + 1):
        # Make a request for each page
        page_url = f"{url}?page={page}"
        page_response = make_get_request(page_url)
        current_page = page_response['response']['result']['page']

        print("pages: ", pages)
        print("per page: ", per_page)
        print("total amt = ", per_page * pages)






def print_rt_lines():
    url = f""
    headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
    rt_url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles/{rt_number}?include%5B%5D=allowed_gateways&include%5B%5D=contacts&include%5B%5D=invoice_profile_customized_email&include%5B%5D=late_fee&include%5B%5D=late_reminders&include%5B%5D=lines&include%5B%5D=presentation&include%5B%5D=system&include%5B%5D=tracking&include%5B%5D=project_format&include%5B%5D=total_accrued_revenue"
    get_response = requests.get(rt_url, data=None, headers=headers)
    
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
        print(f"Error code {code} : {get_response.json()['response']['errors'][0]['message']}")
        print ("Check the bearer token and account hash")




# url = f""
# headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
# rt_url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles/{rt_number}?include%5B%5D=allowed_gateways&include%5B%5D=contacts&include%5B%5D=invoice_profile_customized_email&include%5B%5D=late_fee&include%5B%5D=late_reminders&include%5B%5D=lines&include%5B%5D=presentation&include%5B%5D=system&include%5B%5D=tracking&include%5B%5D=project_format&include%5B%5D=total_accrued_revenue"
# get_response = requests.get(rt_url, data=None, headers=headers)

# print ("Type: ",type(get_response))
# print (bool(get_response))
# print (get_response.text)
# print (get_response.status_code)
# print ("JSON ", get_response.json)


# if get_response.status_code == 200:
#     json_data = get_response.json()
#     lines = json_data['response']['result']['invoice_profile']['lines']
#     for line_number, line in enumerate(lines, start=1):
#         print(f"Line number: {line_number}")
#         print("------------------------")
#         print(json.dumps(line, indent=2))
#         print("     ")

# else:
#    code = get_response.status_code
#    message = get_response.text
#    print(f"Error code {code} : {get_response.json()['response']['errors'][0]['message']}")
#    print ("Check the bearer token and account hash")




get_rt_list()
   

# print_rt_lines()
