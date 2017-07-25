from Queue import Queue
import sys


#Simple implmentation of the fizzbuzz problem
def fizzBuzzPrint(list):
    for num in list:
        if num % 5 == 0 and num % 3 == 0:
            print "fizzbuzz"
        elif num % 5 == 0:
            print "buzz"
        elif num % 3 == 0:
            print "fizz"
        else:
            print ""
            
#Non looping method #1: Recursion
def fizzBuzzPrintRecursive(list,index):
    if(index >= len(list)): 
        return
    if list[index] % 5 == 0 and list[index] % 3 == 0:
        print "fizzbuzz"
    elif list[index] % 5 == 0:
        print "buzz"
    elif list[index] % 3 == 0:
        print "fizz"
    else:
        print ""
    fizzBuzzPrintRecursive(list,index + 1)
            
#Non looping method #2: Custom class to print "fizz", "buzz", "fizzbuzz" based on the index we are getting
class FizzBuzzList(list):
    def __getitem__(self, key):
        return list.__getitem__(self, key-1)
    
    def printAtIdx(self,key):
        item = list.__getitem__(self,key)
        if item % 5 == 0 and item % 3 == 0:
            print "fizzbuzz"
        elif item % 5 == 0:
            print "buzz"
        elif item % 3 == 0:
            print "fizz"
        else:
            print ""
            

def shortestSequenceFizzBuzz(input):
    
    #The lowest sequence starts at 3
    current_num = 0
    #The highest sequence we possibly go up to is 3 x 5 x size of the input list
    max_seq = 15 * len(input)
    start_sequence = 0
    
    smallest_start = 0
    smallest_end = sys.maxint
    
    window = []
    
    while start_sequence < max_seq:
        #Check to see if the window captures the input sequence
        match = sublist1(input,window)
        
        if match is True:
            if (current_num - start_sequence) < (smallest_end - smallest_start):
                smallest_start = start_sequence
                smallest_end = current_num
                
                #This is the smallest range possible
                if current_num - start_sequence == len(input) - 1:
                    break
            
            #We have what we need in this window lets to decrease our window size by incrementing our start sequence
            val = convertNumToFizzBuzz(start_sequence)
            if val is not None:
                window.pop(0)
                
            start_sequence += 1
            
        else:
            
            #Our current window does not contain the sequence so lets increase our window size
            current_num += 1
            
            if current_num >= max_seq: 
                break
            
            val = convertNumToFizzBuzz(current_num)
            if val is not None:
                window.append(val)
                
    if smallest_end == sys.maxint:
        return None
    else:
        return range(smallest_start,smallest_end + 1)
                
        
def sublist1(input, window):

    for i in range(0,len(window) - len(input) + 1):
        is_sublist = True
        for j in range(0,len(input)):
            if window[i + j] != input[j]:
                is_sublist = False
                break
         
        if is_sublist is True:
            return True
        
           
    return False
       
def convertNumToFizzBuzz(num):

    if num == 0:
        return None

    if num % 5 == 0 and num % 3 == 0:
        return "fizzbuzz"
    elif num % 5 == 0:
        return "buzz"
    elif num % 3 == 0:
        return "fizz"
    else:
        return None
            
if __name__ == "__main__":
    print "Normal iterative-----------"
    fizzBuzzPrint([3,10,22,32,10,15])
    print "Recursion -----------------"
    fizzBuzzPrintRecursive([3,10,22,32,10,15],0)
    print "Class implemtation---------"
    f_list = FizzBuzzList()
    f_list.extend([3,10,22,32,10,15])
    f_list.printAtIdx(0)
    f_list.printAtIdx(1)
    f_list.printAtIdx(5)
    
    print "Finding shortest sequence--"
    print shortestSequenceFizzBuzz(["fizz","fizzbuzz"])
