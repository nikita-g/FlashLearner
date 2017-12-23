import requests
import json
url = "https://api.quizlet.com/2.0/sets/415"


#call this method with the proper access_code
def term_definition_generator(access_code):
#input whatever access_code the access_code runner gives
    headers = {
        'client_id': "wBnJTc87dG",
        'whitespace': "1",
        'Authorization': "Bearer " + access_code
        }

    #gets the necessary data
    response = requests.request("GET", url, headers=headers)
    #converts json file into dictionary
    json_data= json.loads(response.text)


    #Get dictionary of terms
    terms_dictionary = json_data['terms']
    #terms
    terms = []
    #definitions
    definitions = []
    for dict in terms_dictionary:
        terms += [dict['term']]
        definitions += [dict['definition']]

    return terms, definitions
#EXAMPLE
#terms,definitions = term_definition_generator("b9vFCtY43VgvfQ5ZCArTr4kDn3v6r8SM9grVvnYQ")





