
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import matplotlib.pyplot as plt
import numpy as np, itertools
import pandas as pd
from tkinter import simpledialog
from tkinter import filedialog
import time

main = tkinter.Tk()
main.title("R-ECLAT TOOL") #designing main screen
main.geometry("400x250")

global eclat_time
global reclat_time

global filename
global num_rows
global password_login_entry
global username_login_entry

global username_verify
global password_verify

global tf1
global tf2
global minsup
global text
global counts

frequent_items = dict()

username_verify = StringVar()
password_verify = StringVar()

def upload():
    global filename
    global tf1
    filename = filedialog.askopenfilename(initialdir="dataset")
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");
    tf1.insert(END,filename)

def readDataset(filename):
    global num_rows
    transaction_data = {}
    transaction = 0
    transaction_items = []
    global num_rows
    f = open(filename, 'r', encoding="utf8") #connecting to dataset
    for row in f:  #looping all records from dataset
        if transaction > 0:
            arr = row.split(',') #separate all items from comma
            transaction_items.append(arr[0].strip()+","+arr[2].strip()) #read fish species and year 
            num_rows = num_rows + 1
        transaction = 1    
    f.close()
    transaction = 0
    for i in range(len(transaction_items)):
        transaction+=1
        for item in transaction_items[i].split(','):
            if item not in transaction_data:
                transaction_data[item] = set()
            transaction_data[item].add(transaction) #generate transaction from items sets
    return transaction_data
    

def runeclatAlgorithm(prefix_pattern, transaction_items):
    while transaction_items:
        item_name,count = transaction_items.pop()  #iterate or loop all items
        item_supp = len(count)
        if item_supp >= minsup: #check prefix support value and if greater than min support then start calculating suffix patterns 
            frequent_items[frozenset(prefix_pattern + [item_name])] = item_supp
            suffix_patterns = []
            for suffix_item, suffix_count in transaction_items: #start looping for suffix patterns available in prefix list
                support = count & suffix_count #get support for suffix items
                if len(support) >= minsup: #if suffix support > min support then form frequent patterns
                    suffix_patterns.append((suffix_item,support))
                    
            runeclatAlgorithm(prefix_pattern+[item_name], sorted(suffix_patterns, key=lambda item: len(item[1]), reverse=True))#recursive loop for all items check
            

def showFrequentItemsets(): #display all frequent items
    for item_name, support_value in frequent_items.items():
        text.insert(END,str(list(item_name))+" "+str(round(support_value,4))+"\n")


def eclatAlgorithm(): #run eclat algorithm
    start_time = time.time()
    global minsup
    global num_rows
    global eclat_time
    num_rows  = 0
    minsup = int(tf2.get()) #read min support value from user
    frequent_items.clear()
    text.delete('1.0', END)
    transaction_items = readDataset(filename) #function to read dataset values
    text.insert(END,'List of Frequent Items\n\n')
    runeclatAlgorithm([], sorted(transaction_items.items(), key=lambda item: len(item[1]), reverse=True))#call eclat algorithm to find frequent items
    text.insert(END,'Total Number of Transactions in dataset is  : '+str(num_rows)+'\n\n')
    text.insert(END,'Total Frequent Patterns Found in dataset is : '+str(len(frequent_items))+'\n\n')
    showFrequentItemsets()
    end_time = time.time()
    eclat_time = (end_time - start_time) * 100
    text.insert(END,'\nECLAT Execution Time : '+str(eclat_time))
    

def runreclatAlgorithm(prefix_pattern, transaction_items, num_rows): #reclat algorithm
    global counts
    while transaction_items:
        item_name,count = transaction_items.pop() #looping items
        item_support = len(count)
        if item_support >= minsup:  #checking item support count for prefix items
            suffix_patterns = []
            for suffix_item, suffix_count in transaction_items: #looping over suffix items ++item
                support = count & suffix_count
                minimum_support =  num_rows * (len(support)/num_rows) #calculating minimum support based on support values and transaction items %
                #if support < minimum support then conisder as infrequent items
                if len(support) <= minimum_support and (len(item_name) <= 4 or len(suffix_item) <= 4) and (len(item_name) > 4 or len(suffix_item) > 4):
                    text.insert(END,item_name+","+suffix_item+" : support count = "+str(len(support))+"\n")
                    counts = counts + 1
            #calling eclat recursively to get infrequentt items from list of items        
            runreclatAlgorithm(prefix_pattern+[item_name], sorted(suffix_patterns, key=lambda item: len(item[1]), reverse=True), num_rows)
    

