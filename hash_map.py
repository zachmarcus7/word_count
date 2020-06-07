# Zach Marcus
# CS 261
# Assignment 5
# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0


    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1


    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False


    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None


    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


    """ 
    Stack Functions 
    """


    def push(self, data):
        """
        Adds a new node before the tail that contains data

        Args:
            data: The data the new node will contain
        """
        new_link = SLNode(0,0)  # initialize a new link
        new_link.data = data  # set new_link data

        #if list is empty
        if self.head is None:
            self.head = new_link
        else:
            current = self.head
            while current.next is not None:
                current = current.next

            new_link.next = current.next
            current.next = new_link


    def pop(self):
        """
        Removes the last element of the list and returns its value.
        """

       #check if list is empty
        if self.head is not None:
            current = self.head
            #check if only one element is on the list
            if current.next is None:
                item = self.head.data
                self.head = None
                return item
            else:
                while current.next is not None:
                    prev = current
                    current = current.next
                item = current.data
                prev.next = None
                return item


    def is_empty(self):
        """
        Checks if the list is empty

        Returns:
            True if the list has no nodes, False otherwise
        """

        if self.head is None:
            return True
        else:
            return False


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0


    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """

        #iterate through buckets
        for i in range(self.capacity):
            if self._buckets[i] is not None:
                self._buckets[i].head = None
                self._buckets[i].size = 0
        self.size = 0


    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        #find the index for passed key
        hash_key = (self._hash_function(key)) % self.capacity

        #check if bucket contains key
        if self._buckets[hash_key].contains(key) is not None:
            link = self._buckets[hash_key].contains(key)
            return link.value
        else:
            return None


    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        
        #create a new hash table
        new_table = HashMap(capacity, self._hash_function)

        #iterate through old hash map
        for i in range(self.capacity):
            current = self._buckets[i].head
            while current is not None:
                new_table.put(current.key, current.value)
                current = current.next

        self._buckets = []
        for i in range(new_table.capacity):
            self._buckets.append(new_table._buckets[i])
        self.capacity = capacity


    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: the key to use to hash the entry
            value: the value associated with the entry
        """

        #find an index for the hash key that fits inside the hash table
        hash_key = (self._hash_function(key)) % self.capacity

        #check if a link with given key already exists
        if self._buckets[hash_key].contains(key):
            self._buckets[hash_key].contains(key).value = value
        else:
            self._buckets[hash_key].add_front(key, value)
            self.size += 1


    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """

        #find the index for passed key
        hash_key = (self._hash_function(key)) % self.capacity

        #check if bucket contains key
        if self._buckets[hash_key].contains(key) is not None:
            link = self._buckets[hash_key].contains(key)
            self._buckets[hash_key].remove(key)
            self.size -= 1


    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        #find the index for passed key
        hash_key = (self._hash_function(key)) % self.capacity

        if self._buckets[hash_key].contains(key) is not None:
            return True
        else:
            return False


    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """

        total_buckets = 0

        #iterate through the buckets
        for bucket in self._buckets:
            if bucket.head is not None:
                total_buckets += 1

        return self.capacity - total_buckets


    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return self.size / self.capacity


    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
