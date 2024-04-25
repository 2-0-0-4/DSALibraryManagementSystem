import tkinter as tk
from tkinter import TclError, ttk
from LibrarySystem import * 
from TrieADT import *

book_trie = initialize_trie()
global root, username, borrowedbook, duedate


#resource used to learn tkinter module: https://www.pythontutorial.net/tkinter/

#This is the main file. This contains all functions to implement the GUI and their related helper functions

#----------HELPER FUNCTIONS------------
def change_availabilty(bookname,avail,due): 
    #O(n*m) where n = number of words in bookname and m = average length of word
    global book_trie
    #changes availability and duedate in trie
    keywords = bookname.split()
    for keyword in keywords: #iterates over all keywords in bookname
        keyword = keyword.lower()
        subtrie = book_trie
        for char in keyword: #traces out path of node in trie
            if char.isalpha():        
                subtrie = subtrie["Pointers"][ord(char.lower())-97]    
                if subtrie == None:
                    return False #node is not in trie

        if bookname in subtrie["data"] and subtrie["end_word"] == True: #changes flag to avail
            subtrie["data"][bookname.lower()][-2] = avail
            subtrie["data"][bookname.lower()][-1] = due 
    
def delete_handling(deleteframe, bookname:str): 
    #deletes the bookname from the csv file and trie and prints appropriate message
    global book_trie
    bookname = bookname.lower()
    output = remove_book(book_trie,bookname)
    if output == 1:
        delete_from_csv(bookname)
        output_label = tk.Label(deleteframe,text="Deleted!")
    elif output == 0: #book is borrowed so deletion is not possible
        output_label = tk.Label(deleteframe, text = "Book is borrowed. Try again later")
    else: #book is not found
        output_label = tk.Label(deleteframe, text = "Book not found.")
    output_label.pack()

def search_handling(searchframe,bookname:str):
    #calls display frame to display search results after searching in trie
    global book_trie
    search_results = search(book_trie,bookname)
    display_frame(searchframe,search_results)

def add_handling(frame,bookname,isbn,author,genre):
    #adds new book to csv file and trie
    add_node(book_trie,isbn,bookname,author,genre,True,None)
    add_to_csv(isbn,bookname,author,genre)
    message(frame,"Added Successfully")

def display_handling(frame):
    #calls the trie display operation that returns a dictionary of all data in trie
    #calls the display frame to display the data in the dictionary
    global book_trie
    books_lst = display(book_trie,{})
    display_frame(frame,books_lst)

def return_handling(frame):
    global username,borrowedbook,duedate,book_trie
    currentdate = calc_current_date()
    duedate = datetime.strptime(duedate, "%Y-%m-%d").date()
    if currentdate <= duedate: #book is being returned within due date
        change_availabilty(borrowedbook.lower(),True,None)
        output = borrow_return(borrowedbook,username.get(),"r")
        borrowedbook = ""
        duedate = None
        message(frame,"Book returned successfully!")
    else: #calculates fine and returns the book
        change_availabilty(borrowedbook.lower(),True,None)
        days, fine = calc_fine(currentdate,duedate)
        borrowedbook = ""
        duedate = None
        output = borrow_return(borrowedbook,username.get(),"r")
        message(frame,"Returned successfully! You returned the book " + str(days)+" days late.\n You have a fine of "+str(fine)+ "Rs. Please pay at the counter.")

def borrow_display(bookname:str,frame):
    #calls the display frame to display borrow buttons 
    global book_trie
    results = search(book_trie,bookname)
    display_frame(frame,results,"b")

