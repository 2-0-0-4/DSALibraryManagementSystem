from Trie import *


def initialize_trie(trie):
    #reads data from csv and makes trie (calls the addnode() function in TrieADT)
    #returns trie
    pass


#add relevant parameters if needed:
def pswd_check(user,pswd): #checks if username and pswd exist in Userdata.csv
    #returns True or False
    return True



def borrow_return(bookname,username,option): #"b" = borrow ,"r" means return
    #return True when borrowed/returned
    # changes the flag of the book(in csv and trie) and 
    #adds bookname in UserData csv file (under the book field for the relevant user)
    #to change flag in trie (use add_avalibaity func in Trie.py)
    pass

def delete_from_csv(): #deletes a book from csv
    pass

def add_to_csv(): #adds a book and its data to csv
    pass



#---------IGNORE
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
