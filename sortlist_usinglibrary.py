# -*- coding: utf-8 -*-


import re

def sort_mylist(list_strings):
    """ Main function that checks the type of string and categorise each string input in the list to a sublist. 
        Functions that sort diffent type of strings will take these sublist as arguments, returning a sorted 
        sublists which will be combined and returned to the user in a human readable format.

    Args:
        list_strings: List of different of strings.
        
    Returns:
        Returns the input string in human-friendly sorted order if it is not empty or None.

    """
    if (list_strings is None or len(list_strings)==0): 
        return None 

    if len(list_strings) == 1: #one string, no need to sort
        list_strings = list_strings[0].strip() # ["   "] or ["      23   "]=> ["23"] or ["\n"] 
        return list_strings

    (dates, numbers, alphanumeric, alpha, others) = check_string_type(list_strings) 

    sorted_numbers = sorted(numbers,key=float)      
    sorted_alpha = sorted(alpha, key=lambda s: s.lower())
    sorted_alphanumeric = sort_alphanumeric(alphanumeric) 
    sorted_dates = sorted(dates, key=lambda d: map(int, d.split('-')))
    sorted_others = sorted(others, key=unicode)

    sorted_strings = sorted_numbers + sorted_alpha + sorted_alphanumeric + sorted_dates + sorted_others

    return sorted_strings



def check_string_type(list_strings):
    """ Extracts different type of strings - numbers, alphabetic, alpanumeric, dates and other types from 
        the input list and appends to the appropriate category of sublist.

    Args:
        list_strings: List of different type of strings.
        
    Returns:
        Returns sublists of diffent type of strings.

    """
    dates = []
    numbers = []
    alpha = []
    alphanumeric = []
    versions =[]
    others =[]

    for s in list_strings:
        s =s.strip()
        if s=="" or s==None:
            continue  

        if re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', s): # only alphanumeric string mainly versions android1.2.3
            alphanumeric.append(s) 

        elif re.match(r'^[a-zA-Z]+$', s): #only alphabetical string
            alpha.append(s)
        
        elif re.match(r'^(\d{1,4})-((0[1-9]|1[0-2])|\d)-(\d{1,2})$', s):  #date in yyy-mm-dd format
            dates.append(s)

        elif re.match(r'^(-|\+*)([0-9]*\.?[0-9]*)$', s): #numbers
			s = float(s)
			numbers.append(s)
        else:
            others.append(s)

    return (dates, numbers, alphanumeric, alpha, others)        


def sort_alphanumeric(list_alphanums):
    """ Quicksort implementation that sorts alphanumeric strings like - android1.1.20 comes after andorid1.1.3
    Args:
        list_alphanums: List of alphanumeric strings eg. android2.3.1
        
    Returns:
        Returns a sorted list of alphanumeric strings

    """
    less = []
    equal = []
    greater = []

    if len(list_alphanums) > 1:
        pivotc = list_alphanums[0]
        matchp = re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', pivotc)
        u = (matchp.group(1)).lower()

        for x in list_alphanums:
            matchx = re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', x)
            w = (matchx.group(1)).lower()

            if w < u:
                less.append(x)
            elif w == u:
            	version_list=[]
            	version_list.append(matchx.group(2)) 
            	version_list.append(matchp.group(2))
         
                t = sorted(version_list, key=lambda s: map(int, s.split('.')))
    
                if t[0] == t[1]:
    	                equal.append(x)
                elif t[0] == matchx.group(2):
    	            	less.append(x)
                else:
    	                greater.append(x)
            elif w > u:
                greater.append(x)

        return sort_alphanumeric(less) + equal + sort_alphanumeric(greater)

    return list_alphanums