def borrow_helper(frame,bookname):
    global username,borrowedbook,book_trie,duedate

    for widget in frame.winfo_children():
        widget.destroy()

    if borrowedbook == "": #user has no borrowed book under their name
        due = calc_due_date()
        output = borrow_return(bookname,username.get(),"b",due)
        if output == True:
            borrowedbook = bookname
            duedate = str(due)
            change_availabilty(borrowedbook.lower(),False,due)
            message(frame,"Borrowed successfully.\n Please return the book by: "+str(due))
        else:
            message(frame,"Error in borrowing the book. Please try again later.")

    else: #one book is already borrowed
        message(frame,"You have borrowed a book already.\n As per library policy, only one book is allowed.\n Please return '"+str(borrowedbook)+"' to borrow this book.")
    
    home_button = tk.Button(frame,text = "Home",command= lambda: user_frame(frame,root))
    home_button.pack()

def choose_frame(frame,pswd):
    #calls admin_frame is user is admin
    #calls user_frame if user is a member
    #checks password and gets user data: borrowedbook, duedate
    global root,username,borrowedbook,duedate
    flag, borrowedbook,duedate = pswd_check(username.get(),pswd)
    if flag == True:  
        if username.get() == "admin":
            admin_frame(frame,root)
        else:
            user_frame(frame,root)  
    else: #password is incorrect
        message(frame,"Error! Enter correct password")

def check_entry(entries):
    #takes an iterable of entries and checks if all fields are filled.
    #returns False if some field is empty
    flag = True
    for entry in entries:
        text = entry.get()
        flag = flag and text!="" 
    return flag

def message(frame,msg):
    #displays message on frame
    text_msg = tk.Label(frame,text=msg)
    text_msg.pack()

#-------------FRAMES----------------

def main_frame(root,frame = ""):
    #asks for username and pswd from user and calls choose_frame to display appropriate frame
    global username,book_trie

    if frame != "": #if main_frame is being called from a different frame(this is used when the user logs out.)
            for widget in frame.winfo_children():
                widget.destroy()  # Clear the main frame before raising another frame


    main = tk.Frame(root)
    main.place(relx=0.5, rely=0.5, anchor='center')

    username = tk.StringVar()
    pswd = tk.StringVar()

    user_label = tk.Label(main, text="Enter username: ")
    user_label.pack()

    user_entry = tk.Entry(main, textvariable=username)
    user_entry.pack()

    pswd_label = tk.Label(main, text="Enter Password: ")
    pswd_label.pack()

    pswd_entry = tk.Entry(main, textvariable=pswd, show="*")
    pswd_entry.pack()

    login_button = tk.Button(main, text="Login/SignUp", command=lambda: choose_frame(main, pswd.get()) if pswd.get() != "" and username.get() != "" else message(main,"Please fill all fields."))
    login_button.pack()

    exit_button = tk.Button(main,text='Quit program',command=lambda: root.quit())
    exit_button.pack()

    main.tkraise()

def admin_frame(frame, root):
    #displays all operations for library admin: add, delete, display, search
    for widget in frame.winfo_children():
        widget.destroy()  # Clear the main frame before raising another frame

    adminframe = tk.Frame(root)
    adminframe.place(relx=0.5, rely=0.5, anchor='center')

    add_oper = tk.Button(adminframe, text="Add books", command=lambda: add_frame(frame,root))
    add_oper.pack()

    delete_oper = tk.Button(adminframe, text="Delete books", command=lambda: delete_frame(adminframe,root))
    delete_oper.pack()

    search_oper = tk.Button(adminframe,text="Search books",command= lambda: search_frame(adminframe, root))
    search_oper.pack()

    display_oper = tk.Button(adminframe,text="Display All Books",command=lambda: display_handling(adminframe))
    display_oper.pack()

    logout_button = tk.Button(adminframe,text="Log out",command=lambda: main_frame(root,adminframe))
    logout_button.pack()

    adminframe.tkraise()

