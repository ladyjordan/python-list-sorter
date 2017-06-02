# -*- coding: utf-8 -*-

import re


def sort_strings(list_strings):
    """ Main function that checks the type of string and categorise each string in the input list to a sublist. 
        Functions that sort diffent type of strings will take these sublists as arguments, returning a sorted 
        sublists which will be combined and returned to the user in a human readable format.

    Args:
        list_strings: List of different type of strings.
        
    Returns:
        Returns the input string in human-friendly sorted order if it is not empty or None or has no whitespaces, tabs, newlines feeds.

    """

    if (list_strings is None or len(list_strings)==0): 
        return None 

    if len(list_strings) == 1: #one string, no need to sort
        list_strings = list_strings[0].strip() # ["   "] or ["      23   "]=> ["23"] or ["\n"] 
        return list_strings

    (numbers, alpha, alphanumeric, dates, others) = check_string_type(list_strings) 

    sorted_numbers = sort_entities(numbers, "numbers")
    sorted_alpha = sort_entities(alpha, "alpha")
    sorted_alphanumeric = sort_entities(alphanumeric, "alphanumeric")
    sorted_dates = sort_entities(dates, "dates")
    sorted_others = sorted(others,key=unicode)

    sorted_strings = sorted_numbers + sorted_alpha + sorted_alphanumeric + sorted_dates + sorted_others

    return sorted_strings


def sort_entities(entity, entity_type):
    """Handles the assignment of different entities to their respective sorting functions(decouples the codes)

    Args:
        entity: Sublist of string type that would be assigned to a specific sort function of entity type.
        entity_type: Defines the type of entity.

    Returns:
        Returns the sorted list for the entity list passed as the argument.

    """
    if entity_type=="numbers":
        return sort_numbers(entity)
    if entity_type=="alpha":
        return sort_alpha(entity)
    if entity_type=="alphanumeric":
        return sort_alphanumeric(entity)
    if entity_type=="dates":
        return sort_dates(entity)


def check_string_type(list_strings): 
    """Extracts the same type of strings(using regular expressions)from the list and adds to the specific sublist 
        - numbers, alpha, alphanumeric, dates and others

    Args:
        list_strings: Input list of differnt type of strings.

    Returns:
        Resturn the numbers, alpha, alphanumeric, date, others sublist

    """

    dates = []
    numbers = []
    alpha = []
    alphanumeric = []
    others =[]

    for s in list_strings:
        s =s.strip()  # input sanitization
        if s=="" or s==None:
            continue  

        if re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', s): #only alphanumeric string like versions "android1.2.3 or android2 extracted"
            alphanumeric.append(s) 

        elif re.match(r'^[a-zA-Z]+$', s): #only alphabetical string extracted
            alpha.append(s)
        
        elif re.match(r'^(\d{1,4})-((0[1-9]|1[0-2])|\d)-(\d{1,2})$', s):  #date in yyyy-mm-dd format
            ''' handles y-m-d format by appending 0'''
            dateobj = re.match(r'^(\d{1,4})-((0[1-9]|1[0-2])|\d)-(\d{1,2})$', s)
 
            yearf = format(int(dateobj.group(1)) ,'04d') #handles user input for year like y, yy, yyy by formatting (appending 0's and making it yyyy)
            monthf = format(int(dateobj.group(2)),'02d') #month formatted(0 appended if single digit)
            dayf = format(int(dateobj.group(4)), '02d') #date formatted(0 appened if single digit)

            date_str = str(yearf)+"-"+str(monthf)+"-"+str(dayf) #new formatted string appended
            dates.append(date_str)
           
        elif re.match(r'^(-|\+?)([0-9]*\.?[0-9]*)$', s): #numbers extracted, int and float
            numbers.append(s)

        else:
            others.append(s) #empty strings and other type of strings not handled above extracted here

    return (numbers, alpha, alphanumeric, dates, others)



def version_cmp(version1, version2):
    """Function that compares 2 versions(digit part) for order eg. android1.2.3 comes before android1.2.22 

    Args:
        version1: Version number eg. 1.1.10
        version2: Version number eg. 1.1.2

    Returns:
        Returns -1, 0 , 1 based on custom comparator.

    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
    return custom_comparator(normalize(version1), normalize(version2))



def custom_comparator(a,b):
    """Compares two arguments and defines an order.

    Args:
        a: a number 
        b: a number

    Returns:
        Returns -1, 0 , 1 based on sorting order.

    """
    if a > b:
        return 1
    if a == b:
        return 0 
    return -1



def sort_alphanumeric(list_alphanum):
    """Quicksort implementation that compares the first alphabetical part of two strings, if they are 
        equal, 2nd halves(version number)sent to version_cmp to compare and sort according to the custom 
        defined comparator. eg. android1.3 comes before android1.22

    Args:
        list_alphanum: List of alphanumeric strings

    Returns:
        Returns a sorted alphanumeric list of strings.

    """
    less = []
    equal = []
    greater = []

    if len(list_alphanum) > 1:
        pivotc = list_alphanum[0]
        matchp = re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', pivotc) 
        u = (matchp.group(1)).lower() # first half of pivot string

        for x in list_alphanum:
            matchx = re.match(r'^([a-zA-Z]+)(\d+(\.\d+)*)$', x)
            w = (matchx.group(1)).lower() # first half of string
            if w < u:
                less.append(x)
            elif w == u:
                t = version_cmp(matchp.group(2), matchx.group(2)) #if 1st alphabetical value matches, 2nd half sent to version comaparator
                if t == 1:
                    less.append(x)
                elif t == 0:
                    equal.append(x)
                elif t == -1:
                    greater.append(x)
            elif w > u:
                greater.append(x)

        return sort_alphanumeric(less) + equal + sort_alphanumeric(greater)

    return list_alphanum



def sort_numbers(list_nums):
    """Quicksort implementation of function to sort number strings.

    Args:
        list_nums: List of numbers.
        
    Returns:
        Returns a sorted list of numbers

    """
    less = []
    equal = []
    greater = []

    if len(list_nums) > 1:
        pivot = float(list_nums[0])
        for x in list_nums:
            w = float(x)
            if w < pivot:
                less.append(x)
            elif w == pivot:
                equal.append(x)
            elif w > pivot:
                greater.append(x)
        return sort_numbers(less) + equal + sort_numbers(greater)

    return list_nums



def sort_dates(list_dates):
    """Implementation of quicksort. Formats dates to integers and sort the integers to get chronological order.

    Args:
        list_dates: List of dates strings

    Returns:
        Returns sorted dates list

    """
    less = []
    equal = []
    greater = []

    if len(list_dates) > 1:
        pivot = int(list_dates[0].replace("-", ""))
        for p in list_dates:
            x = int(p.replace("-", ""))  
            if x < pivot:
                less.append(p)
            elif x == pivot:
                equal.append(p)
            elif x > pivot:
                greater.append(p)
        return sort_dates(less) + equal + sort_dates(greater)
   
    return list_dates


# quick sort for pure alphabetic string
def sort_alpha(list_alpha):
    """Quicksort implementation to sort alphabetic string lexicographically ignoring cases.

    Args:
        list_alpha: List of alphabetic strings

    Returns:
        Returns sorted list of alphabetic strings.

    """
    less = []
    equal = []
    greater = []

    if len(list_alpha) > 1:
        pivot = list_alpha[0].lower()
        for x in list_alpha:
            if x.lower() < pivot:
                less.append(x)
            elif x.lower() == pivot:
                equal.append(x)
            elif x.lower() > pivot:
                greater.append(x)
        return sort_alpha(less) + equal + sort_alpha(greater)

    return list_alpha


