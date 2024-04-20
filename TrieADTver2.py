def create_node(letter,data:dict,end):
    node = {"char": letter ,"data": data, "Pointers": [None]*26, "end_word": end}
    return node

#formula for ord(character) -97. all characters are to be in lowercase

def add_node(trie,isbn,title,author,genre,avail_flag): #O(h) where h is length of title
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
                    data = {title.lower():[title,isbn,author,genre,avail_flag]}
                if p == None: #there is no node present in list of nodes
                    subtrie["Pointers"][index] = create_node(letter,data,flag)
                    subtrie = subtrie["Pointers"][index] 
                else: #node is already present so iterate until title[char_i] is not present
                    subtrie = subtrie["Pointers"][index]
                    if flag == True:
                        subtrie["end_word"] = True
                        subtrie["data"][title.lower()] = [title,isbn,author,genre,avail_flag]
                    # else:
                        # subtrie = subtrie["Pointers"][index] 
    return trie

def delete(trie, del_val, length=0):
    if trie == None: #trie is empty or word does not exist
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
    search_lst = bookname.split()
    search_val = search_lst[0] 
    search_val = search_val.lower()
    subtrie = trie
    length = 0
    for char in search_val:
        length += 1
        # print(char)
        char_i = ord(char) - 97
        subtrie = subtrie["Pointers"][char_i]
        if subtrie["end_word"] == True and length == len(search_val): #data found
            if len(search_lst) > 1 and bookname.lower() in subtrie["data"]:
                return subtrie["data"][bookname.lower()]
            return subtrie["data"]
        if subtrie == None: #path cannot be traced
            return {}
          
def display(trie,ret_dict): #O(n) where n is the number of nodes in the trie

    if trie["end_word"] == True and trie["Pointers"]==[None]*26: #end of word 
        # print(trie["data"])
        # if trie["data"].keys() not in ret_lst.keys():
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
                subtrie["data"].pop(bookname)
                if subtrie["data"] == {}: #dictionary is empty there is no book with this keyword
                    delete(trie,keyword)
            if subtrie == None: #path cannot be traced
                return False
    return True
    

# t = create_node("","",False)
# # title = "The Lost World".split()
# # for word in title:
# add_node(t,"978-0-7653-7990-8","The Lost World","Michael Crichton","Science Fiction",True)
# add_node(t,"978-0-0000-0004-8","The Road","Mark Twain","Adventure",True)
# # print(t)
# add_node(t,"978-0-553-38276-3","The Catcher in the Rye","J.D. Salinger","Classic Literature",True)
# add_node(t,"978-0-0000-0000-1","Burmese Days","George Orwell","Fiction",True)
# add_node(t,"978-1-5247-9757-9","The Lord of the Rings","J.R.R. Tolkien","Fantasy",True)
# add_node(t,"978-0-0000-0004-8","The Adventures of Huckleberry Finn","Mark Twain","Adventure",True)
# add_node(t,"978-0-0000-0004-4","Mockingbird","Mark Twain","Adventure",True)
# add_node(t,"978-0-0000-0007-7","Mocking","William Shakespeare","Tragedy",True)
# add_node(t,"978-0-0000-0007-7","Moby Dick","William Shakespeare","Tragedy",True)
# add_node(t,"978-0-0000-0007-7","Moby","William Shakespeare","Tragedy",True)  
# add_node(t,"978-0-307-47607-1","Wild","Cheryl Strayed","Travel Memoir",True)
# add_node(t,"978-1-4767-6603-8","Wild by Nature","Sarah Marquis","Adventure Memoir",True)
# print(t)
# lst = display(t,{})
# for k,v in lst.items():
#     print(v)
# print("______________")
# print(search(t,"the"))
# print(search(t,"moby dick"))
# print(search(t,"mocking"))
# print(search(t,"mockingbird"))
# print(search(t,"wild by nature"))

# # remove_book(t,"moby")
# # remove_book(t,"moby dick")
# # print("------------------------")
# # lst = display(t,{})
# # for k,v in lst.items():
#     # print(v)
# # # print(t)
# # # print(t)
# # # print(search(t,"wild"))
# # # # searching:
# # # lst = display(t,{})
# # # for element in lst:
# # #     print(element)
# # # print("------searching------")
# # # for i in range(5):
# # #     search_val = input("enter search: ")
# # #     print(search(t,search_val))

# # # #deletion
# # # print("------deletion------")
# # # for i in range(5):
# # #     delval = str(input("enter value to be deleted: "))
# # #     delval = delval.replace(" ","")
# # #     delval= delval.lower()
# # #     delete(t,delval)
# # #     print("after deletion:")
# # #     lst = display(t,[])
# # #     for element in lst:
# # #         print(element)