#resource used to learn about tries: https://www.geeksforgeeks.org/introduction-to-trie-data-structure-and-algorithm-tutorials/

def create_node(letter,data:dict,end):
    node = {"char": letter ,"data": data, "Pointers": [None]*26, "end_word": end}
    return node
 
def add_node(trie,isbn,title,author,genre,avail_flag,due):
    #O(n) where n is length of title
    words = title.split()
    for keyword in words:
        subtrie = trie 
        for char_i in range(len(keyword)): #index of every character in title
            if keyword[char_i].isalpha():
                index = ord(keyword[char_i].lower()) - 97 #pointer index
                letter = keyword[char_i]
                p = subtrie["Pointers"][index] 
                flag = False #to indicate end of title
                data = {}
                if char_i == len(keyword)-1: #for last character of title 
                    flag = True 
                    data = {title.lower():[title,isbn,author,genre,avail_flag,due]}
                if p == None: #there is no node present in list of nodes
                    subtrie["Pointers"][index] = create_node(letter,data,flag)
                    subtrie = subtrie["Pointers"][index] 
                else: #node is already present so iterate until title[char_i] is not present
                    subtrie = subtrie["Pointers"][index]
                    if flag == True:
                        subtrie["end_word"] = True
                        subtrie["data"][title.lower()] = [title,isbn,author,genre,avail_flag,due]
                  
    return trie

def delete(trie, del_val, length=0):
    #O(m) where m is the number of characters in del_val
    if trie == None: #trie is empty or word does not exist(path was not traced)
        return None

    if length == len(del_val): #reached the end of the del_val
        if trie["end_word"] == True: #end of word is reached
            trie["end_word"] = False 
        if not any(trie["Pointers"]): #independent node, does not have any children
            return None
        return trie
    
    #calculating next index and calling the delete function on the next node
    index = ord(del_val[length]) - ord("a")
    trie["Pointers"][index] = delete(trie["Pointers"][index], del_val, length + 1)

    #if the node has no other children and is not the last node 
    if not any(trie["Pointers"]) and not trie["end_word"]: 
        return None
    return trie

def search(trie,bookname):   
    #O(h) where h is the average height of trie
    search_lst = bookname.split()
    search_val = search_lst[0] #first keyword of the bookname
    search_val = search_val.lower() 
    subtrie = trie
    length = 0
    for char in search_val: 
        length += 1
        char_i = ord(char) - 97
        subtrie = subtrie["Pointers"][char_i]
        if subtrie == None: #path cannot be traced
            return {}
        if subtrie["end_word"] == True and length == len(search_val): #data found
            #finds specific book in the dictionary if the bookname is more than one word(its not a keyword search)
            if len(search_lst) > 1 and bookname.lower() in subtrie["data"]: 
                return subtrie["data"][bookname.lower()]
            return subtrie["data"]
              
def display(trie,ret_dict): 
    #O(n) where n is the number of words in trie
    if trie["end_word"] == True and trie["Pointers"]==[None]*26: #end of word 
        ret_dict.update(trie["data"])
    else:
        if trie["end_word"] == True:
            ret_dict.update(trie["data"])
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                display(subtrie,ret_dict)
    return ret_dict

def remove_book(trie,bookname):
    #O(n*m) where n = number of words in bookname and m = average length of word
    #iterates over all keywords and removes bookname from their leafnode
    keywords = bookname.split()
    for keyword in keywords: 
        keyword = keyword.lower()
        subtrie = trie
        length = 0
        for char in keyword:
            length += 1
            # print(char)
            char_i = ord(char) - 97
            subtrie = subtrie["Pointers"][char_i]
            if subtrie["end_word"] == True and length == len(keyword): #data found
                if subtrie["data"][bookname][-2] == True: #book is in library
                    subtrie["data"].pop(bookname)
                    if subtrie["data"] == {}: #dictionary is empty there is no book with this keyword
                        delete(trie,keyword)
                else: #book is borrowed
                    return 0
            if subtrie == None: #path cannot be traced
                return -1
    return 1
