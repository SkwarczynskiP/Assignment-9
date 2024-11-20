# Question 1
# Complete this problem using the following observation and technique:
# - The problem can be modeled as a bipartite graph, where the valid seats are the vertices and the edges represent
#   being able to copy.
# - The goal of the problem is to compute a maximal independent set of the graph, i.e. the largest set of seats that
#   don't have an edge between them.
# - A set of vertices is an independent set if and only if its complement is a vertex cover, i.e. a set of vertices
#   such that every vertex on the graph is adjacent to one of the vertices in the set. A maximala independent set
#   corresponds to a minimal vertex cover.
# - By Konig's theorem, the number of vertices in a minimal vertex cover is the same as the number of edges in a maximum
#   matching.
# - You can use the Ford-Fulkerson method for computing a maximal flow to compute a maximum matching!

# Compute a maximal matching for the graph using the Ford-Fulkerson method (e.g. the Edmonds-Karp algorithm), and return
# the number of seats minus the size of the matching. Give the worst-case runtime of your algorithm.
# https://leetcode.com/problems/maximum-students-taking-exam/description/

class Solution:
    def maxStudents(self, seats: List[List[str]]) -> int:
        m, n = len(seats), len(seats[0])
        seats = [[0 if seats[i][j] == '.' else 1 for j in range(n)] for i in range(m)]
        adj = [[] for _ in range(m * n + 2)]
        for i in range(m):
            for j in range(n):
                if seats[i][j] == 0:
                    continue
                if (i + j) % 2 == 0:
                    adj[0].append(i * n + j + 1)
                    for dx, dy in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
                        x, y = i + dx, j + dy
                        if 0 <= x < m and 0 <= y < n and seats[x][y] == 1:
                            adj[i * n + j + 1].append(x * n + y + 1)
                else:
                    adj[i * n + j + 1].append(m * n + 1)
        def maxFlow():
            res = 0
            while True:
                prev = [-1] * (m * n + 2)
                q = [0]
                while q and prev[-1] == -1:
                    u = q.pop(0)
                    for v in adj[u]:
                        if prev[v] == -1 and v != 0 and v != m * n + 1:
                            prev[v] = u
                            q.append(v)
                if prev[-1] == -1:
                    break
                res += 1
                v = m * n + 1
                while v != 0:
                    u = prev[v]
                    adj[u].remove(v)
                    adj[v].append(u)
                    v = u
            return res
        return sum(seats[i][j] for i in range(m) for j in range(n)) - maxFlow()