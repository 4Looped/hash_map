# Description: Implementation of a hash map using separate chaining and associated functions.


from base_structures import (DynamicArray, LinkedList,
                             hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        """

        # Locate target index
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Insert if target index is empty
        if self._buckets[index].length() == 0:
            self._buckets[index].insert(key, value)
            self._size += 1

        # If not empty
        else:

            # Assume target key has not been seen and set pointer
            seen = False
            current_bucket = self._buckets[index]

            # Iterate through current bucket and update if seen
            for node in current_bucket:
                if node.key == key:
                    node.value = value
                    seen = True
                    break

            if seen == False:
                current_bucket.insert(key, value)
                self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        empty_count = 0

        for bucket in range(self._capacity):
            if self._buckets[bucket].length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        n = self._size
        m = self._capacity
        load_factor = n/m

        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """

        for bucket in range(self._capacity):
            self._buckets[bucket] = LinkedList()

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """

        # Create new capacity
        if new_capacity < 1:
            return
        else:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        # Create a new array
        new_array = DynamicArray()

        # Fill new array with linked lists
        for bucket in range(new_capacity):
            new_array.append(LinkedList())

        # Copy current elements and re-hash into new array
        for bucket in range(self._capacity):

            current_list = self._buckets[bucket]

            if current_list.length() != 0:

                for node in current_list:

                    new_hash = self._hash_function(node.key)
                    new_index = new_hash % new_capacity

                    new_array[new_index].insert(node.key, node.value)

        self._buckets = new_array
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].length() == 0:
            return None
        else:
            current_bucket = self._buckets[index]
            for node in current_bucket:
                if node.key == key:
                    return node.value
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].length() == 0:
            return False
        else:
            current_bucket = self._buckets[index]
            for node in current_bucket:
                if node.key == key:
                    return True
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """

        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].length() == 0:
            return
        else:
            current_bucket = self._buckets[index]
            check = current_bucket.remove(key)
            if check == True:
                self._size -= 1
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key / value pair stored in the hash map.
        """

        new_array = DynamicArray()

        for bucket in range(self._capacity):

            current_list = self._buckets[bucket]

            if current_list.length() != 0:

                for node in current_list:

                    pair = (node.key, node.value)

                    new_array.append(pair)

        return new_array

    def get_bucket(self, index):
        """Returns the bucket"""
        return self._buckets[index]


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array and returns a tuple containing a dynamic array with the mode, and its frequency.
    """

    # Create new hashmap and counter to track highest frequency
    map = HashMap()
    highest_count = 0

    # Cycle through input array, checking if key is already in the array - if so, update count; if not, add with a count of 1
    for element in range(da.length()):

        count = map.get(da[element])

        if count != None:
            count += 1
            map.put(da[element], count)
            if count > highest_count:
                highest_count = count

        else:
            map.put(da[element], 1)
            if highest_count < 1:
                highest_count = 1

            # Check load if adding a new element
            load = map.table_load()
            if load > 8:
                new_capacity = map.get_capacity()*2
                map.resize_table(new_capacity)

    # Create new array to hold modes
    mode_array = DynamicArray()

    # Add strings to new array if their value equals the highest frequency
    for element in range(map.get_capacity()):

        current_bucket = map.get_bucket(element)

        for node in current_bucket:

            if node.value == highest_count:
                mode_array.append(node.key)

    return (mode_array, highest_count)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
