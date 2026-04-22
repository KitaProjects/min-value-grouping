# ======= #
# GLOBALS #
# ======= #
INF = float("inf")

# ==== #
# MAIN #
# ==== #
def main():
    n = int(input())
    k = int(input())

    arr     = init_arr()
    dp      = init_dp(n, k)
    traceDp = init_traceDp(n, k)

    pSum = init_pSums(n, arr)

    solve(n, k, pSum, dp, traceDp)

    slices = trace_back(k, n, traceDp)

    print(dp[k][n])
    print(slices)

# ------ #
# SOLVER #
# ------ #
def solve(n, k, pSum, dp, traceDp):
    for i in range(1, k + 1):
        for j in range(i, n + 1):
            for m in range(i - 1, j):
                if dp[i - 1][m] < INF:
                    # sum of the i'th group using the precalculated sums
                    groupSum = pSum[j] - pSum[m]

                    # total cost = cost of first i-1 groups + current group sum cubed
                    cost = dp[i - 1][m] + groupSum ** 3

                    # chose the winner
                    if cost < dp[i][j]:
                        dp[i][j]      = cost
                        traceDp[i][j] = m

# ---------- #
# TRACE BACK #
# ---------- #
def trace_back(k, n, traceDp):
    slices = []

    while k > 0:
        m = traceDp[k][n]
        slices.append(n)

        n = m
        k -= 1

    slices.append(0)
    slices.reverse()

    return slices


# ------------ #
# INIT HELPERS #
# ------------ #

# splits input array
def init_arr():
    arr = []

    for i in input().split():
        arr.append(int(i))

    return arr


# initialises dynamic programming table e.g.
# [ [0  , INF, INF, INF]
#   [INF, INF, INF, INF]
#   [INF, INF, INF, INF]
# ]
def init_dp(n, k):
    dp = []

    for _ in range(k + 1):
        row = [INF] * (n + 1)
        dp.append(row)

    dp[0][0] = 0

    return dp

# initialises trace table to trace the dynamic programming table e.g.
# [ [-1, -1, -1, -1]
#   [-1, -1, -1, -1]
#   [-1, -1, -1, -1]
# ]
def init_traceDp(n, k):
    traceDp = []

    for _ in range(k + 1):
        row = [-1] * (n + 1)
        traceDp.append(row)

    return traceDp

# initialises a pre calculated sums table where each i index is the sum of the first i elements e.g.
# [0, 3, 4, 6]
def init_pSums(n, arr):
    pSum = [0] * (n + 1)

    for i in range(n):
        pSum[i + 1] = pSum[i] + arr[i]

    return pSum

# -------- #
# WRITE UP #
# -------- #
#
# OVERVIEW
# --------
# This min-value-grouping solution uses dynamic programming the table of which is stored in a 2D
# array, dp, which can be thought of as a table. dp[i][j] will be the smallest possible cost of
# partitioning the first j elements into exactly i groups. The dp is updated by the solver
# function which updates dp row by row finding the best possible solution for each number of
# partitions leading up to the target. e.g. first we find the best possible solutions for 1
# partition which is trivial. Then we find the best possible solution for 2 paritions. This is
# done by considering every way we can split the 1 partition solutions and so on until we have
# the number of desired partitions. Once the table is filled, dp[k][n] holds the answer and
# we can use traceDp to reconstruct the positions of the boundaries.
#
# The sums are precalculated so that the sum of any array slice can be fetched O(1) and a 2D
# array, traceDp, acts as a trace table so that the positions of partitions can be reconstructed
#
# MODULE RELEVANCE
# ----------------
# This is similar to {0, 1} knapsack problem solution but differs in some ways. For one, the
# solution to the min value grouping problem will always be in dp[k][n] whereas in the knapsack
# problem we are just looking for the highest possible value in the entire table. Another way
# this problem differs from the {0, 1} knapsack problem is that here we must retain the order
# of the items given whereas the knapsack problem allows us to pick whichever items we want
# in whichever order we want. I believe this distinction is what makes this solution more
# inefficient than the {0, 1} knapsack problem. In the knapsack problem, we can either keep
# or leave an item, but in the min value grouping problem we must (I assume we must) consider
# every single possible way we can partition the set of numbers.
#
# TIME COMPLEXITY
# ---------------
# Initialising dp and traceDp fills a (k+1) by (n+1) table costing O(nk). The pre calculated sums
# are O(n).
#
# The solver runs 3 nested loops:
# 
# for i in range(1, k + 1):         | k iterations
#     for j in range(i, n + 1):     | At most n iterations
#         for m in range(i - 1, j): | At most n iterations
#
# This results in O(knn) or O(k*n^2) which is the final time complexity of this solution.
main()

