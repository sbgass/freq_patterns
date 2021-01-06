#Apriori algorithm
def apriori(database, min_sup_count):
    #This is an implementation of the Apriori Algorithm
    #input: database is a list of transaction lists, e.g. [[a,b],[c,d]], 
	#and min_sup_count an int of the minimum support 
    #output: 2xn dimensional list of max patterns and thier support counts

    def first_scan(database):
        #input must be a list transation records of dimension 1 x n 
        Ck = [[],[]]

        for record in database:
            for value in record:
                #if Ck is empty 
                if not Ck[0]:
                    Ck[0].append(value)
                    Ck[1].append(1)
                else: 
                    #check to see if value is already found
                    for i in range(len(Ck[0])):
                        if value == Ck[0][i]:
                            Ck[1][i] += 1 
                            break 
                        #if we've looped to the end and it wasn't found, append as new value
                        if i == len(Ck[0])-1:
                            Ck[0].append(value)
                            Ck[1].append(1)
        return Ck

    def subset(r, c):
        #returns true if c is a subset of r 
        #both r and c are lists of strings 

        if not isinstance(r, list): 
            r = [r]

        for element in c:

            found = False 
            for attribute in r:
                if attribute == element:
                    found = True
                    break
            if not found:
                return False

        return True

    def scan_database(database, Ck):
        #input must be a list of dimensions 2 x n 
        #e.g. Ck = [[],[]]

        for record in database:
            for item_index in range(len(Ck[0])):
                if subset(record, Ck[0][item_index]):
                    Ck[1][item_index] += 1 

        return Ck

    def no_infrequent_subsets(cand, Lk):
        #cand is a list, Lk is a 2 by n list of frequent item sets 
        #return true if all subsets of cand are found in Lk 

        #for each k-1 subset of cand, check to make sure it was a freq_itemset
        for c in cand:
            sub_cand = cand.copy()
            sub_cand.remove(c) #this is k-1 subset 

            freq_found = False 
            for itemset in Lk[0]:
                if subset(itemset, sub_cand):
                    freq_found = True
                    break 

            if not freq_found:
                return False 

        return True 

    def gen_new_candidates(Lk):
        #input Lk is a list dimension 2 by n. index 0 is keys. Index 1 is values  
        #input is a full list of frequent item sets 
        #returns the next generation of candidate item sets through joining Lk item sets 
        import itertools

        Ck = [[],[]]

        #find new k from old Lk 
        k = len(Lk[0][0])+1

        for i in range(len(Lk[0])-1):
            for j in range(i+1, len(Lk[0])): 
                #join all combinations of freq items lists and then remove duplicates 
                if isinstance(Lk[0][i], list):
                    candidate_key = Lk[0][i] + Lk[0][j]
                else:
                    candidate_key = [Lk[0][i], Lk[0][j]]

                candidate_key = sorted(list(set(candidate_key))) #remove duplicate items in the list

                if len(candidate_key)> k:
                    candidate_list = list(itertools.combinations(candidate_key, k))
                    candidate_list = list(map(list, candidate_list))
                else:
                    candidate_list = [candidate_key]

                for sub_cand_key in candidate_list:
                    if no_infrequent_subsets(sub_cand_key, Lk):
                        if sub_cand_key not in Ck[0]:
                            Ck[0].append(sub_cand_key)
                            Ck[1].append(0)

        return Ck 

    def prune(Ck, min_count):
        #inputs candidate list and minimum support count intiger 
        #returns Lk which is populated with candidates that made the cut 

        Lk = [[],[]]
        for i in range(len(Ck[0])):
            if Ck[1][i] >= min_count:
                Lk[0].append(Ck[0][i])
                Lk[1].append(Ck[1][i])

        return Lk 

    #find initial support of each value
    Ck = first_scan(database)
    
    #when done counting, prune infrequent values from list
    Lk_plus = prune(Ck, min_sup_count)
    Lk = []
    
    #Begin process of C and L lists 
    while len(Lk_plus[0]) > 1:
        Lk = Lk_plus.copy()
        Ck = gen_new_candidates(Lk)
        
        #scan database for values in candidate list 
        Ck = scan_database(database, Ck)
        
        #make new Lk from candidatess > min_support 
        Lk_plus = prune(Ck, min_sup_count)
        
    if len(Lk_plus[0]) == 0:
        return Lk
    else:
        return Lk_plus

