# -*- coding: utf-8 -*-
'''
==========
UNIT TESTS
==========
'''

import unittest
from sortlist_main import sort_alphanumeric, sort_numbers, sort_alpha, sort_dates

class SortListTestCase(unittest.TestCase):

    def test_if_all_numbers_are_sorted_ascending_order(self):
        
        self.assertEqual(sort_numbers(["11","0.0000009","-2.78","0","-03.0"]),["-03.0","-2.78","0","0.0000009","11"])


    def test_if_negative_floats_are_sorted(self):
  
        self.assertEqual(sort_numbers(["-2.78","-03.0"]),["-03.0","-2.78"])


    def test_if_alpabetical_strings_are_sorted_lexicographically(self):
        
        self.assertEqual(sort_alpha(["Orange","watermelon","nectrine","apple"]),["apple","nectrine","Orange","watermelon"]) 


    def test_if_alpabetical_strings_are_sorted_lexicographically_and_case_ignored(self):
        
        self.assertEqual(sort_alpha(["Watermelon","mango","Mango","tomato","apple"]),["apple","mango","Mango","tomato","Watermelon"]) 


    def test_if_alphanumeric_versions_are_sorted(self):
        
    	self.assertEqual(sort_alphanumeric(["iOS2.1.66","iOS2.1.7"]),["iOS2.1.7","iOS2.1.66"])


    def test_if_dates_are_sorted_chronologically(self):
    	'''are dates in yyyy-m-d format sorted correctly?'''
        
        self.assertEqual(sort_dates(["2013-01-01","2012-12-31","1988-2-2"]),["1988-2-2","2012-12-31","2013-01-01"])

   

if __name__ == '__main__':
    unittest.main()



