import tkinter as tk                    
from tkinter import ttk
from tkinter import Text, Scrollbar
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import time
import azreader as azr
#import azreader as azr
  
  
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

for i in range(3):
    root.columnconfigure(i, weight=1, minsize=75)
    root.rowconfigure(i, weight=1, minsize=50)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Query')
tabControl.add(tab2, text ='Log Analytics Token Gen')
tabControl.add(tab3, text ='Resource Graph Token Gen')
tabControl.pack(expand = 1, fill ="both")


#Tab 1 Query Execution and variables
#This Should be a function... 
ttk.Label(tab1,text ="Query Execution Window").grid(column=0, row=0)

query = Text(tab1, height=10, width=100, relief="sunken")
query.insert('1.0', 'VmConnection | take 10')
query.grid(column = 0,row = 1)

#Sample function to attach to a button for query window
def query_results_writer():
    #results=azr.workspaces_query(token, query, workspace, additionalworkspaces) # Connect our fields from the other tabs to this command
    messages['state']='normal'
    msg="Ran a query at {dtg} it returned {X} results".format(dtg=time.ctime(time.time()),X=10) # X=str(results.shape[0])
    messages.insert('end', msg)
    messages.insert('end', '\n')
    msg="Query Executed\n==========\n{Q}==========\n".format(Q=query.get('1.0','end'))
    messages.insert('end', msg)
    #messages.insert('end',results)
    messages['state']='disabled'
    messages.see('end')

#Creates button and tells it to run the function defined above on click.
ttk.Button(tab1,text="Run Query", command=query_results_writer).grid(column = 0,row = 2)

messages = Text(tab1,state="disabled", height=10, width=100, relief="sunken")
scrollbar = Scrollbar(messages)
messages.insert('1.0', 'Messages')
messages.grid(column = 0,row = 3)


#Sample function to attach to a button Logging Window
def log_writer():
    #help(messages)
    messages['state']='normal'
    Files=[('Text Document', '*.txt')]
    file=asksaveasfile(mode='w',filetypes = Files, defaultextension = Files, initialfile='QueryResults '+time.strftime('%Y-%m-%d %H%M%S'))
    file.write(str(messages.get("1.0", "end-1c")))
    msg="Saved to {path} on {dtg}".format(dtg=time.ctime(time.time()),path=file.name)
    messages.insert('end', msg)
    messages.insert('end', '\n')
    messages['state']='disabled'
    messages.see('end')
    
ttk.Button(tab1,text="Save Results",command=log_writer).grid(column = 0,row = 4)

#Tab 2 Log Analytics Token and variables
#This Should be a function...

ttk.Label(tab2,text ="Log Analytics Token Generator").grid(column = 0,row = 0)

#Creates a tkinter label object but does not save it to a variable
ttk.Label(tab2,text ="Client ID").grid(column = 0,row = 1, sticky="nw")

#Creates a ikinter Entry object and saves it to a variable
#See comment  below for why this is on two lines.
#client_id variable is <ttk.Entry> class

str_client_id=str()
str_tenant=str()
str_redirect_uri=str()
str_resource=str()
str_client_secret=str()

client_id=ttk.Entry(tab2, width=100, textvariable=str_client_id)
#Sets the column location of the object by referencing the variable saved to an object...
client_id.grid(column = 0,row = 2)

ttk.Label(tab2,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
#One line version; Creates object as variable and sets grid
#This object cannot be referenced post instantiation; tenant variable is <NoneType>
tenant=ttk.Entry(tab2, width=100,textvariable=str_tenant)
tenant.grid(column = 0,row = 4)

ttk.Label(tab2,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
redirect_uri=ttk.Entry(tab2, width=100,textvariable=str_redirect_uri)
redirect_uri.grid(column = 0,row = 6)

ttk.Label(tab2,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
resource=ttk.Combobox(tab2,width=50, textvariable=str_resource, state= "readonly",values=('https://api.loganalytics.us/', 'https://api.loganalytics.io/'))
resource.grid(column = 0,row = 8, sticky="nw")

ttk.Label(tab2,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
client_secret=ttk.Entry(tab2, width=100, textvariable=str_client_secret)
client_secret.grid(column = 0,row = 10)

def log_analytics_token():
    token=azr.get_token(client_id.get(),tenant.get(),redirect_uri.get(),resource.get(),client_secret.get())

ttk.Button(tab2,text="Get Log Analytics API Token",command=log_analytics_token).grid(column = 0,row = 14)



#Tab 3 Resource Token Gen and variables
#This Should be a function...
#NYI just copied and pasted
ttk.Label(tab3,text ="Resource Graph Token Generator").grid(column = 0,row = 0)

ttk.Label(tab3,text ="Client ID").grid(column = 0,row = 1, sticky="nw")
rgclient_id=ttk.Entry(tab3, width=100)
rgclient_id.grid(column = 0,row = 2)

ttk.Label(tab3,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
rgtenant=ttk.Entry(tab3, width=100)
rgtenant.grid(column = 0,row = 4)

ttk.Label(tab3,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
rgredirect_uri=ttk.Entry(tab3, width=100)
rgredirect_uri.grid(column = 0,row = 6)

ttk.Label(tab3,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
rgresource=ttk.Combobox(tab3,width=50, state="readonly",values=('https://management.azure.com/', 'https://management.usgovcloudapi.net/'))
rgresource.grid(column = 0,row = 8, sticky="nw")

ttk.Label(tab3,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
rgclient_secret=ttk.Entry(tab3, width=100)
rgclient_secret.grid(column = 0,row = 10)

def rg_log_analytics_token():
    #print(rgclient_id.get(),rgtenant.get(),rgredirect_uri.get(),rgresource.get(),rgclient_secret.get())
    rgtoken=azr.get_token(rgclient_id.get(),rgtenant.get(),rgredirect_uri.get(),rgresource.get(),rgclient_secret.get())

ttk.Button(tab3,text="Get Resource Graph API Token", command=rg_log_analytics_token).grid(column = 0,row = 14)



#Loop
root.mainloop()


#Extra code for later

##Dynamic Windows resizing code
#for i in range(3):
#  tab2.columnconfigure(i, weight=1, minsize=75)
#   tab2.rowconfigure(i, weight=1, minsize=50)