def reclatAlgorithm():
    start_time = time.time()
    global minsup
    global num_rows
    global reclat_time
    global counts
    text.delete('1.0', END)
    counts = 0
    num_rows  = 0
    minsup = int(tf2.get()) #read min support value from user
    transaction_items = readDataset(filename) #function to read dataset values
    text.insert(END,'List of Infrequent Items using RECLAT Algorithm\n\n')
    runreclatAlgorithm([], sorted(transaction_items.items(), key=lambda item: len(item[1]), reverse=True),num_rows)#call eclat algorithm to find frequent items
    text.insert(END,'\nTotal Number of Transactions in dataset is  : '+str(num_rows)+'\n\n')
    text.insert(END,'Total Infrequent Patterns Found in dataset is : '+str(counts)+'\n\n')
    end_time = time.time()
    reclat_time = (end_time - start_time) * 100
    text.insert(END,'RECLAT Execution Time : '+str(reclat_time))

def graph():
    height = [eclat_time,reclat_time]
    bars = ('ECLAT Execution Time', 'R-ECLAT Execution Time')
    f, ax = plt.subplots(figsize=(5,5))
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    ax.legend(fontsize = 12)
    plt.show()

def reclatTool():
    global tf1
    global tf2
    global text
    newwin = Toplevel(main)
    newwin.config(bg='OliveDrab2')
    newwin.geometry("1300x1200")
    main.withdraw()
    font = ('times', 16, 'bold')
    title = Label(newwin, text='R-ECLAT TOOL')
    title.config(bg='LightGoldenrod1', fg='medium orchid')  
    title.config(font=font)           
    title.config(height=3, width=120)       
    title.place(x=0,y=5)

    font1 = ('times', 12, 'bold')
    text=Text(newwin,height=20,width=100)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=10,y=250)
    text.config(font=font1)


    font1 = ('times', 12, 'bold')
    
    l1 = Label(newwin, text='Upload Dataset')
    l1.config(font=font1)
    l1.place(x=50,y=100)

    tf1 = Entry(newwin,width=40)
    tf1.config(font=font1)
    tf1.place(x=200,y=100)

    uploadButton = Button(newwin, text="Browse", command=upload)
    uploadButton.place(x=550,y=100)
    uploadButton.config(font=font1)

    l2 = Label(newwin, text='Minimum Support')
    l2.config(font=font1)
    l2.place(x=50,y=150)

    tf2 = Entry(newwin,width=10)
    tf2.config(font=font1)
    tf2.place(x=200,y=150)

    eclatButton = Button(newwin, text="Run Eclat Frequent Items Algorithm", command=eclatAlgorithm)
    eclatButton.place(x=50,y=200)
    eclatButton.config(font=font1)

    reclatButton = Button(newwin, text="Run Reclat Infrequent Items Algorithm", command=reclatAlgorithm)
    reclatButton.place(x=330,y=200)
    reclatButton.config(font=font1)

    graphButton = Button(newwin, text="Execution Time Comparison Graph", command=graph)
    graphButton.place(x=640,y=200)
    graphButton.config(font=font1)


def login():
    global password_login_entry
    global username_login_entry
    username = username_verify.get()
    password = password_verify.get()

    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)    

    if username == 'admin' and password == 'admin':
       reclatTool()
    else:
       messagebox.showinfo("Invalid Login Details","Invalid Login Details")
    

font = ('times', 16, 'bold')
title = Label(main, text='Login Screen')
title.config(bg='LightGoldenrod1', fg='medium orchid')  
title.config(font=font)           
#title.config(height=3, width=120)       
title.place(x=80,y=5)

font1 = ('times', 12, 'bold')
l1 = Label(main, text="Username * ")
l1.place(x=10,y=50)
l1.config(font=font1)  
username_login_entry = Entry(main, textvariable=username_verify)
username_login_entry.place(x=130,y=50)

l2 = Label(main, text="Password * ")
l2.place(x=10,y=100)
l2.config(font=font1)  
password_login_entry = Entry(main, textvariable=password_verify, show= '*')
password_login_entry.place(x=130,y=100)



loginButton = Button(main, text="Login", command=login)
loginButton.place(x=80,y=150)
loginButton.config(font=font1)  


main.config(bg='OliveDrab2')
main.mainloop()
