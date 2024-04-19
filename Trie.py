def create_node(data,end):
    node = {"data": data, "Pointers": [None]*26, "end_title": end}
    return node

#formula for ord(character) -97. all characters are to be in lowercase

def add_node(trie, isbn,title,author,genre,avail_flag): #O(h) where h is length of title
    subtrie = trie 
    for char_i in range(len(title)): #index of every character in title
        if title[char_i].isalpha():
            index = ord(title[char_i].lower()) - 97 #pointer index
            data = [title[char_i]]
            p = subtrie["Pointers"][index] 
            flag = False #to indicate end of title
            if char_i == len(title)-1: #for last character of title 
                flag = True 
                data = [title[char_i],title,isbn,author,genre,avail_flag]
            if p == None: #there is no node present in list of nodes
                subtrie["Pointers"][index] = create_node(data,flag)
                subtrie = subtrie["Pointers"][index] 
            else: #node is already present so iterate until title[char_i] is not present
                if flag == True:
                    subtrie["end_title"] = True
                    subtrie["data"] = data
                else:
                    subtrie = subtrie["Pointers"][index] 
    return trie

    

def delete(trie, del_val, length=0):
    if trie == None: #trie is empty or word does not exist
        return None

    if length == len(del_val): #reached the end of the del_val
        if trie["end_title"] == True: #end of word is reached
            trie["end_title"] = False 
            trie["data"] = trie["data"][0]
        if not any(trie["Pointers"]): #independent node, does not have any children
            return None
        return trie
    
    #calculating next index and calling the delete function on the next node
    index = ord(del_val[length]) - ord("a")
    trie["Pointers"][index] = delete(trie["Pointers"][index], del_val, length + 1)

    #if the node has no other children and is not the last node 
    if not any(trie["Pointers"]) and not trie["end_title"]: 
        return None
    return trie


def search(trie,search_val):   #O(n + m) where n is the number of nodes and m is the number of books

    # if trie["end_title"] == True and trie["Pointers"] == [None]*26: #end of word 
    #     if search_val in path_str:
    #             ret_lst.append(trie["data"])
                
    # else:
    #     if trie["end_title"] == True:
    #         if search_val in path_str:
    #             ret_lst.append(trie["data"])
               
    #     for i in range(26): #iterates over all pointers
    #         subtrie = trie["Pointers"][i] 
    #         if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
    #             path_str = path_str + subtrie["data"][0]
    #             search(subtrie,search_val,path_str,ret_lst)  
    #             path_str = ""
    lst = display(trie,[])
    ret_lst = []
    for element in lst:
        if search_val.lower() == element[0].lower() or search_val.lower() in element[0].lower():
            ret_lst.append(element)
    return ret_lst


        
def display(trie,ret_lst): #O(n) where n is the number of nodes in the trie

    if trie["end_title"] == True and trie["Pointers"]==[None]*26: #end of word 
        # print(trie["data"][1:])
        ret_lst.append(trie["data"][1:])
    else:
        if trie["end_title"] == True:
            ret_lst.append(trie["data"][1:])
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                display(subtrie,ret_lst)
    return ret_lst

# def add_node(trie, isbn,title,author,genre,avail_flag = True)
t = create_node("",False)
add_node(t,"978-0-7653-7990-8","The Lost World","Michael Crichton","Science Fiction",True)
add_node(t,"978-0-553-38276-3","The Catcher in the Rye","J.D. Salinger","Classic Literature",True)
add_node(t,"978-0-0000-0000-1","Burmese Days","George Orwell","Fiction",True)
add_node(t,"978-1-5247-9757-9","The Lord of the Rings","J.R.R. Tolkien","Fantasy",True)
add_node(t,"978-0-0000-0004-8","The Adventures of Huckleberry Finn","Mark Twain","Adventure",True)
add_node(t,"978-0-0000-0004-4","The Adventures of Tom Sawyer","Mark Twain","Adventure",True)
add_node(t,"978-0-0000-0004-8","The Road","Mark Twain","Adventure",True)
add_node(t,"978-0-0000-0007-7","Hamlet","William Shakespeare","Tragedy",True)
add_node(t,"978-0-0000-0007-7","Moby Dick","William Shakespeare","Tragedy",True)
add_node(t,"978-0-0000-0007-7","Moby","William Shakespeare","Tragedy",True)
add_node(t,"978-0-307-47607-1","Wild","Cheryl Strayed","Travel Memoir",True)
add_node(t,"978-1-4767-6603-8","Wild by Nature","Sarah Marquis","Adventure Memoir",True)

# searching:
lst = display(t,[])
for element in lst:
    print(element)
print("------searching------")
for i in range(5):
    search_val = input("enter search: ")
    print(search(t,search_val))

#deletion
# print("------deletion------")
# for i in range(5):
#     delval = str(input("enter value to be deleted: "))
#     delval = delval.replace(" ","")
#     delval= delval.lower()
#     delete(t,delval)
#     print("after deletion:")
#     lst = display(t,[])
#     for element in lst:
#         print(element)
