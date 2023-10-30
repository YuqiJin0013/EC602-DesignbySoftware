#!/usr/bin/env python
# Copyright 2023 Krishna Saharsh M mkrishna@bu.edu
# Copyright 2023 Yuqi Jin yuqijin8@bu.edu
# Copyright 2023 abhishek dhande abhi86@bu.edu

def swap_places(lst, ind):
    tmp = lst[ind]
    lst[ind] = lst[ind+1]
    lst[ind+1] = tmp
    val = ''.join(lst)

    return val

def swap_without_tail(guests_lst, guests_perms, len_of_original):
    swaps = len_of_original//2

    for i in range(len_of_original - 1):
        lst_for_swap_fn = []
        lst_for_swap_fn = lst_for_swap_fn + guests_lst
        tmp_lst = [] + lst_for_swap_fn

        swapped_val = swap_places(lst_for_swap_fn, i)
        guests_perms.append(swapped_val)

###################################################################

    for i in range(1, len_of_original):
        swapped_val_lst = list(guests_perms[i])

        for j in range(i+1, len_of_original - 1):
            svl = [] + swapped_val_lst
            swapped_val = swap_places(svl, j)
            guests_perms.append(swapped_val)

    num_of_perms = len(guests_perms)
    a = len_of_original
    b = len(guests_perms)

###################################################################

    for i in range(a, b):
        swapped_val_lst = list(guests_perms[i])

        val = 0

        for j in range(len_of_original):
            if(tmp_lst[j] != swapped_val_lst[j]):
                val = j

        for z in range(val+1, len_of_original - 1):
            svl = [] + swapped_val_lst
            swapped_val = swap_places(svl, z)
            guests_perms.append(swapped_val)
    
###################################################################

    for k in range(swaps-3):
        a = b
        b = len(guests_perms)
        for i in range(a, b):
            swapped_val_lst = list(guests_perms[i])
            val = 0

            for j in range(len_of_original):
                if(tmp_lst[j] != swapped_val_lst[j]):
                    val = j

            for z in range(val+1, len_of_original - 1):
                svl = [] + swapped_val_lst
                swapped_val = swap_places(svl, z)
                guests_perms.append(swapped_val)

    return guests_perms


class Wedding:
    def __init__(self):
        pass

    def shuffle(self, guests):
        original = guests
        orig_list = []
        orig_list.append(original)
        orig = list(original)
        orig_len = len(orig)
        
        incomp_list = []
        seating = []
        for i in range(1, len(orig) - 1):
            incomp_list.append(orig[i])
        seating.append(''.join(incomp_list))

        c1 = len(incomp_list)
        res1 = swap_without_tail(incomp_list, seating, c1)
        for i in range(len(res1)):
            res1[i] = orig[orig_len - 1] + res1[i] + orig[0]

        res2 = swap_without_tail(orig, orig_list, orig_len)
        for i in range(len(res1)):
            res2.append(res1[i])


        combi = []
        rotate_list = [] + orig
        starting_guest = orig[0]
        
        for i in range(orig_len - 1):
            rotate_list[i] = rotate_list[i+1]
        rotate_list[orig_len - 1] = starting_guest

        final = ''.join(rotate_list)
        combi.append(final)

        rotate_list = [] + orig
        starting_guest = rotate_list[orig_len - 1]

        for i in range(len(orig) - 1, 0, -1):
            rotate_list[i] = rotate_list[i-1]
        rotate_list[0] = starting_guest
        fin_str = ''.join(rotate_list)
        combi.append(fin_str)
            
        for j in range(len(combi)):
            res2.append(combi[j])
        if len(orig) == 2:
            res2.pop(2)
            res2.pop(2)
            res2.pop(2)
        return res2

        
    def barriers(self, guests, bars):
        original = guests
        orig = list(original)
        fin_res = []

        for i in range(len(bars)):
            bars[i] += i
            
        lin_list = []
        counter = 0

        for i in range(len(orig) + len(bars)):
            lin_list.append(0)

        for i in range(len(lin_list)):
            if i in bars:
                lin_list[i] = '|'
                counter += 1
            else:
                lin_list[i] = orig[i-counter]

        td_list = []
        for j in range(len(bars) + 1):
            td_list.append([])
        counter1 = 0
        for k in range(len(lin_list)):
            if lin_list[k] == '|':
                counter1 += 1
            else:
                td_list[counter1].append(lin_list[k])

        str_list = []
        for i in range(len(bars)+1):
            str_list.append([])
            
        for p in range(len(td_list)):  
            str_list[p].append(''.join(td_list[p]))
            tdlist_len = len(td_list[p])
            str_list[p] = swap_without_tail(td_list[p],str_list[p],tdlist_len)

        
        result = [[]]
        part1 = []
        for pool in str_list:
            tmp = []
            for x in result:
                for y in pool:
                    tmp.append(x+[y])
            result = tmp
            
        for i in range(len(result)):
          part1.append('|'.join(result[i]))
        fin_res.extend(part1)

        #Tail Arrange

        if bars[0] != 0:
            extra = td_list[0].pop(0)
            last_el_2d = td_list[len(td_list) - 1].pop(len(td_list[len(td_list) - 1]) - 1)

            str_list = []
            for i in range(len(bars)+1):
                str_list.append([])
                
            for p in range(len(td_list)):  
                str_list[p].append(''.join(td_list[p]))
                tdlist_len = len(td_list[p])
                str_list[p] = swap_without_tail(td_list[p],str_list[p],tdlist_len)

            result = [[]]
            part1 = []
            for pool in str_list:
                tmp = []
                for x in result:
                    for y in pool:
                        tmp.append(x+[y])
                result = tmp
                
            for i in range(len(result)):
              part1.append(last_el_2d + '|'.join(result[i]) + extra)
            fin_res.extend(part1)
        
        return fin_res
            
#######################################################################
def  show_result(v, partial=False,ind=None):
    v.sort()
    if not partial:
        print(len(v),"\n".join(v),sep="\n")
    else:
        print(len(v),v[ind],sep="\n")




def standard_tests():
    standard = Wedding()
    res = standard.shuffle("abc")
    show_result(res)

    res = standard.shuffle("WXYZ")
    show_result(res)

    res = standard.barriers("xyz", [0])
    show_result(res)

    res = standard.shuffle("abc")
    show_result(res)

    res = standard.shuffle("abcdefXY")
    show_result(res)

    res = standard.barriers("abcDEFxyz", [2, 5, 7])
    show_result(res)

    res = standard.barriers("ABCDef", [4])
    show_result(res)

    res = standard.barriers("bgywqa", [0, 1, 2, 4, 5])
    show_result(res)

    res = standard.barriers("n", [0])
    show_result(res)
    res = standard.shuffle("hi")
    show_result(res)



def main():

    print("""Type quit to exit.
Commands:
tests
s guests
b guests n barriers
sp guests ind
bp guests n barriers ind
""")
    w = Wedding()
    while True:
        asktype=input().split()
        if not asktype or asktype[0] == "quit":
            break;
        elif asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            r = w.shuffle(guests)
            show_result(r);
        elif asktype[0] == "b":
            guests,nbar,bars = asktype[1],asktype[2],asktype[3:]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r)
        elif asktype[0] == "sp":
            guests,ind = asktype[1:]
            r = w.shuffle(guests);
            show_result(r, True, int(ind));
        elif asktype[0] == "bp":
            guests,nbar,bars,ind  = asktype[1],asktype[2],asktype[3:-1],asktype[-1]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))
    

if __name__ == '__main__':
    main()