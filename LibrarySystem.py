from TrieADT import *
import csv

def initialize_trie():
    #reads data from csv and makes trie (calls the addnode() function in TrieADT)
    #returns trie
    trie = create_node("",False)
    file = open("BookData.csv")
    bookdata = csv.DictReader(file)
    for book in bookdata:
        isbn = book["ISBN"]
        title = book["BookName"]
        author = book["Author"]
        genre = book["Genre"]
        avail = book["Available"]
        if avail == "True":
            add_node(trie,isbn,title,author,genre,True)
        else:
            add_node(trie,isbn,title,author,genre,False)

    file.close()
    return trie

# t = initialize_trie()
# lst = display(t,[])
# for i in lst:
#     print(i)
#     # print(type(i[-1]))
# print(len(lst))

def change_availabilty(trie,node,avail): 

    subtrie = trie
    for char in node: #traces out path of node in trie
        subtrie = subtrie["Pointers"][ord(char)-97]    
        if subtrie == None:
            return -1  #node is not in trie

    if subtrie["data"][1] == node and subtrie["end_title"] == True: #changes flag to avail
        subtrie["data"][-1] = avail 
        return 0


def pswd_check(user,pswd):
    #checks if username and pswd exist in Userdata.csv
    #returns True or False
    file = open("UserData.csv")
    users = csv.DictReader(file)
    for user_dict in users:
        if user_dict["Username"] == user and user_dict["Password"] == pswd:
            return True 
        
    return False

def borrow_return(bookname,username,option): #"b" = borrow ,"r" means return
    #return True when borrowed/returned
    # changes the flag of the book(in csv and trie) and 
    #adds bookname in UserData csv file (under the book field for the relevant user)
    #to change flag in trie (use change_avalibaity func in Trie.py)
    pass

def delete_from_csv(): 
    #deletes a book from csv
    pass

def add_to_csv(): 
    #adds a book and its data to csv
    pass



#---------IGNORE--------------
# def main():
#     option_login = input("Would you like to login(press 1) or would you like to sign up(press 2)")
#     if option_login == 1:
#         log_in()
#     elif option_login == 2:
#         sign_up()
#     else:
#         count = 1
#         while option_login != 1 or option_login != 2 and count < 3:
#             option_login = input("Error. Would you like to login(press 1) or would you like to sign up(press 2)")
#             count += 1
    


# def search_book(bookname):
#     global trie
#     search_results = search(trie,bookname,"",[])
#     for book in search_results:
#         print('Book Name: ',book[0] ,end = " ")
#         print('ISBN: ',book[1] ,end = " ")
#         print('Author: ',book[2] ,end = " ")
#         print("Genre: ", book[3],end = " ")
#         print("Available: ", book[4],end = " ")
#         print("------------------")

# def delete_book(bookname):
#     global trie

#     print("deleting")
