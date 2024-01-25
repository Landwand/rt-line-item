import requests
import json
import account_details


account_id = account_details.account_id
token = account_details.token
rt_number = "91785"


# def mock_get_response(url):
#     print("URL : ", url)

def combine_paginated_data(response_data_json, url):
    response_list =[]

    pages = int(response_data_json['response']['result']['pages'])
    per_page = int(response_data_json['response']['result']['per_page'])
    per_page = int(response_data_json['response']['result']['per_page'])
    total_rt_count = per_page * pages

    print("pages: ", pages)
    print("per page: ", per_page)
    print("total amt = ", total_rt_count)
    
    if pages == 1:
        print("Just one page; appending")
        response_list.append(response_data_json)
        return response_list
    # else: append 1st response to [] and repeat for other pages
    response_list.append(response_data_json)
    print("Multiple pages: 1st page appended.")

    for page in range(2, pages + 1):
        print(f"Combining page # {page}")
        page_url = f"{url}?page={page}"
        page_response = make_get_request(page_url)
        response_list.append(page_response)
        print(f"{page} appended to []")

    print("Appending job complete.")
    print("len(response_list) = ", len(response_list))

    for index, response in enumerate(response_list):
        position = index + 1
        print("#############")
        print(f"Response # : {position}")
        # print (json.dumps(response, indent=2))
        with open("rt_list.txt", "w+") as file:
            file.write((json.dumps(response, indent=2)))

    return response_list


def make_get_request(url=None):
    # print(f"make_get_request started: token {token}, account_id {account_id}")
    print("make_get_request - start")
    headers = {'Authorization': f'Bearer {token}', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
    get_response = requests.get(url, data=None, headers=headers)

    if get_response.status_code == 200:
        print("GET = OK")
        json_data = get_response.json()
        return json_data
    else:
        code = get_response.status_code
        message = get_response.text
        print(f"Error code {code} : {get_response.json()['response']['errors'][0]['message']}")
        print ("Check the bearer token and account hash")
        print ("Exiting program")
        quit()


def get_list_of_rt():
    url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles"  
    response_json = make_get_request(url)
    response_list = combine_paginated_data(response_data_json=response_json, url=url)


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



## Main Program ##

get_list_of_rt()
print("Program Done!")
