# Description: Implementation of a hash map using open addressing and associated functions.


from base_structures import (DynamicArray, HashEntry,
                             hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Adds or updates an element in the hashmap.
        """

        # Check load
        if self.table_load() >= 0.5:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # Find initial index
        hash = self._hash_function(key)
        initial_index = hash % self.get_capacity()

        # Add if empty
        if self._buckets[initial_index] == None:
            self._buckets[initial_index] = HashEntry(key, value)
            self._size += 1

        # Add if tombstone
        elif self._buckets[initial_index].is_tombstone == True:
            self._buckets[initial_index] = HashEntry(key, value)
            self._size += 1

        # Update if key matches
        elif self._buckets[initial_index].key == key:
            self._buckets[initial_index].value = value

        # Else continue cycling through until key is found or None
        else:

            placed = False
            j = 1

            while placed == False:

                new_index = (initial_index + j**2) % self.get_capacity()

                if self._buckets[new_index] == None:
                    self._buckets[new_index] = HashEntry(key, value)
                    self._size += 1
                    placed = True

                elif self._buckets[new_index].is_tombstone == True:
                    self._buckets[new_index] = HashEntry(key, value)
                    self._size += 1
                    placed = True

                elif self._buckets[new_index].key == key:
                    self._buckets[new_index].value = value
                    placed = True

                else:
                    j += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        n = self._size
        m = self._capacity
        load_factor = n/m

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        empty = self.get_capacity() - self.get_size()

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """

        # Create new capacity
        if new_capacity < self.get_size():
            return
        else:
            if not self._is_prime(new_capacity):
                revised_capacity = self._next_prime(new_capacity)
            else:
                revised_capacity = new_capacity

        # Create a new map
        new_map = HashMap(revised_capacity, self._hash_function)

        # Copy current elements and re-hash into new array
        for bucket in range(self._capacity):

            current_hashentry = self._buckets[bucket]

            if current_hashentry != None:

                new_map.put(current_hashentry.key, current_hashentry.value)

        self._buckets = new_map.get_buckets()
        self._capacity = new_map.get_capacity()


    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        """

        # Find initial index
        hash = self._hash_function(key)
        initial_index = hash % self.get_capacity()

        # Return if None
        if self._buckets[initial_index] == None:
            return None

        # Return value if found
        elif self._buckets[initial_index].key == key and self._buckets[initial_index].is_tombstone == False:
            return self._buckets[initial_index].value

        # Else continue searching
        else:

            found = False
            j = 1

            while found == False:

                new_index = (initial_index + j**2) % self.get_capacity()

                if self._buckets[new_index] == None:
                    return None

                elif self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone == False:
                    return self._buckets[new_index].value

                else:
                    j += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """

        # Find initial index
        hash = self._hash_function(key)
        initial_index = hash % self.get_capacity()

        # Return if None
        if self._buckets[initial_index] == None:
            return False

        # Return if found
        elif self._buckets[initial_index].key == key and self._buckets[initial_index].is_tombstone == False:
            return True

        # Else continue searching
        else:

            found = False
            j = 1

            while found == False:

                new_index = (initial_index + j**2) % self.get_capacity()

                if self._buckets[new_index] == None:
                    return False

                elif self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone == False:
                    return True

                else:
                    j += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """

        # Find initial index
        hash = self._hash_function(key)
        initial_index = hash % self.get_capacity()

        # Return if not found
        if self._buckets[initial_index] == None:
            return

        # Remove if found
        elif self._buckets[initial_index].key == key and self._buckets[initial_index].is_tombstone == False:
            self._buckets[initial_index].is_tombstone = True
            self._size -= 1

        # Else continue searching
        else:

            found = False
            j = 1

            while found == False:

                new_index = (initial_index + j**2) % self.get_capacity()

                if self._buckets[new_index] == None:
                    return

                elif self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone == False:
                    self._buckets[new_index].is_tombstone = True
                    self._size -= 1
                    found = True

                else:
                    j += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """

        underlying_da = self.get_buckets()

        for bucket in range(self._capacity):
            underlying_da[bucket] = None

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        """

        output_array = DynamicArray()

        for bucket in range(self._capacity):

            element = self._buckets[bucket]

            if element != None:

                if element.is_tombstone == False:

                    output_array.append((element.key, element.value))

        return output_array


    def get_bucket(self, index):
        """Gets the bucket at an index."""
        return self._buckets[index]

    def get_buckets(self):
        """Returns the underlying DA."""
        return self._buckets


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
