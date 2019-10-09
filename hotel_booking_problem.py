import random

n_rooms = 3
sequence_len = 12
start_time = 20
end_time = 30
def gen_ai():
    # generate ai
    return int((end_time - start_time - 1) * random.random() + start_time)
	
def gen_pi():
    # generate pi
    return random.choice([2,3,4])

def gen_ti():
    # generate ti
    start_time = 12
    end_time = 24
    return int((end_time - start_time - 1) * random.random() + start_time)

def gen_seq(seq_len):
    # fault: can generate identical elements
    seq = []
    for i in range(seq_len):
        ai = gen_ai()
        pi = gen_pi()
        while ai + pi > 30:
            ai = gen_ai()
            pi = gen_pi()
        ti = gen_ti()
        while ti >= ai:
            ti = gen_ti()
        di = ai + pi
        seq.append((i,ti,ai,di,pi))
    seq = merge_sort(seq, lambda x: x[3])
    seq = merge_sort(seq, lambda x: x[2])
    seq = merge_sort(seq, lambda x: x[1])
    seq = [(i, seq[i][1], seq[i][2], seq[i][3], seq[i][4]) for i in range(len(seq))] 
    return seq
    
         

def merge(left,right, sort_by):
    # part of function merge_sort, return a list merged by 2 lists: left, right.
    sorted=[] #array to store the sorted list
    i,j=0,0
    while i<len(left) and j<len(right):
        if sort_by(left[i]) <= sort_by(right[j]):
            sorted.append(left[i])
            i+=1
        else:
            sorted.append(right[j])
            j+=1

    sorted+=left[i:]
    sorted+=right[j:]
    return sorted

def merge_sort(li, sort_by):
    # merge sort return a list sorted by the attribute whose index is sort_by
    "function to compute merge-sort"
    if len(li)==1:
        return li
    middle=len(li)//2
    left_li=merge_sort(li[:middle], sort_by)
    right_li=merge_sort(li[middle:], sort_by)
    return merge(left_li,right_li, sort_by)

def print_seq(seq):
    # print request sequence as a table
    print('ci\tti\tai\tdi\tpi')
    for i in seq:
        print('\t'.join([str(j) for j in i]))
    print()
    return
        
def first_fit(sigma_A, sigma_S, sigma_t, seq):
    sigma_t = merge_sort(sigma_t, lambda x: seq[x][3])
    sigma_t = merge_sort(sigma_t, lambda x: seq[x][2])
    accept_list = []
    for i in sigma_t:
        for j in range(n_rooms):
            collide = False
            occupied = sigma_A + accept_list
            occupied_j = [s for s in occupied if s[1] == j]
            for k in occupied_j:
                if not(seq[k[0]][2]>=seq[i][3] or seq[k[0]][3]<=seq[i][2]):
                    
                    collide = True 
            if not collide:
                accept_list.append((i,j))
                break 
            
    return accept_list 
    
def best_fit(sigma_A, sigma_S, sigma_t, seq):
    sigma_t = merge_sort(sigma_t, lambda x: -seq[x][3])
    sigma_t = merge_sort(sigma_t, lambda x: seq[x][2])
    
    accept_list = []
    for i in sigma_t:
        tmp_list = []
        found_ans = False
        for j in range(n_rooms):
            
            collide = False
            close_gap = False
            occupied = sigma_A + accept_list
            occupied_j = [s for s in occupied if s[1] == j]
            for k in occupied_j:
                if seq[k[0]][2]==seq[i][3] or seq[k[0]][3]==seq[i][2]:
                    close_gap = True
                if not(seq[k[0]][2]>=seq[i][3] or seq[k[0]][3]<=seq[i][2]):
                    collide = True 
            if not collide:
                if close_gap:
                    accept_list.append((i,j))
                    found_ans = True
                    break
                else:
                    tmp_list.append(j)
        if tmp_list and not found_ans:
            accept_list.append((i,tmp_list[0]))
    return accept_list 

