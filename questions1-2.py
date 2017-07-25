from Queue import Queue
import StringIO
import sys
import unittest

#Simple implmentation of the fizzbuzz problem
def fizzBuzzPrint(list):
    for num in list:
        if num % 5 == 0 and num % 3 == 0:
            print "fizzbuzz"
        elif num % 5 == 0:
            print "buzz"
        elif num % 3 == 0:
            print "fizz"
            
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
            

"""
The implementation of this function to find the shortest possible fizz buzz sequence is to 
use the sliding window technique. The total fizzbuzz sequence happens every 15 integers so we can 
determine the maximum sequence number no matter what by multiplying the number of words in the input
list * 15. We always keep a list of what 'fizz','buzz','fizzbuzz' keywords are in the current window we are evaluating.

Run-time Complexity:
Due to my implemention of isSubList it's possible to be O(n^2) where n is the size of the input list

The psuedocode for the sliding window is as follows:
    var window as list
    while (the start of the window hasn't reached the max):
        if the input list is a sublist of our current window
            if current window size is smaller than our min window size
                set this window as our new min size window
                
                remove the first element our window if the start window index contains a keyword
                decrease our window size by moving our window start index by one
                
            else
                increase the window size and a keyword (if applicable) to our window
        
            
    return the smallest window we found that contained our input list
"""
def shortestSequenceFizzBuzz(input):
    
    current_num = 0
    #The highest sequence we possibly go up to is 3 x 5 x size of the input list
    max_seq = 15 * len(input)
    start_sequence = 0
    
    smallest_start = 0
    smallest_end = sys.maxint
    
    window = []
    
    while start_sequence < max_seq:
        #Check to see if the window captures the input sequence
        match = isSubList(input,window)
        
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
                
        
def isSubList(input, window):

    if input is None or window is None or len(input) == 0:
        return False

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
        
class TestMethods(unittest.TestCase):

    def test_fizzbuzz(self):
        capturedOutput = StringIO.StringIO()          
        sys.stdout = capturedOutput                   
        fizzBuzzPrint([3,10,22,32,10,15])
        self.assertEqual(capturedOutput.getvalue(), 'fizz\nbuzz\nbuzz\nfizzbuzz\n')
        sys.stdout = sys.__stdout__
        
    def test_fizzbuzz_recursive(self):
        capturedOutput = StringIO.StringIO()          
        sys.stdout = capturedOutput                   
        fizzBuzzPrintRecursive([3,10,22,32,10,15],0)
        self.assertEqual(capturedOutput.getvalue(), 'fizz\nbuzz\nbuzz\nfizzbuzz\n')
        sys.stdout = sys.__stdout__
        
    def test_fizzbuzz_class(self):
        capturedOutput = StringIO.StringIO()          
        sys.stdout = capturedOutput                   
        f_list = FizzBuzzList()
        f_list.extend([3,10,22,32,10,15])
        f_list.printAtIdx(0)
        f_list.printAtIdx(1)
        f_list.printAtIdx(4)
        f_list.printAtIdx(5)
        self.assertEqual(capturedOutput.getvalue(), 'fizz\nbuzz\nbuzz\nfizzbuzz\n')
        sys.stdout = sys.__stdout__
        
    def test_sublist(self):
        self.assertEqual(isSubList([1,2,3],[5,3,6,1,2,3,5,3,10]),True)
        self.assertEqual(isSubList([1,2,3,5,6],[5,3,6,1,2,3,5,3,10]),False)
        self.assertEqual(isSubList([],[5,3,6]),False)
        
    def test_fizzbuzz_lowest_sequence(self):
        self.assertEqual(shortestSequenceFizzBuzz(["fizz","buzz"]),[9,10])
        self.assertEqual(shortestSequenceFizzBuzz([]),None)
        self.assertEqual(shortestSequenceFizzBuzz(["fizz","buzz","fizz"]),[3,4,5,6])
        self.assertEqual(shortestSequenceFizzBuzz(["fizzbuzz","fizz"]),[15,16,17,18])
        self.assertEqual(shortestSequenceFizzBuzz(["fizz","fizz","buzz","buzz"]),None)
            
if __name__ == "__main__":
    unittest.main()
