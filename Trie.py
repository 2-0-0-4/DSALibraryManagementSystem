def create_node(data,end):
    node = {"data": data, "Pointers": [None]*26, "end_title": end}
    return node

#formula for ord(character) -97. all characters are to be in lowercase

def add_node(trie, title,isbn,author,genre,avail_flag = True): #O(n) where n is length of title
    subtrie = trie 
    for char_i in range(len(title)): #index of every character in title
        if title[char_i].isalpha():
            index = ord(title[char_i]) - 97 #pointer index
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
                subtrie = subtrie["Pointers"][index] 
    return trie

def change_availabilty(trie,node,avail): 
    subtrie = trie
    for char in node: #traces out path of node in trie
        subtrie = subtrie["Pointers"][ord(char)-97]    
        if subtrie == None:
            return -1  #node is not in trie

    if subtrie["data"][1] == node and subtrie["end_title"] == True: #changes flag to avail
        subtrie["data"][-1] = avail 
        return 0
        
def delete(trie,node):
    node = trie.root
    nodes_stack = []
    for char in key:
        if char not in node.children:
                # Key not found, no deletion required
            return
        nodes_stack.append(node)
        node = node.children[char]

        # Mark the end of key
    node.is_end_of_word = False
    while len(nodes_stack) > 0:
        parent_node = nodes_stack.pop()
        if len(node.children) > 1 or node.is_end_of_word:
            return
        del parent_node.children[node.key]
        node = parent_node
    
def search(trie,search_val,path_str,ret_lst):   #O(n) where n is the number of nodes

    if trie["end_title"] == True and trie["Pointers"] == [None]*26: #end of word 
        if search_val in path_str:
                ret_lst.append(trie["data"])
                
    else:
        if trie["end_title"] == True:
            if path_str == search_val or search_val in path_str:
                ret_lst.append(trie["data"])
               
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                path_str = path_str + subtrie["data"][0]
                search(subtrie,search_val,path_str,ret_lst)  
                path_str = ""
        return ret_lst

        
def display(trie,ret_lst): #O(n) where n is the number of nodes in the trie
    if trie["end_title"] == True and trie["Pointers"]==[None]*26: #end of word 
        # print(trie["data"][1:])
        ret_lst.append(trie["data"][1:])
    else:
        if trie["end_title"] == True:
            # print(trie["data"][1:])
            ret_lst.append(trie["data"][1:])
        for i in range(26): #iterates over all pointers
            subtrie = trie["Pointers"][i] 
            if subtrie != None: #recursive call when subtrie exists (there is a path to be explored)
                display(subtrie,ret_lst)
    return ret_lst


t = create_node("",False)
add_node(t,"harry potter",4673460,"afeera","fiction")
add_node(t,"harry potter and the sorceres stone",4673460,"afeera","fiction")
add_node(t,"wonder",4673890,"umair","first one")
add_node(t,"wonders",4673890,"umair","second")
add_node(t,"alice",123456,"umair","mystery")
add_node(t,"kindness",123456,"umair","kind")
print(display(t,[]))
change_availabilty(t,"alice",False)
print(display(t,[]))
# add_node(t,"wonders",4673890,"umair","fiction")
# print(search(t,'harry potter',""))
# print(search(t,'alice'))
# print("------------------")
# print(search(t,"alice","",[]))
# print("------------------")
# print(search(t,'harry',"",[]))
# print("------------")
# print(search(t,'wonders',"",[]))
# print("------------")
# print(search(t,'wonder',"",[]))
# print("------------")
# print(search(t,'kind',"",[]))
# print(search(t,'and',"",[]))


# add_node(t,"qwertyuiopasdfghjklzxcvbnm,")
