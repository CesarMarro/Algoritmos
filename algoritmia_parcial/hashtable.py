'''
HashTable implementation with chaining using linked lists.
'''

from pokemon import Pokemon

class Node:
    def __init__(self, data):
        """
        Inicializa el nodo con una instancia de Pokemon.
        """
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"

class LinkedList:
    
    def __init__(self):
        self.head = None

    def insert(self, data):
        """
        Inserta un nuevo nodo al inicio de la lista.

        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def find(self, key):
        """
        Busca un Pokemon por su nombre en la lista enlazada.
        """
        current = self.head
        while current:
            if current.data.nombre == key:
                return current.data
            current = current.next
        return None

    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current.data))
            current = current.next
        return " -> ".join(nodes) if nodes else "Empty"

class HashTable:

    def __init__(self, m=25):
        """
        Inicializa la tabla hash con m slots.
        """
        self.m = m
        self.table = [LinkedList() for _ in range(self.m)]

    def hash_function(self, key):
        """
        Función hash que mapea el nombre del Pokemon a un índice entre 0 y m-1.
        """
        # Se hace el hash con ascii y se utiliza el modulo 10
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.m

    def insert(self, pokemon):
        """
        Inserta una instancia de Pokemon en la tabla hash.

        """
        index = self.hash_function(pokemon.nombre)
        self.table[index].insert(pokemon)

    def search(self, key):
        """
        Busca un Pokemon por su nombre en la tabla hash.
        """
        index = self.hash_function(key)
        result = self.table[index].find(key)
        if result:
            return result
        else:
            print(f"{key} No se encuentra en el pokedex")
        return result

    def __repr__(self):
        representation = ""
        for i, linked_list in enumerate(self.table):
            representation += f"Slot {i}: {linked_list}\n"
        return representation
