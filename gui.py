import tkinter as tk                    
from tkinter import ttk
from tkinter import Text, Scrollbar
from tkinter.filedialog import asksaveasfile, asksaveasfilename, StringVar
import time
import azreader as azr
import traceback
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

querytype = StringVar()
ttk.Radiobutton(tab1, text='Query Multiple Workspaces', variable=querytype, value='multi').grid(column = 0,row = 1, sticky="nw")
ttk.Radiobutton(tab1, text='Query Single Workspace', variable=querytype, value='single').grid(column = 0,row = 2, sticky="nw")

wks_id=ttk.Label(tab1,text ="Workspace ID to query from")
wks_id=ttk.Entry(tab1, width=100)
wks_id.grid(column = 0,row = 3, sticky="nw", pady=10)

query = Text(tab1, height=10, width=100, relief="sunken")
query.insert('1.0', 'VmConnection | take 10')
query.grid(column = 0,row = 5)

#Sample function to attach to a button for query window

results=None

def query_results_writer():
    global results
    messages['state']='normal'
    print(wks_id.get())
    print(logtoken.get())
    print((query.get('1.0','end')).replace('\n', ' '))
    if workspaces is not None :
        print(len(workspaces))
        
    try:
        if querytype.get() == '':
            messages.insert('end', "\nError: Choose a query type above!\n")
        elif querytype.get() == "single" :
            data=azr.logquery(logtoken.get(), query.get('1.0','end').replace('\n', ' '), wks_id.get())
            results=data[0]
        elif querytype.get() == "multi":
            data=azr.workspaces_query(logtoken.get(), query.get('1.0','end').replace('\n', ' '), wks_id.get(), workspaces)
            results=data
               
        msg="Ran a query at {dtg} it returned {X} results".format(dtg=time.ctime(time.time()),X=len(results.index))
        messages.insert('end', msg)
        messages.insert('end', '\n')
        msg="Query Executed\n==========\n{Q}==========\n\n".format(Q=query.get('1.0','end'))
        messages.insert('end', msg)
        #messages.insert('end',results)
        messages.see('end')
    except:
        messages.insert('end', time.ctime(time.time()), '', '\n')
        messages.insert('end', traceback.format_exc(), '', '\n','', '-----------------')


    messages['state']='disabled'
        

#Creates button and tells it to run the function defined above on click.
ttk.Button(tab1,text="Run Query", command=query_results_writer).grid(column = 0,row = 99)

messages = Text(tab1,state="disabled", height=10, width=100, relief="sunken")
scrollbar = Scrollbar(messages)
messages.insert('1.0', 'Messages')
messages.grid(column = 0,row = 199)


#Sample function to attach to a button Logging Window
def log_writer():
    #help(messages)
    messages['state']='normal'
    Files=[('Text Document', '*.txt')]
    file=asksaveasfile(mode='w',filetypes = Files, defaultextension = Files, initialfile='QueryResults '+time.strftime('%H%M.%Y-%m-%d'))
    file.write(results.to_csv())
    msg="Saved to {path} on {dtg}".format(dtg=time.ctime(time.time()),path=file.name)
    messages.insert('end', msg)
    messages.insert('end', '\n')
    messages['state']='disabled'
    messages.see('end')
    
ttk.Button(tab1,text="Save Results",command=log_writer).grid(column = 0,row = 200)

#Tab 2 Log Analytics Token and variables
#This Should be a class...
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

logclient_id=ttk.Entry(tab2, width=100, textvariable=str_client_id)
#Sets the column location of the object by referencing the variable saved to an object...
logclient_id.grid(column = 0,row = 2, sticky="nw")

