#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 20:18:25 2021

@author: williamhou
"""

output = 1;
_input = int(input("What factorial do you want?"))
while(_input > 0):
    output *= _input
    _input -= 1   
print(output)

table = int(input("Which multiplication table do you want?"))
row = int(input("How many rows in the table?"))
i = 1
while(i <= row):
    print(str(table) + "*" + str(i) + "=" + str(table*i))
    i += 1
