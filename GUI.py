import tkinter as tk
from tkinter import TclError, ttk
from LibrarySystem import * #pswd check file reading and intilization of trie
from Trie import *
trie = initialize_trie({})


def choose_frame(frame,user, pswd):
    if pswd_check:  # Assuming pswd_check is a function that returns True or False
        if user == "admin":
            admin_frame(frame,root)
            print("admin")
        else:
            user_frame(frame,root)  # Assuming there's a user_frame function defined somewhere
            print("user")
    else:
        error = tk.Label(frame, text="Error! Incorrect password/username")
        error.pack()

def admin_frame(frame, root):
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

    logout_button = tk.Button(adminframe,text="Log out",command=lambda: root.quit())
    logout_button.pack()

    adminframe.tkraise()

def delete_frame(frame, root):

    for widget in frame.winfo_children():
        widget.destroy()  # Clear the main frame before raising another frame

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

def delete_handling(deleteframe, bookname):

    output = delete(trie, bookname)
    if output == True:
        output_label = tk.Label(deleteframe,text="Deleted!")
    else:
        output_label = tk.Label(deleteframe, text = "Book not found")
    output_label.pack()

def search_frame(frame,root):

    for widget in frame.winfo_children():
        widget.destroy()  # Clear the main frame before raising another frame

    searchframe = tk.Frame(root)
    searchframe.place(relx=0.5, rely=0.5, anchor='center')

    bookname = tk.StringVar()
    search_label = tk.Label(searchframe, text= "Enter book to be searched: ")
    search_label.pack()

    search_entry = tk.Entry(searchframe, textvariable=bookname)
    search_entry.pack()

    search_button = tk.Button(searchframe, text="Search", command=lambda: search_handling(searchframe, bookname.get()))
    search_button.pack()

    home_button = tk.Button(searchframe,text = "Home",command= lambda: admin_frame(searchframe,root))
    home_button.pack()

    searchframe.tkraise()

def search_handling(searchframe,bookname):
    
    values = search(trie,bookname,"",[])
    pass #prints all search thingies

def check_entry(entries):
    flag = True
    for entry in entries:
        text = entry.get()
        flag = flag and text!="" 
    return flag

def add_frame(frame,root): #called from adminframe only

    for widget in frame.winfo_children():
        widget.destroy()  # Clear the main frame before raising another frame
    
    addframe = tk.Frame(root)
    addframe.place(relx=0.5, rely=0.5, anchor='center')
    
    data = []
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

    add_button = tk.Button(addframe, text="Add", command=lambda: add_handling(addframe,bookname,isbn,author,genre) if check_entry((bookname,isbn,author,genre)) else message(addframe,"Error! Fill all fields"))
    add_button.pack()

    home_button = tk.Button(addframe,text = "Home",command= lambda: admin_frame(addframe,root))
    home_button.pack()

def message(frame,msg):
    text_msg = tk.Label(frame,text=msg)
    text_msg.pack()

def add_handling(frame,bookname,isbn,author,genre):
    data = [bookname.get(),isbn.get(),author.get(),genre.get()]
    print(data)

def main_frame(root,frame = ""):

    if frame != "":
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

    login_button = tk.Button(main, text="Login/SignUp", command=lambda: choose_frame(main,username.get(), pswd.get()))
    login_button.pack()

    exit_button = tk.Button(main,text='quit program',command=lambda: root.quit())
    exit_button.pack()

    main.tkraise()
     # Return the frame in case you need to reference it later

def user_frame(frame,root):

    for widget in frame.winfo_children():
        widget.destroy()

    userframe = tk.Frame(root)
    userframe.place(relx=0.5, rely=0.5, anchor='center')

    display_oper = tk.Button(userframe,text="Display All Books",command=lambda: display_handling(userframe,root))
    display_oper.pack()
    
    search_oper = tk.Button(userframe,text="Search books",command= lambda: search_frame(userframe, root))
    search_oper.pack()

    borrow_oper = tk.Button(userframe,text="Borrow a book:",command=lambda: borrow_frame(userframe,root))
    borrow_oper.pack()
    
    logout_button = tk.Button(userframe,text="Log out",command=lambda: root.quit())
    logout_button.pack()

def display_handling(frame,root):
    pass

def borrow_frame(frame,root):
    #asks for input, searches and displays a borrow button
    pass   

def borrow_handling(frame,root):
    pass

root = tk.Tk()
root.geometry("600x400")

main_frame(root)  

root.mainloop()
