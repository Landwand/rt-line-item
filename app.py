import requests
import requests
import json
import account_details
from pydantic import BaseModel
from typing import List, Dict, Optional


account_id = account_details.account_id
token = account_details.token
rt_number = "91785"


class AmountDetails(BaseModel):
    amount: float
    code: str

class AmountObj(BaseModel):
    amount: AmountDetails


class UnitCostDetails(BaseModel):
    amount: float
    code: str

class Line(BaseModel):
    amount: AmountDetails
    lineid: int
    modern_projectid: Optional[int]
    taskno: Optional[int]
    taxAmount1: Optional[int]
    taxAmount2: Optional[int]
    taxName1: Optional[str]
    taxName2: Optional[str]
    compounded_tax: bool
    description: Optional[str]
    name: str

class Lines(BaseModel):
    lines: List[Line]


class BasicRTInfo(BaseModel):
    auto_bill: bool
    id: int
    profileid: int
    vis_state: int


class InvoiceProfileDetails(BaseModel):
    auto_bill: bool
    id: int
    profileid: int
    vis_state: int
    lines: List[Lines]


class InvoiceProfileObj(BaseModel):
    invoice_profile: InvoiceProfileDetails



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
    # print (f"URL = {url}")
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


def response_list_to_rt_list(response_list):
    rt_list = []
    print("response_list_to_rt_list starts")
    print("Len response_list = ", len(response_list))
    total_len_of_rts_in_all_responses = 0
    count = 0
    for index, response in enumerate(response_list):
        print ("response_to_rt_list number ", index)
        # print (json.dumps(response, indent=2))
        rts = response['response']['result']['invoice_profiles']
        print("Len of response: ", len(response))
        print("")
        total_len_of_rts_in_all_responses = len(response) + total_len_of_rts_in_all_responses

        for rt in rts:
            count = count + 1
            print ("count ", count)
            # print ("appending to rt_list")
            # print(json.dumps(rt, indent=2))
            
            basic_rt_info = BasicRTInfo(**rt)
            if basic_rt_info.vis_state != 1: # active, archived
                rt_list.append(int(basic_rt_info.profileid))
            else:
                print(f"RT {count} is deleted !!!")
    print ("LEN RT_LIST")
    print ("")
    print(len(rt_list))
    print ("Count: ", count)
    print(total_len_of_rts_in_all_responses)
    print(f"list of RTs before returning: {len(rt_list)}")
    return rt_list
        

def print_rt_id_list(rt_list):
    print("Print RT List started ####")
    print("Length of incoming rt_list: ", len(rt_list))
    while True:
        choice = input("1 to print all or 2 to print every 10: ")
        choice = int(choice)
        if choice == 1:
            for number, rt in enumerate(rt_list, 1):
                print(f"Template Count #: {number}, id = {rt}")
            print ("Printing job done.")
            break
        if choice == 2:        
            for number, rt in enumerate(rt_list, 1):
                print (f"printing : {number}")
                if number % 10 == 0:
                    print("")
                    print("Template number printing ------")
                    print(rt)
            print ("Printing job done.")
            break



def get_rt_id_list():
    url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles"  
    response_json = make_get_request(url)
    response_list = combine_paginated_data(response_data_json=response_json, url=url)
    rt_list = response_list_to_rt_list(response_list)
    return rt_list


def show_rt_lines(id_list):
    while True:
        id = (input ("Enter an RT to show lines from: "))

        if id == " ":
            id = 91785
        id = int(id)
        
        if id in id_list:
            url = f"https://api.freshbooks.com/accounting/account/{account_id}/invoice_profiles/invoice_profiles/{id}?include%5B%5D=allowed_gateways&include%5B%5D=contacts&include%5B%5D=invoice_profile_customized_email&include%5B%5D=late_fee&include%5B%5D=late_reminders&include%5B%5D=lines&include%5B%5D=presentation&include%5B%5D=system&include%5B%5D=tracking&include%5B%5D=project_format&include%5B%5D=total_accrued_revenue"

            line_json_data = make_get_request(url=url)
            line_json_data = line_json_data['response']['result']['invoice_profile']
            rt_lines_model = Lines(**line_json_data)
            rt_lines_dump = rt_lines_model.model_dump()
            print(f"L I N E   I T E M S:")
            for line in rt_lines_dump['lines']:
                print("")
                print(f"===== Line ID :: {line['lineid']} ======")
                for key, value in line.items(): # Dict method
                    print(f"'{key}'  :  '{value}'")
                


                
            
            break
        print("Error: Profile not in list of IDs.")
        




## Main Program ##
rt_list = get_rt_id_list()
#print_rt_id_list(rt_list)
show_rt_lines(rt_list)

"""
RT examples

74893
75211
18358

"""


print("")
print("Program Done!")