def my_fit(sigma_A, sigma_S, sigma_t, seq):
    sigma_t = merge_sort(sigma_t, lambda x: -seq[x][3])
    sigma_t = merge_sort(sigma_t, lambda x: seq[x][2])
    
    accept_list = []
    for i in sigma_t:
        tmp_list = []
        
        occupied_space_list = []
        for j in range(n_rooms):
            
            collide = False
            occupied = sigma_A + accept_list
            occupied_j = [s for s in occupied if s[1] == j]
            
            occupied_space = 0
            for ci_ri in occupied_j:
                occupied_space += seq[ci_ri[0]][4]
            occupied_space_list.append(occupied_space)
            
            for k in occupied_j:
                if not(seq[k[0]][2]>=seq[i][3] or seq[k[0]][3]<=seq[i][2]):
                    collide = True 
            if not collide:
                tmp_list.append(j)
        if tmp_list:
            tmp_list = merge_sort(tmp_list, lambda ri: occupied_space_list[ri])
            accept_list.append((i,tmp_list[0]))
    return accept_list 

def hotel_booking(request_seq, algo):
    sigma_t = []
    sigma_A = []
    sigma_S = []
    ptr = 0
    while ptr < len(request_seq):
        head = request_seq[ptr]
        ptr += 1
        t = head[1]
        sigma_t.append(head[0])
        while ptr < len(request_seq) and head[1] == request_seq[ptr][1]:
            head = request_seq[ptr]
            ptr += 1
            sigma_t.append(head[0])
        
        accept_list = algo(sigma_A, sigma_S, sigma_t, request_seq)
        for i in accept_list: # i: (ID, ri)
            sigma_A.append(i)
        sigma_t = []
        for i in sigma_A:
            if t >= request_seq[i[0]][3]:
                sigma_A.remove(i)
                sigma_S.append(i)
    return sigma_A, sigma_S

def print_sigmas(sigma_A, sigma_S, n_rooms, seq):
    sigmas = sigma_A + sigma_S
    room_space = [["*" for i in range(end_time - start_time)] for j in range(n_rooms)]
    for i in sigmas:
        for j in range(seq[i[0]][2] - start_time, seq[i[0]][3] - start_time):
            room_space[i[1]][j] = i[0]
    
    title = [str(i) for i in range(start_time, end_time)]
    print("\t".join(title))
    for i in range(n_rooms):
        print("\t".join([str(j) for j in room_space[i]]))
    print()
    
    request_nights = 0
    for i in seq:
        request_nights += i[4]
    accepted_nights = 0
    for i in sigmas:
        accepted_nights += seq[i[0]][4]
    accepted_percentage = accepted_nights/request_nights * 100
    
    room_nights = (end_time - start_time) * n_rooms
    idle_percentage = (room_nights - accepted_nights)/room_nights * 100
    print("accepted nights\t\t" + "{0:.2f}".format(accepted_percentage) + "%")
    print("rejected nights\t\t" + "{0:.2f}".format(100 - accepted_percentage) + "%")
    print("idle nights\t\t" + "{0:.2f}".format(idle_percentage) + "%")
    print()
    return
    
    
   
print("generating request sequence randomly...")
request_seq = gen_seq(sequence_len) 
print("printing request sequence...")  
print_seq(request_seq)
# request_seq = [ [0,12,23,27,4],
                # [1,13,20,24,4],
                # [2,13,26,29,3],
                # [3,15,22,26,4],
                # [4,15,20,22,2],
                # [5,15,20,23,3],
                # [6,18,27,30,3],
                # [7,18,25,28,3],
                # [8,21,24,28,4],
                # [9,21,28,30,2],
                # [10,23,27,31,4],
                # [11,23,29,31,2]]
                

print("running first fit algorithm...")
sigma_A, sigma_S = hotel_booking(request_seq, first_fit)

print("printing summary of first fit...")
print_sigmas(sigma_A,sigma_S,n_rooms, request_seq)

print("running best fit algorithm...")
sigma_A, sigma_S = hotel_booking(request_seq, best_fit)

print("printing summary of best fit...")
print_sigmas(sigma_A,sigma_S,n_rooms, request_seq)

print("running my fit algorithm...")
sigma_A, sigma_S = hotel_booking(request_seq, my_fit)

print("printing summary of my fit...")
print_sigmas(sigma_A,sigma_S,n_rooms, request_seq)



