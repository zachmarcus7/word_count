# Zach Marcus
# CS 261
# Assignment 5
# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import *

"""
This is the regular expression used to capture words.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word at a time and
    # put the word in `w`
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                current_word = w.lower()
                #get a count for current word
                current_count = ht.get(current_word)
                if current_count is None:
                    ht.put(current_word, 1)
                else:
                    ht.put(current_word, current_count + 1)

    #create an empty list to store top words in
    tuple_list = []

    #traverse hash_map to find most used words
    for i in range(ht.capacity):
        if ht._buckets[i] is not None:
            #traverse links at each bucket
            current = ht._buckets[i].head
            while current is not None:
                tuple_list.append((current.key, current.value))
                current = current.next

    #create an ordered list out of items
    iter_tuple_quick_sort(tuple_list, len(tuple_list) - 1, 0)

    #create a new list to return with passed number arg
    return_list = []
    list_counter = 0
    while list_counter <= number - 1:
        if list_counter == len(tuple_list) - 1:
            break
        else:
            return_list.append(tuple_list[list_counter])
            list_counter += 1

    return return_list


def tuple_partition(list, max, min):
    """
    Partitions a list around a pivot. The elements are compared by their second element
    and partitioned into descending order.

    Args:
        list: list to partition
        max: the max index in the list
        min: the minimum index in the list
    Returns:
        the index where the pivot ended up after the list was partitioned
    """
    #make the pivot the rightmost element in the list
    pivot = list[max]

    #start the index at the leftmost element
    pivot_index = min

    #make the current element the leftmost element
    current = min

    #iterate through list
    while current < max:
        #if current element is less than or equal to pivot
        #swap current element with index
        #then increment index
        if list[current][1] >= pivot[1]:
            temp = list[current]
            list[current] = list[pivot_index]
            list[pivot_index] = temp
            pivot_index += 1
        current += 1

    #put pivot into correct index
    temp = list[pivot_index]
    list[pivot_index] = list[max]
    list[max] = temp

    return pivot_index


def iter_tuple_quick_sort(list, max, min):
    """
    Sorts a tuple list in descending order, with the second element in each tuple as the
    element of comparison.

    Args:
        list: list to sort
        max: the max index in the list
        min: the minimum index in the list
    """
    #push min and max indices onto a stack
    stack = LinkedList()
    stack.push(min)
    stack.push(max)

    #keep pushing min and max indices onto stack to
    #iteratively sort those lists
    while not stack.is_empty():
        #pop the next min and max indices to partition
        max = stack.pop()
        min = stack.pop()

        #partition the list and find the next pivot
        pivot_index = tuple_partition(list, max, min)

        #if there's more than one element in the list
        #check if LHS needs to be partitioned
        if pivot_index - 1 >= min:
            stack.push(min)
            stack.push(pivot_index - 1)
        #check if RHS needs to be partitioned
        if pivot_index + 1 <= max:
            stack.push(pivot_index + 1)
            stack.push(max)

