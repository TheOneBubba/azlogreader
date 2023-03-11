####################################################################################################
###Module to query logs from a list of workspaces, consolidating the data into a single result set##
####################################################################################################
#Required modules
# pandas, azure.identity, azure.monitor.query, jsonpath_ng.ext 

#imports
import requests, json
import pandas
from jsonpath_ng.ext import parse

#Create token for Azure API
def get_token(client_id,tenant,redirect_uri,resource,client_secret):
    
    url = 'https://login.microsoftonline.us/{t2}/oauth2/token'.format(t2 = tenant)#cArmy DEV Tenant
    
    body = {
        'grant_type' : 'client_credentials',
        'client_id' : client_id,
        'redirect_uri' : redirect_uri,
        'resource' :  resource,
        'client_secret' : client_secret
        }
    

    x = requests.post(url,data=body)
    print(x.text)
    #z = str(x.text)
    y = json.loads(str(x.text))
    
    token = (y["access_token"]) # Contains the token obtained from the API. Not using Try/Catch because lazy.
    #print(token)
    return token
    
    

#Query Azure Resource Graph API Using token
#Accepts ARG token and returns list of workspaces accessible
def get_workspaces(token):
    
    url='https://management.usgovcloudapi.net/providers/Microsoft.ResourceGraph/resources?api-version=2021-03-01'
    headers = {
        "Authorization": "Bearer {t1}".format(t1 = token),
        'Content-Type': 'application/json'
        }
    #The query must be a valid json object
    body = {
      "query": "Resources| where type == 'microsoft.operationalinsights/workspaces'| project id = parse_json(properties.customerId) "
    }

    x = requests.post(url, json=body, headers = headers) 
    z = json.loads(x.text)
    
    workspaces_list=[]
    

    #Iterate through the the json data with json path to spit out only log analytics workspace IDs
    #Appends the ids to the workspaces_list python list.
    jsonpath_expression = parse("$.data..id")
    for match in jsonpath_expression.find(z):
    	#print(match.value)
        workspaces_list.append(match.value)
    print(len(workspaces_list))
    
    #Code by Rowley
    #This block of code creates an array of indices to split the workspaces_list on
    #The final result is a 2D array containing workspace lists of length 50 or less
    #workspace list size limited to 50 per batch due to computational constraints
    #Holman comment: I had to change the batch size from 50 to 10 because the APi was sending 500 codes
    workspace_list_piece=[]
    if(len(workspaces_list)>10):
        remainder=len(workspaces_list)
        while(remainder > 0):
            workspace_list_piece.append(workspaces_list[remainder-10:remainder-0])
            if(remainder <= 10):
                workspace_list_piece.append(workspaces_list[0:remainder-0])
            remainder-=10
    else:
        workspace_list_piece.append(workspaces_list)

    workspace_list_piece = [ele for ele in workspace_list_piece if ele != []]

    print (*workspace_list_piece, sep="\n\n")
    return workspace_list_piece

####################################################################################################
######## Now we can create an Azure Monitor Workspace Token and query all of our Workspaces ########
####################################################################################################
def logquery(token,query,workspace,additionalworkspaces=None):
    url = "https://api.loganalytics.us/v1/workspaces/{t2}/query".format(t2 = workspace)
    
    auth = {
        "Authorization": "Bearer {t1}".format(t1 = token),
        'Content-Type': 'application/json'    } 
        
    if additionalworkspaces == None:
        body = {
            "query": query,
            }
    elif additionalworkspaces != None and type(additionalworkspaces) == list:   
        body = {
            "query": query,
            "workspaces": additionalworkspaces
            }   
    #Takes the response in text form and and loads it into a dict using json.loads
    #This allows for iteration later on.
    txt_response = requests.post(url, headers = auth, json=body)
    #print(txt_response , txt_response.text)
    json_response = json.loads(str(txt_response.text))
    #print(json.dumps(json_response))
    #print(len(json_response['tables'][0]["columns"]))
    
    #Loop Through the json to create two lists of columns and rows for pandas
    #This is required because the response object is a nested json object.
    tcolumns=[]
    trows=[]
    for column in json_response['tables'][0]["columns"]:
        tcolumns.append(column["name"])
    for row in json_response['tables'][0]["rows"]:
        trows.append(row)
    
    #print(trows)
    data = pandas.DataFrame(data=trows, columns=tcolumns)

    return data, tcolumns, trows

  
def workspaces_query(token, query, workspace, additionalworkspaces):
    #Code by Rowley
    #Azure Monitor query requires a query and at least 1 target workspace 
    #loop to iterate over a list of workspaces fed into the function
    resultset=pandas.DataFrame()
    for workspaces in additionalworkspaces :
        #additional_workspaces=first# ['c90d1a9e-ea4b-44c9-97cd-bec0a9b0e2e7','9bbcac46-5949-4e69-afb9-84840e0e7ebe']
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
         
        #send the query to the target workspace(s), then add it to a dataframe, finally append that dataframe to an empty dataframe.
        logs = logquery(token, query, workspace, workspaces)
        batch = pandas.DataFrame(columns=logs[1], data=logs[2])
        resultset = resultset.append(batch, ignore_index=True) 
    return resultset

