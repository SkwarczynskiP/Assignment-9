# Question 1
# Complete this problem using the following observation and technique:
# - The problem can be modeled as a bipartite graph, where the valid seats are the vertices and the edges represent
#   being able to copy.
# - The goal of the problem is to compute a maximal independent set of the graph, i.e. the largest set of seats that
#   don't have an edge between them.
# - A set of vertices is an independent set if and only if its complement is a vertex cover, i.e. a set of vertices
#   such that every vertex on the graph is adjacent to one of the vertices in the set. A maximal independent set
#   corresponds to a minimal vertex cover.
# - By Konig's theorem, the number of vertices in a minimal vertex cover is the same as the number of edges in a maximum
#   matching.
# - You can use the Ford-Fulkerson method for computing a maximal flow to compute a maximum matching!

# Compute a maximal matching for the graph using the Ford-Fulkerson method (e.g. the Edmonds-Karp algorithm), and return
# the number of seats minus the size of the matching. Give the worst-case runtime of your algorithm.
# https://leetcode.com/problems/maximum-students-taking-exam/description/

from collections import deque
from typing import List

class Solution:
    def maxStudents(self, seats: List[List[str]]) -> int:
        rows, cols = len(seats), len(seats[0])
        graph = {}
        valid_seats = 0

        # Build the graph
        for i in range(rows):
            for j in range(cols):
                if seats[i][j] == '.':
                    valid_seats += 1
                    node = (i, j)
                    graph[node] = []

                    # Check possible cheating edges
                    for di, dj in [(0, 1), (1, -1), (1, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and seats[ni][nj] == '.':
                            graph[node].append((ni, nj))

        # Helper function for BFS in Ford-Fulkerson
        def bfs_match(match, visited):
            queue = deque()
            parent = {}
            for node in graph:
                if node not in match:
                    queue.append(node)
                    parent[node] = None

            found_augmenting_path = False
            while queue:
                current = queue.popleft()
                for neighbor in graph[current]:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)

                    pair = match.get(neighbor)
                    if pair is None:
                        # Found an augmenting path
                        found_augmenting_path = True
                        while current is not None:
                            match[neighbor] = current
                            match[current] = neighbor
                            neighbor, current = current, parent[current]
                        break
                    else:
                        # Continue BFS
                        parent[pair] = current
                        queue.append(pair)
                if found_augmenting_path:
                    break
            return found_augmenting_path

        # Max matching using augmenting path
        match = {}
        visited = set()
        while bfs_match(match, visited):
            visited.clear()

        # Return the result
        return valid_seats - len(match) // 2

        # m, n = len(seats), len(seats[0])
        # graph = [[0] * (m * n + 2) for _ in range(m * n + 2)]
        # source, sink = m * n, m * n + 1
        #
        # def add_edge(u, v, capacity):
        #     graph[u][v] = capacity
        #
        # def bfs(parent):
        #     visited = [False] * (m * n + 2)
        #     queue = deque([source])
        #     visited[source] = True
        #
        #     while queue:
        #         u = queue.popleft()
        #         for v in range(m * n + 2):
        #             if not visited[v] and graph[u][v] > 0:
        #                 queue.append(v)
        #                 visited[v] = True
        #                 parent[v] = u
        #                 if v == sink:
        #                     return True
        #     return False
        #
        # def ford_fulkerson():
        #     parent = [-1] * (m * n + 2)
        #     max_flow = 0
        #
        #     while bfs(parent):
        #         path_flow = float('Inf')
        #         s = sink
        #         while s != source:
        #             path_flow = min(path_flow, graph[parent[s]][s])
        #             s = parent[s]
        #
        #         v = sink
        #         while v != source:
        #             u = parent[v]
        #             graph[u][v] -= path_flow
        #             graph[v][u] += path_flow
        #             v = parent[v]
        #
        #         max_flow += path_flow
        #
        #     return max_flow
        #
        # for i in range(m):
        #     for j in range(n):
        #         if seats[i][j] == '.':
        #             if (i + j) % 2 == 0:
        #                 add_edge(source, i * n + j, 1)
        #                 for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        #                     ni, nj = i + di, j + dj
        #                     if 0 <= ni < m and 0 <= nj < n and seats[ni][nj] == '.':
        #                         add_edge(i * n + j, ni * n + nj, 1)
        #             else:
        #                 add_edge(i * n + j, sink, 1)
        #
        # max_matching = ford_fulkerson()
        # total_seats = sum(row.count('.') for row in seats)
        # return total_seats - max_matching

# Test the function with the given input
seats = [["#",".","#","#",".","#"],[".","#","#","#","#","."],["#",".","#","#",".","#"]]
solution = Solution()
output = solution.maxStudents(seats)
print(output) # Expected output: 4

seats = [[".","#"],["#","#"],["#","."],["#","#"],[".","#"]]
output = solution.maxStudents(seats)
print(output) # Expected output: 3

seats = [["#",".",".",".","#"],[".","#",".","#","."],[".",".","#",".","."],[".","#",".","#","."],["#",".",".",".","#"]]
output = solution.maxStudents(seats)
print(output) # Expected output: 10

# Works, but uses dynamic programming instead of Ford-Fulkerson
        # m, n = len(seats), len(seats[0])
        # dp = [[0] * (1 << n) for _ in range(m + 1)]
        #
        # def count_bits(x):
        #     return bin(x).count('1')
        #
        # def valid(row, mask):
        #     for i in range(n):
        #         if (mask & (1 << i)) and seats[row][i] == '#':
        #             return False
        #         if i > 0 and (mask & (1 << i)) and (mask & (1 << (i - 1))):
        #             return False
        #     return True
        #
        # for i in range(1, m + 1):
        #     for mask in range(1 << n):
        #         if not valid(i - 1, mask):
        #             continue
        #         for prev_mask in range(1 << n):
        #             if mask & (prev_mask << 1) or mask & (prev_mask >> 1):
        #                 continue
        #             dp[i][mask] = max(dp[i][mask], dp[i - 1][prev_mask] + count_bits(mask))
        #
        # return max(dp[m])