def user_frame(frame,root):
    #displays all operations for users: searching, displaying, borrowing, returning
    global book_trie
    for widget in frame.winfo_children():
        widget.destroy()

    userframe = tk.Frame(root)
    userframe.place(relx=0.5, rely=0.5, anchor='center')

    display_oper = tk.Button(userframe,text="Display All Books",command=lambda: display_handling(userframe))
    display_oper.pack()
    
    search_oper = tk.Button(userframe,text="Search books",command= lambda: search_frame(userframe, root))
    search_oper.pack()

    borrow_oper = tk.Button(userframe,text="Borrow a book",command=lambda: borrow_frame(userframe,root))
    borrow_oper.pack()
    
    return_oper = tk.Button(userframe,text="Return a book",command=lambda: return_frame(userframe))
    return_oper.pack()

    logout_button = tk.Button(userframe,text="Log out",command=lambda: main_frame(root,userframe))
    logout_button.pack()

def delete_frame(frame, root):
    #frame for delete operation
    for widget in frame.winfo_children():
        widget.destroy()  

    deleteframe = tk.Frame(root)
    deleteframe.place(relx=0.5, rely=0.5, anchor='center')

    bookname = tk.StringVar()
    delete_label = tk.Label(deleteframe, text="Enter book to be deleted: ")
    delete_label.pack()

    delete_entry = tk.Entry(deleteframe, textvariable=bookname)
    delete_entry.pack()

    # Assuming delete_book is a function that takes a string argument
    delete_button = tk.Button(deleteframe, text="Delete", command=lambda: delete_handling(deleteframe, bookname.get()))
    delete_button.pack()

    home_button = tk.Button(deleteframe,text = "Home",command= lambda: admin_frame(deleteframe,root))
    home_button.pack()

    deleteframe.tkraise()

def search_frame(frame,root):
    #frame for search operation
    for widget in frame.winfo_children(): #to clear the frame before adding another frame
        widget.destroy()  

    searchframe = tk.Frame(root)
    searchframe.place(relx=0.5, rely=0.5, anchor='center')

    bookname = tk.StringVar()
    search_label = tk.Label(searchframe, text= "Enter book to be searched: ")
    search_label.pack()

    search_entry = tk.Entry(searchframe, textvariable=bookname)
    search_entry.pack()

    search_button = tk.Button(searchframe, text="Search", command=lambda: search_handling(searchframe, bookname.get()))
    search_button.pack()

    home_button = tk.Button(searchframe,text = "Home",command= lambda: admin_frame(searchframe,root) if username.get() == "admin" else user_frame(searchframe,root))
    home_button.pack()

    searchframe.tkraise()
    
def add_frame(frame,root): 
    #for the add operation
    for widget in frame.winfo_children():
        widget.destroy()  
    
    addframe = tk.Frame(root)
    addframe.place(relx=0.5, rely=0.5, anchor='center')
    
    isbn = tk.StringVar()
    isbn_label = tk.Label(addframe, text= "Enter isbn of book: ")
    isbn_label.pack()
    isbn_entry = tk.Entry(addframe, textvariable= isbn)
    isbn_entry.pack()

    bookname = tk.StringVar()
    book_label = tk.Label(addframe, text= "Enter bookname: ")
    book_label.pack()
    book_entry = tk.Entry(addframe, textvariable= bookname)
    book_entry.pack()
    
    author = tk.StringVar()
    author_label = tk.Label(addframe, text= "Enter genre: ")
    author_label.pack()
    author_entry = tk.Entry(addframe, textvariable= author)
    author_entry.pack()
    
    genre = tk.StringVar()
    genre_label = tk.Label(addframe, text= "Enter author: ")
    genre_label.pack()
    genre_entry = tk.Entry(addframe, textvariable= genre)
    genre_entry.pack()
    #ensures all fields are filled then calls add_handling
    add_button = tk.Button(addframe, text="Add", command=lambda: add_handling(addframe,bookname.get(),isbn.get(),author.get(),genre.get()) if check_entry((bookname,isbn,author,genre)) else message(addframe,"Error! Fill all fields"))
    add_button.pack()

    home_button = tk.Button(addframe,text = "Home",command= lambda: admin_frame(addframe,root))
    home_button.pack()

