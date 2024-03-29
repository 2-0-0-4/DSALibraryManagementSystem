def create_node(data,end):
    node = {"data": data, "Pointers": [None]*26, "end_title": end}
    return node

#formula for ord(character) -97. all characters are to be in lowercase

def add_node(trie, title,isbn,author,genre): #to add node to Trie O(n)
    subtrie = trie 
    for char_i in range(len(title)): #index of every character in title
        if title[char_i].isalpha():
            index = ord(title[char_i]) - 97 #pointer index
            data = [title[char_i]]
            p = subtrie["Pointers"][index] #element in pointers at n position of node pointers
            flag = False #to indicate end of title
            if char_i == len(title)-1: #for last character of title 
                flag = True 
                data = [title[char_i],title,isbn,author,genre]
            if p == None: #there is no node present in list of nodes
                subtrie["Pointers"][index] = create_node(data,flag)
                subtrie = subtrie["Pointers"][index] #assigns new subtrie to subtrie variable
            else: #node is already present so iterate until title[n] is not present
                subtrie = subtrie["Pointers"][index] 
    return trie

def search(trie,search_val,path_str,ret_lst):     
    if trie["end_title"] == True and trie["Pointers"] == [None]*26: #end of word 
        if search_val in path_str:
                ret_lst.append(trie["data"])
                

    else:
        if trie["end_title"] == True:
            if path_str == search_val or search_val in path_str:
                ret_lst.append(trie["data"])
               
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] #saves subtrie 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                path_str = path_str + subtrie["data"][0]
                search(subtrie,search_val,path_str,ret_lst)  
                path_str = ""
        return ret_lst

        



def display(trie):
    if trie["end_title"] == True and trie["Pointers"]==[None]*26: #end of word 
        print(trie["data"][1:])
    else:
        if trie["end_title"] == True:
            print(trie["data"][1:])
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] #saves subtrie 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                display(subtrie)


t = create_node("",False)
add_node(t,"harry potter",4673460,"afeera","fiction")
add_node(t,"harry potter and the sorceres stone",4673460,"afeera","fiction")
add_node(t,"wonder",4673890,"umair","first one")
add_node(t,"wonders",4673890,"umair","second")
add_node(t,"alice",123456,"umair","mystery")
add_node(t,"kindness",123456,"umair","kind")
# add_node(t,"wonders",4673890,"umair","fiction")
# print(search(t,'harry potter',""))
# print(search(t,'alice'))
print("------------------")
print(search(t,"alice","",[]))
print("------------------")
print(search(t,'harrypotterandthesorceresstone',"",[]))
print("------------")
print(search(t,'wonders',"",[]))
print("------------")
print(search(t,'wonder',"",[]))
print("------------")
print(search(t,'kind',"",[]))
print(search(t,'and',"",[]))

# add_node(t,"qwertyuiopasdfghjklzxcvbnm,")
