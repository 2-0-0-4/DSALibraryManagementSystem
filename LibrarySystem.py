from TrieADT import *
import csv
from datetime import datetime,timedelta

# this file contains all functions used for csv file handling and duedate handling

def initialize_trie():
    #reads data from csv and makes trie (calls the addnode() function in TrieADT)
    #returns trie
    trie = create_node("","",False)
    file = open("BookData.csv")
    bookdata = csv.DictReader(file)
    for book in bookdata:
        isbn = book["ISBN"]
        title = book["BookName"]
        author = book["Author"]
        genre = book["Genre"]
        avail = book["Available"]
        duedate = book["DueDate"]
        if duedate == "":
            duedate = None
        else: 
            duedate = datetime.strptime(duedate, "%Y-%m-%d").date()
        if avail == "True":
            add_node(trie,isbn,title,author,genre,True,duedate)
        else:
            add_node(trie,isbn,title,author,genre,False,duedate)

    file.close()
    return trie

def pswd_check(user,pswd):
    #checks if username and pswd exist in Userdata.csv
    #returns True if user exists and pswd is correct
    #returns False if pswd is wrong
    #adds user to file if user does not exist in file (calls sign_up())
    file = open("UserData.csv")
    users = csv.DictReader(file)
    if pswd == "" or user == "":
        return False
    for user_dict in users:
        if user_dict["Username"] == user:
            if user_dict["Password"] == pswd:
                borrowedbook = user_dict["BorrowedBook"]
                duedate = user_dict["DueDate"]
                return True,borrowedbook,duedate  #password is correct
            else:
                return False,"","" 

    #user does not exist in file:
    return sign_up(user,pswd)

def sign_up(user,pswd):
    #when pswd and user do not exist in the csv file
    #this adds a new member to the library system
    file = open("UserData.csv","a",newline="\n")
    writer = csv.writer(file)
    writer.writerow([user, pswd,"",""])
    file.close()
    return True,"",""

def borrow_return(bookname,username,option,duedate=None): #"b" = borrow ,"r" means return
    #updates both csv files with relevant changes
    #changes availability and duedate in Bookdata.csv
    #changes borrowedbook and duedate in UserData.csv
    if option == "r": #return 
        change_book_data(bookname,"True","")
        update_user_data(username,"","")
    elif option == "b": #borrow
        change_book_data(bookname,"False",str(duedate))
        update_user_data(username,bookname,str(duedate))
    return True

def change_book_data(bookname,avail,due):
    #changes availability and due date of bookname in BookData.csv
    file1 = open("BookData.csv","r") 
    lines = file1.readlines() #list of all lines
    file1.close()
    file2 = open("BookData.csv","w") #to write updates to file
    for line in lines:
        lst = line.split(",")
        if lst[1].lower() == bookname.lower(): #makes changes to line
            lst[-1] = str(due)
            lst[-2]= avail
            line = ",".join(lst) + "\n"
        file2.write(line)
    file2.close()

def update_user_data(username,bookname,due):
    #changes borrowed book and due date of username in UserData.csv
    file1 = open("UserData.csv","r")
    lines = file1.readlines() #list of all rows
    file1.close()
    file2 = open("UserData.csv","w") #opens file in write mode to write updated list
    for line in lines:
        lst = line.split(",")
        if lst[0] == username: #updates the username row
            lst[-1] = str(due)
            lst[-2] = bookname
            line = ",".join(lst) + "\n"
        file2.write(line)
    file2.close()

def delete_from_csv(bookname): 
    #deletes a book from csv (deletes that specific line in BookData.csv)
    file1 = open("BookData.csv","r")
    lines = file1.readlines() #list of all lines in file
    file1.close()
    file2 = open("BookData.csv","w") #opens file again in write mode
    for line in lines:
        lst = line.split(",")
        if lst[1].lower() != bookname.lower(): #to avoid writing the line that needs to be deleted
            file2.write(line)
            
    file2.close()

def add_to_csv(isbn,bookname,author,genre): 
    #adds a book and its data to csv (sets Available flag to True and duedate to "")
    file = open("BookData.csv","a",newline="\n")
    writer = csv.writer(file)
    writer.writerow([isbn,bookname,author,genre,"True",""])
    file.close()

def calc_current_date():
    #returns current date
    date = datetime.now().date()
    return date

def calc_due_date():
    #calculates due date by adding 2 weeks to current date
    currentdate = calc_current_date()
    duedate = currentdate + timedelta(weeks = 2)
    return duedate

def calc_fine(date1:datetime.date,date2:datetime.date):
    #returns fine by multiplying 100 with the number of days between the duedate and returndate
    diff = date2 - date1
    days = abs(diff.days)
    return days, days * 100