#___________________________________________________________________________
#FP-Growth
def fp_growth(db, min_support):
    #This is an implementation of the FP-Growht Algorithm
    #inputs: db is a list of transaction lists, e.g. [[a,b],[c,d]]
        #and min_support is an intiger representing the minimum support count 
    #output: 2xn dimensional list of max patterns and thier support counts

    def first_scan(database):
        #returns unordered frequent items list of dimension 2 by n 

        F = [[],[]]

        for record in database:
            for value in record:
                #if F is empty 
                if not F[0]:
                    F[0].append(value)
                    F[1].append(1)
                else: 
                    #check to see if value is already found
                    for i in range(len(F[0])):
                        if value == F[0][i]:
                            F[1][i] += 1 
                            break 
                        #if we've looped to the end and it wasn't found, append as new value
                        if i == len(F[0])-1:
                            F[0].append(value)
                            F[1].append(1)
        return F

    def prune(F, min_count):
        #inputs candidate list and minimum support count intiger 
        #returns L which is populated with candidates that made the cut 

        L = [[],[]]
        for i in range(len(F[0])):
            if F[1][i] >= min_count:
                L[0].append(F[0][i])
                L[1].append(F[1][i])

        return L 

    def sort_freq(L):
        #returns sorted input. Input is 2 by n list 
        #sorts descending order based on value in second list

        #bubble sort 
        for i in range(len(L[0])): 
            for j in range(0, len(L[0])-i-1): 
                if L[1][j] < L[1][j+1]: 
                    L[1][j], L[1][j+1] = L[1][j+1], L[1][j]
                    L[0][j], L[0][j+1] = L[0][j+1], L[0][j]

        return L

    def match_order(record, rubric):
        #sorts record in the order designated by 'rubric'
        #both inputs are lists
        #returns only elements in record that are in 'order'
        #returns a list 

        T = []
        for frq_item in rubric: 
            for item in record:
                if item == frq_item:
                    T.append(item)

        return T 


    def construct_fp_tree(database, min_sup_count):
        #find initial support of each value
        F = first_scan(database)

        #when done counting, prune infrequent values from list
        L = prune(F, min_sup_count)

        #order F list in descending 
        L = sort_freq(L)

        fp_tree = Tree()
        #start second loop through database
        for record in database:
            #first, sort record according to L 
            T = match_order(record, L[0])

            #build fp_tree
            fp_tree.insert_tree(fp_tree.root, T)

        return fp_tree
    class Tree_Node:
        def __init__(self, name, count = 0, parent = None, link = None):
            self.item_name = name
            self.count = count
            self.parent = parent
            self.link = link
            self.children = [] 

        def __str__(self, level=0):
            ret = "\t"*level+repr(self.item_name) + ':' + repr(self.count)+"\n"
            for child in self.children:
                ret += child.__str__(level+1)
            return ret

        def __repr__(self):
            return self.item_name

        def increment(self):
            self.count += 1 

        def insert_child(self, child_node):
            self.children.append(child_node)

        def make_link(self, to_node):
            self.link = to_node


    class Tree:
        def __init__(self, value = []):
            self.root = Tree_Node(value)
            self.header = {}

        def __repr__(self):
            return str(self.root)

        def get_child(self, parentnode, childname):
            #returns node if parent has a child with same name as childname
            #childname is a num or string matching self.item_name of a node
            #NOT RECURSIVE. just checking if in self.children

            for child in parentnode.children:
                if child.item_name == childname:
                    return child
            return False 

        def link_nodes(self, node):
            #updates self.header or link to existing node

            if node.item_name in self.header.keys():
                #then follow links until check_node.link == None 
                queued_node = self.header[node.item_name]
                while queued_node.link:
                    queued_node = queued_node.link
                queued_node.link = node 
            elif node.item_name:
                self.header[node.item_name] = node

        def insert_tree(self, parentnode, child):
            #child is ordered frequent item set list 

            if child:
                #if child[0] is in parentnode's children,
                childnode = self.get_child(parentnode, child[0])
                if childnode:
                    childnode.increment()
                    #next add the rest of the list to the tree
                    if len(child) > 1:
                        P = child[1:].copy()
                        self.insert_tree(childnode, P)
                else:
                    #else, add new child to tree
                    #Tree_Node(name, count, parent, link)
                    newtreenode = Tree_Node(child[0], 1, parentnode, None)
                    #and add it's children to the tree as well 
                    if len(child)> 1: 
                        P = child[1:].copy()
                        self.insert_tree(newtreenode, P)

                    parentnode.insert_child(newtreenode)
                    self.link_nodes(newtreenode)

    #This is the heart of the FP-Growth algorithm:
    #Defines and returns L (frequent patters above minimum support)
    def generate_combinations (condition_list, cond_support, trunk_elements = [[],[]]):
        #Updates L, frequent item sets from unions of alpha and beta 
        #alpha being the conditional list, beta being a [[A,B],[4,3]] of trunk items and thier supports 
        import itertools

        L_max = condition_list.copy()
        if trunk_elements[0]:
            L_max += trunk_elements[0]

        #find all combinations of all lists in trunk_elements[0] and join with alpha
        for n in range(2,len(L_max)+1):
            #return all combinations of array size n
            for combo in list(itertools.combinations(L_max, n)):

                #find the support of this comibination 
                #combination's support will be the minimum support of all the elements in the list
                item_support = []
                for element in combo:
                    if element in condition_list:
                        item_support.append(cond_support)
                    else:
                        #find it in trunk_elemetns
                        for i in range(len(trunk_elements[0])):
                            if element == trunk_elements[0][i]:
                                item_support.append(trunk_elements[1][i])
                                break

                #if this support is > min_support, add to L 
                combo_support = min(item_support)
                if combo_support >= min_support:
                    L[0].append(combo)
                    L[1].append(combo_support)

        #END of generate_combinations 
    
    def fp_growth_loop(parent_tree, alpha, alpha_sup):
        #support funciton 
        #Mining the fp_tree using the fp_growth algorithm 
        #
        
        #if there is single trunck left on the tree, capture elements and supports in a cond_L
        cond_L = [[],[]] 

        #Check for single trunk with no branching
        single_trunk = True 
        check_node = parent_tree.root #root is always an [] 

        #while children < 1 and haven't reach the last child, go to the next children
        while single_trunk and check_node.children:
            if len(check_node.children) > 1:
                #then we have branching in the tree 
                single_trunk = False
            else:
                check_node = check_node.children[0]
                #if the new check_node is already below min_support, you don't need to check any more children
                if check_node.count >= min_support: 
                    cond_L[0].append(check_node.item_name)
                    cond_L[1].append(check_node.count)
                else:
                    break
        
        #if tree contains only a single path, 
        #then form pattern base without looping through header 
        if single_trunk: 
            generate_combinations(alpha, alpha_sup, cond_L)

        else:
            #else, we have branching, and need to loop through header to form pattern base 

            #put header in list so we can loop in reverse order 
            header_list = [] 
            for item in parent_tree.header.keys():
                header_list.append(item) #by appending, we are making it reverse order

            for a in header_list:
                #loop through each link 
                cond_node = parent_tree.header[a]
                pattern_base = []
                beta = alpha.copy()
                beta.append(a)
                beta_sup = 0 #the sum of the supports of the conditional nodes (a)

                #for each link node 
                while True: 
                    beta_sup += cond_node.count

                    #find path to form patter base of the type {[A,B]:2}
                    path_head = cond_node
                    pattern_i = [] 

                    #stop forming patter when you get to your conditional pattern 
                    while path_head.parent:
                        pattern_i.append(path_head.item_name) 
                        path_head = path_head.parent
                    
                    #if there is a pattern to add
                    if pattern_i[1:]:
                        #add it to the pattern base n time, where n is the support of the conditional node 
                        for i in range(cond_node.count):
                            pattern_base.append(pattern_i[1:]) #removing the conditional from pattrn_i

                    #break while loop when at the end of the linked list 
                    if cond_node.link:
                         cond_node = cond_node.link
                    else:
                        break
                #END of While loop  

                if beta_sup >= min_support:
                    #Form beta-conditional FP_Trees out of patter base of frequent item sets. 
                    conditional_tree = Tree()

                    #build beta-conditional tree one branch at a time 
                    for item in pattern_base:
                        conditional_tree.insert_tree(conditional_tree.root, item)
                        
                    #recursively call growth algorithm now that you have beta (the condition) and conditional tree 
                    fp_growth_loop(conditional_tree, beta, beta_sup)
                else:
                    generate_combinations(beta, beta_sup)
        #END of fp_growth_loop 

    #Beginning of the FP-Growth MAIN function 
    #initial your output
    L = [[],[]]
    
    fp_tree = construct_fp_tree(db, min_support)
    fp_growth_loop(fp_tree, [], 0)
    
    #find the longest pattern in L and prune any that aren't as long 
    max_length = max(list(map(len, L[0])))
    for i in reversed(range(len(L[0]))):
        if len(L[0][i]) < max_length:
            L[0].pop(i)
            L[1].pop(i)
                     
    return L


    