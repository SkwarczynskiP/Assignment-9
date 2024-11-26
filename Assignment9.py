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

class Solution:
    def maxStudents(self, seats: List[List[str]]) -> int:
        rows, columns = len(seats), len(seats[0])
        graph = {}
        validSeats = 0

        # Building the graph
        for i in range(rows):
            for j in range(columns):
                if seats[i][j] == '.':
                    validSeats += 1

                    node = (i, j)
                    graph[node] = []

                    # Add edges to the left, right, and diagonals if the seat is valid
                    for di, dj in [(0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
                        ni, nj = i + di, j + dj

                        if 0 <= ni < rows and 0 <= nj < columns and seats[ni][nj] == '.':
                            graph[node].append((ni, nj))

        def bfs_match(match, visited):  # Helper function for BFS in Ford-Fulkerson
            queue = deque()
            parent = {}

            # Initialize the queue with nodes not in the matching
            for point in graph:
                if point not in match:
                    queue.append(point)
                    parent[point] = None

            foundAugmentingPath = False  # Flag to indicate if an augmenting path is found

            while queue:  # BFS
                current = queue.popleft()

                for neighbor in graph[current]:  # Iterate over the neighbors
                    if neighbor in visited:  # Skip visited nodes
                        continue

                    visited.add(neighbor)  # Mark the node as visited
                    pair = match.get(neighbor)  # Get the pair of the neighbor

                    if pair is None:  # Found an augmenting path
                        foundAugmentingPath = True  # Set the flag

                        while current is not None:  # Update the matching
                            match[neighbor] = current
                            match[current] = neighbor
                            neighbor, current = current, parent[current]
                        break

                    else:  # Continue the BFS
                        parent[pair] = current
                        queue.append(pair)

                if foundAugmentingPath:
                    break

            return foundAugmentingPath

        match = {}
        visited = set()

        while bfs_match(match, visited):  # Find augmenting paths until no more can be found
            visited.clear()

        return validSeats - len(match) // 2  # Return the number of seats minus the size of the matching

    # Time Complexity: O(V * E^2) where V represents the vertices, or valid seats, and E represents the edges, or edges
    # between the seats.
    # This is because the algorithm uses the Ford-Fulkerson method to compute the maximum matching, which has a
    # complexity of O(V * E^2) in the worst case. The graph construction portion of the algorithm has a complexity of
    # O(VE) time, as we iterate over all the valid seats and their neighbors to build the graph. Each run of the BFS
    # algorithm for augmenting paths has a complexity of O(E) time. These two parts of the algorithm combine to give
    # a total complexity of O(V * E^2) time.
    