ttk.Label(tab2,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
#One line version; Creates object as variable and sets grid
#This object cannot be referenced post instantiation; tenant variable is <NoneType>
logtenant=ttk.Entry(tab2, width=100,textvariable=str_tenant)
logtenant.grid(column = 0,row = 4, sticky="nw")

ttk.Label(tab2,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
logredirect_uri=ttk.Entry(tab2, width=100,textvariable=str_redirect_uri)
logredirect_uri.grid(column = 0,row = 6, sticky="nw")

ttk.Label(tab2,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
logresource=ttk.Combobox(tab2,width=50, textvariable=str_resource, state= "readonly",values=('https://api.loganalytics.us/', 'https://api.loganalytics.io/'))
logresource.grid(column = 0,row = 8, sticky="nw")

ttk.Label(tab2,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
logclient_secret=ttk.Entry(tab2, width=100, textvariable=str_client_secret)
logclient_secret.grid(column = 0,row = 10, sticky="nw")

#Log Token variable. StringVar object so it works better with tkinter
#If the user enters the right parameters, logtoken will contain the token, else it will render an error.
##Need to change return of azurereader.get_token() to give http status code and message too.
logtoken=StringVar()
logtoken_status = StringVar()
def log_analytics_token():
    try:
        x=azr.get_token(logclient_id.get(),logtenant.get(),logredirect_uri.get(),logresource.get(),logclient_secret.get())
        #x="LogTokenTest"
    except Exception as err:
        logtoken_mesg['foreground']='red'
        logtoken_status.set('Token Status: No Token. Check parameters and see error message below')
        logtoken_mesg['state']='normal'
        logtoken_mesg.delete('1.0', 'end')
        logtoken_mesg.insert('end', time.ctime(time.time()), '', '\n')
        logtoken_mesg.insert('end', traceback.format_exc(), '', '\n')
        logtoken_mesg['state']='disabled'
    else:
        logtoken_status.set('Token Status: Good')
        logtoken_mesg.delete('1.0', 'end')
        logtoken.set(x)

ttk.Button(tab2,text="Get Log Analytics API Token",command=log_analytics_token).grid(column = 0,row = 14)

ttk.Label(tab2, textvariable=logtoken_status).grid(column = 0,row = 15)

logtoken_mesg = Text(tab2,state="disabled", height=30, width=100, relief="sunken")
logtoken_mesg.grid(column = 0,row = 16)


#Tab 3 Resource Token Gen and variables
#This Should be a class...
ttk.Label(tab3,text ="Resource Graph Token Generator").grid(column = 0,row = 0)

ttk.Label(tab3,text ="Client ID").grid(column = 0,row = 1, sticky="nw")
rgclient_id=ttk.Entry(tab3, width=100)
rgclient_id.grid(column = 0,row = 2, sticky="nw")

ttk.Label(tab3,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
rgtenant=ttk.Entry(tab3, width=100)
rgtenant.grid(column = 0,row = 4, sticky="nw")

ttk.Label(tab3,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
rgredirect_uri=ttk.Entry(tab3, width=100)
rgredirect_uri.grid(column = 0,row = 6, sticky="nw")

ttk.Label(tab3,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
rgresource=ttk.Combobox(tab3,width=50, state="readonly",values=('https://management.azure.com/', 'https://management.usgovcloudapi.net/'))
rgresource.grid(column = 0,row = 8, sticky="nw")

ttk.Label(tab3,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
rgclient_secret=ttk.Entry(tab3, width=100)
rgclient_secret.grid(column = 0,row = 10, sticky="nw")



#Resource Token variable. StringVar object so it works better with tkinter
#If the user enters the right parameters, rgtoken will contain the token, else it will render an error.
##Need to change return of azurereader.get_token() to give http status code and message too.
rgtoken=StringVar()
rgtoken_status = StringVar()
def rg_log_analytics_token():
    #print(rgclient_id.get(),rgtenant.get(),rgredirect_uri.get(),rgresource.get(),rgclient_secret.get())
    rgtoken_mesg['state']='normal'
    try:
        x=azr.get_token(rgclient_id.get(),rgtenant.get(),rgredirect_uri.get(),rgresource.get(),rgclient_secret.get())
        #x="text"
    except Exception as err:
        rgtoken_mesg['foreground']='red'
        rgtoken_status.set('Token Status: No Token. Check parameters and see error message below')
        rgtoken_mesg['state']='normal'
        rgtoken_mesg.delete('1.0', 'end')
        rgtoken_mesg.insert('end', time.ctime(time.time()), '', '\n')
        rgtoken_mesg.insert('end', traceback.format_exc(), '', '\n')  
    else:
        rgtoken_mesg.delete('1.0', 'end')
        rgtoken_status.set('Token Status: Good')
        rgtoken.set(x)
    rgtoken_mesg['state']='disabled'
        
workspaces=None
def pop_workspace_list():
    rgtoken_mesg['state']='normal'
    rgtoken_mesg.delete('1.0', 'end')
    global workspaces
    workspaces=azr.get_workspaces(rgtoken.get())
    n=0
    for w in workspaces:
        n+=len(w)

    rgtoken_mesg.insert('end', time.ctime(time.time()), '', '\n','',"{x} workspaces retrived".format(x=n))
    rgtoken_mesg['state']='disabled'
    

ttk.Button(tab3,text="Get Resource Graph API Token", command=rg_log_analytics_token).grid(column = 0,row = 14)
ttk.Button(tab3,text="Get all workspaces", command=pop_workspace_list).grid(column = 0,row = 15)

ttk.Label(tab3,textvariable=rgtoken_status).grid(column = 0,row = 16)

rgtoken_mesg = Text(tab3,state="disabled", height=30, width=100, relief="sunken")
rgtoken_mesg.grid(column = 0,row = 17)

#Loop
#root.mainloop()


#Extra code for later

##Dynamic Windows resizing code
#for i in range(3):
#  tab2.columnconfigure(i, weight=1, minsize=75)
#   tab2.rowconfigure(i, weight=1, minsize=50)