def display_frame(frame, all_books,option=""):
    global username
    for widget in frame.winfo_children(): #empties all widgets on frame
        widget.destroy()
    #creates canvas on frame to place scroll bar
    canvas = tk.Canvas(frame, width=frame.winfo_width()+600)  
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    home_button = tk.Button(frame,text = "Home",command= lambda: admin_frame(frame,root) if username.get() == "admin" else user_frame(frame,root))
    home_button.pack()

    if all_books == {} or all_books == None or all_books == []: #there are no search results
        message(scrollable_frame,"No Books Found.")
    else:
        if type(all_books) == list: #searching returns bookdata of one book
                    
                number_label = tk.Label(frame,text=str(1)+" book found:")
                number_label.pack()

                book_data = all_books
                book_text = " | Available"
                available = book_data[-2]
                if available == False:
                    book_text = " | Borrowed"
                book_data = book_data[0:-2]
                book_text = " | ".join(book_data) + book_text
                data_label = tk.Label(scrollable_frame, text=book_text)
                data_label.pack()
                if option == "b" and available == True:
                    print(book_data[0])
                    borrowbutton = tk.Button(scrollable_frame,text="Borrow",command=lambda: borrow_helper(frame,book_data[0]))
                    borrowbutton.pack()
        else:   #searching returns a dictionary of data
            n = len(all_books)
            number_label = tk.Label(frame,text=str(n)+" books found:")
            number_label.pack()
            books_lst = [""]*n
            i = 0
            for key,book_data in all_books.items():
                book_text = "| Available"
                available = book_data[-2]
                if available == False:
                    book_text = "| Borrowed"
                book_data = book_data[0:-2]
                book_text = " | ".join(book_data) + book_text
                data_label = tk.Label(scrollable_frame, text=book_text)
                data_label.pack()
                #creates a list of book names to ensure every button corresponds to a different bookname (according to the display)
                books_lst[i] = book_data[0] 
                if option == "b" and available == True:
                    borrowbutton = tk.Button(scrollable_frame,text="Borrow",command=lambda i = i: borrow_helper(frame,books_lst[i]) if books_lst[i] != "" else message(frame,'Error!'))
                    borrowbutton.pack()
                i += 1
        

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
def borrow_frame(frame,root):
    #asks for input, searches and displays a borrow button
    for widget in frame.winfo_children():
        widget.destroy()

    borrowframe = tk.Frame(root)
    borrowframe.place(relx=0.5, rely=0.5, anchor='center')

    searchbook = tk.StringVar()
    
    search_label = tk.Label(borrowframe, text= "Enter book to be searched: ")
    search_label.pack()

    borrowentry = tk.Entry(borrowframe,textvariable=searchbook)
    borrowentry.pack()
    
    search_button = tk.Button(borrowframe,text="Search",command= lambda: borrow_display(searchbook.get(),borrowframe))
    search_button.pack()

    home_button = tk.Button(borrowframe,text = "Home",command= lambda: user_frame(borrowframe,root))
    home_button.pack()

    borrowframe.tkraise()

def return_frame(frame):
    #asks user if book needs to be returned and calls return_handling
    global username,borrowedbook,duedate
    for widget in frame.winfo_children():
        widget.destroy()
    
    returnframe = tk.Frame(root)
    returnframe.place(relx=0.5, rely=0.5, anchor='center')

    if borrowedbook != "":
        returnlabel = tk.Label(returnframe,text="Would you like to return: "+str(borrowedbook))
        returnlabel.pack()

        returnbutton = tk.Button(returnframe,text="Return",command=lambda : return_handling(returnframe))
        returnbutton.pack()
    else: #user has no books
        message(returnframe,"You have no borrowed books.")
    
    home_button = tk.Button(returnframe,text = "Home",command= lambda: user_frame(returnframe,root))
    home_button.pack()

    returnframe.tkraise()

def main():
    #creates the root window
    global root
    root = tk.Tk()
    root.title("Library System")
    root.geometry("800x600")

    main_frame(root)  

    root.mainloop()

main()
