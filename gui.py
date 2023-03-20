import tkinter as tk                    
from tkinter import ttk
  
  
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
tabControl.add(tab2, text ='Log Token Gen')
tabControl.add(tab3, text ='Resource Token Gen')
tabControl.pack(expand = 1, fill ="both")
  
ttk.Label(tab1,text ="Query Stuff").grid(
    column = 0, 
    row = 0,
    padx = 30,
    pady = 30)

ttk.Label(tab2,text ="Client ID").grid(column = 0,row = 0,sticky = "nw")
client_id=ttk.Entry(tab2, width=100).grid(column = 0,row = 1)

ttk.Label(tab2,text ="Tenant ID").grid(column = 0,row = 2)
tenant=ttk.Entry(tab2).grid(column = 0,row = 3)

ttk.Label(tab2,text ="Redirect URL").grid(column = 0,row = 4)
redirect_uri=ttk.Entry(tab2).grid(column = 0,row = 5)

ttk.Label(tab2,text ="API Endpoint").grid(column = 0,row = 6)
resource=ttk.Entry(tab2).grid(column = 0,row = 7)

ttk.Label(tab2,text ="Client Secret").grid(column = 0,row = 8)
client_secret=ttk.Entry(tab2).grid(column = 0,row = 9)

ttk.Button(tab2,text="Get Token").grid(column = 0,row = 11)



ttk.Label(tab3,text ="Resource Token Stuff").grid(
    column = 0,
    row = 0, 
    padx = 30,
    pady = 30)
  
root.mainloop()  
