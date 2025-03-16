#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'isBalanced' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def isBalanced(s):
    # Write your code here
    yon = 'YES'
    b_list = list(s)
    
    print(b_list)
    
    left = 0
    right = len(b_list) - 1
    
    for i in range((len(b_list)//2)):
        if b_list[left] == b_list[right]:
            left += 1
            right -= 1
            yon = 'YES'
        else:
            return 'NO'
    
    #print(str((len(b_list)//2) - 1))
    #print(b_list[left])
    #print(b_list[right])
    return yon
    
    
if __name__ == '__main__':
    tmp = "{[()]}"
    result = isBalanced(tmp)
    print(result)

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        s = input()

        result = isBalanced(s)

        fptr.write(result + '\n')

    fptr.close()