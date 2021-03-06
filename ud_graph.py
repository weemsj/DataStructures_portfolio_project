# Course: CS261
# Author: Jacqueline Weems
# Assignment: Assignment 6
# Description: Undirected graphs

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        ed = self.adj_list[u]
        for val in ed:
            if val == v:
                return
        self.adj_list[u]+= v
        self.adj_list[v]+= u

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u not in self.adj_list or v not in self.adj_list:
            return
        ed = self.adj_list[u]
        for val in ed:
            if val == v:
                self.adj_list[v].remove(u)
                self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        incident = []
        if v not in self.adj_list:
            return
        else:
            for val in self.adj_list[v]:
                incident.append(val)
        for val in incident:
            self.remove_edge(val, v)
        del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        keys_a = self.get_vertices()
        keys_b = self.get_vertices()
        pairs = []
        if keys_a:

            for letter in keys_b:
                ed = self.adj_list[letter]
                for value in keys_a:
                    for item in ed:
                        if value == item:
                            if (letter,value) not in pairs and (value, letter) not in pairs:
                                pairs.append((letter, value))
        return pairs

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        ed = self.get_edges()
        vert = self.get_vertices()
        num = 0
        ind = num + 1
        if len(path) == 1:
            if path[num] in vert:
                return True
            return False
        while ind <= len(path) -1:
            start = path[num]
            nxt = path[ind]
            if (start, nxt) not in ed and (nxt, start) not in ed:
                return False
            num += 1
            ind += 1
        return True

    def dfs(self, v_start, v_end=None, visited=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_end not in self.adj_list:
            v_end = None

        if visited is None:
            visited = []

        if v_start not in self.adj_list:
            return visited
        visited.append(v_start)

        adj = self.adj_list[v_start]
        adj.sort()
        for nxt in adj:
            if nxt not in visited and v_end not in visited:
                self.dfs(nxt, v_end, visited)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """

        visited = []
        queue = [v_start]
        if v_start not in self.adj_list:
            return visited
        while queue and v_end not in visited:
            v = queue.pop(0)
            if v not in visited:
                visited.append(v)
                adj = self.adj_list[v]
                adj.sort()
                for x in adj:
                    if x not in visited:
                        queue.append(x)
        return visited

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        count = 0
        visited = []
        for vet in self.adj_list:
            if vet not in visited:
                visited += self.dfs(vet)
                count += 1
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        keys = self.adj_list.keys()
        for val in keys:
            if len(self.adj_list[val]) > 1:
                if self.rec_has_cycle(val):
                    return True
        return False

    def rec_has_cycle(self, v_start, parent=None,visited=None):

        if visited is None:
            visited = []
        visited.append(v_start)

        adj = self.adj_list[v_start]
        adj.sort()
        for nxt in adj:
            if nxt not in visited:
                if self.rec_has_cycle(nxt, v_start, visited):
                    return True
            elif nxt != parent:
                return True
        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())

    edges = ['FD', 'EK', 'EB', 'EJ', 'KB', 'JC', 'JG', 'CG', 'GB']
    g = UndirectedGraph(edges)
    print(g.has_cycle())