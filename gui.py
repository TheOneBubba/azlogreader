import tkinter as tk                    
from tkinter import ttk
from tkinter import Text, Scrollbar
import time
  
  
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
    messages['state']='normal'
    msg="Ran a query at {dtg} it returned {X}".format(dtg=time.ctime(time.time()),X=10)
    messages.insert('end', msg)
    messages.insert('end', '\n')
    msg="Query Executed\n==========\n{Q}==========\n".format(Q=query.get('1.0','end'))
    messages.insert('end', msg)
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
    msg="Saved some place at {dtg}".format(dtg=time.ctime(time.time()))
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
client_id=ttk.Entry(tab2, width=100)
#Sets the column location of the object by referencing the variable saved to an object...
client_id.grid(column = 0,row = 2)

ttk.Label(tab2,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
#One line version; Creates object as variable and sets grid
#This object cannot be referenced post instantiation; tenant variable is <NoneType>
tenant=ttk.Entry(tab2, width=100).grid(column = 0,row = 4)

ttk.Label(tab2,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
redirect_uri=ttk.Entry(tab2, width=100).grid(column = 0,row = 6)

ttk.Label(tab2,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
resource=ttk.Combobox(tab2,width=50, values=('api.loganalytics.us', 'api.loganalytics.io'))
resource.grid(column = 0,row = 8, sticky="nw")

ttk.Label(tab2,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
client_secret=ttk.Entry(tab2, width=100)
client_secret.grid(column = 0,row = 10)

ttk.Button(tab2,text="Get Log Analytics API Token").grid(column = 0,row = 12)



#Tab 3 Resource Token Gen and variables
#This Should be a function...
#NYI just copied and pasted
ttk.Label(tab3,text ="Resource Graph Token Generator").grid(column = 0,row = 0)

ttk.Label(tab3,text ="Client ID").grid(column = 0,row = 1, sticky="nw")
client_id=ttk.Entry(tab3, width=100).grid(column = 0,row = 2)

ttk.Label(tab3,text ="Tenant ID").grid(column = 0,row = 3, sticky="nw")
tenant=ttk.Entry(tab3, width=100).grid(column = 0,row = 4)

ttk.Label(tab3,text ="Redirect URL").grid(column = 0,row = 5, sticky="nw")
redirect_uri=ttk.Entry(tab3, width=100).grid(column = 0,row = 6)

ttk.Label(tab3,text ="API Endpoint").grid(column = 0,row = 7, sticky="nw")
resource=ttk.Combobox(tab3,width=50, values=('management.azure.com', 'management.usgovcloudapi.net')).grid(
    column = 0,row = 8, sticky="nw")

ttk.Label(tab3,text ="Client Secret").grid(column = 0,row = 9, sticky="nw")
client_secret=ttk.Entry(tab3, width=100).grid(column = 0,row = 10)

ttk.Button(tab3,text="Get Resource Graph API Token").grid(column = 0,row = 12)

#Loop
root.mainloop()


#Extra code for later

##Dynamic Windows resizing code
#for i in range(3):
#  tab2.columnconfigure(i, weight=1, minsize=75)
#   tab2.rowconfigure(i, weight=1, minsize=50)
