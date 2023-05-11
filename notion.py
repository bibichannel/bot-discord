import requests 
"""
1. Connect to Notion data
    - Created a Notion integration key
    - Save key in my_secrets.py file
    - Allow the Notion Integration key to access the page we want to share
2. Decrypt data from Notion
3. Connect to Discord
4. Push data to Discord 
"""

# header = {"Authorization":my_secrets.KEY, "Notion-Version":"2022-06-28" }
# database_id = "b07f3dd8c16849d8b800a66fc724adb7"
class Notion:
    base_url = "https://api.notion.com/v1/databases/"
    ticket = ""
    note = ""
    link = ""
    owner = ""
    assign = []
    
    def __init__(self, database_id, key):
        self.database_id = database_id
        self.key = key
        self.header = {"Authorization":self.key, "Notion-Version":"2022-06-28" }

    def get(self, query=""):
        response = requests.get(self.base_url + self.database_id, headers=self.header, data=query)
        return response

    def post(self, query=""):
        response = requests.post(self.base_url + self.database_id + "/query", headers=self.header, data=query)
        return response

    def check_ticket_assgin(self, response, ticket):
        output_to_discord = "nothing"
        for i in range(len(response.json()["results"])):
            self.ticket= response.json()["results"][i]["properties"]["Ticket"]["title"][0]["plain_text"]
            if  self.ticket == ticket:
                self.note = response.json()["results"][i]["properties"]["Note"]["rich_text"][0]["plain_text"]
                self.link = response.json()["results"][i]["properties"]["Link"]["formula"]["string"]
                self.owner = response.json()["results"][i]["properties"]["Owner"]["select"]["name"]

                for i in range(len(response.json()["results"][0]["properties"]["assign"]["multi_select"])):
                  assign_user = response.json()["results"][0]["properties"]["assign"]["multi_select"][i]["name"]
                  self.assign.append(assign_user)

                return True
        return False
    
    def dictionary_decoder(self, response):
        return [i for i in response]


# ------------------------------------------------------------------------

query = {"filter":{"property":"Ticket","exists": True}}
