import tiledriver

# print(tiledriver.conflict_tiles(3, 5))
# print(tiledriver.conflict_tiles(4, 7))

tiles = (3, 1, 8, 6, 0, 5, 4, 7, 2)
arr = []
for i in range(len(tiles)):
    arr.append(tiles[i])
arr.remove(0)
print(tiledriver.count_inversions(arr, 0))

# tiles0 = (1, 3, 2, 0)
# tiles1 = (1, 6, 4, 7, 0, 5, 8, 3, 2)
# tiles2 = (3, 1, 8, 6, 0, 5, 4, 7, 2)
# tiles3 = (3, 7, 1, 4, 0, 2, 6, 8, 5)
#
#
# state1 = tiledriver.State((0, 1, 2), "", 0, 10)
# state2 = tiledriver.State((0, 1, 2), "", 0, 10)
# state3 = tiledriver.State((0, 1, 2), "", 0, 10)
# state4 = tiledriver.State((0, 1, 2), "", 0, 10)
# state5 = tiledriver.State((0, 1, 2), "", 0, 10)
#
# frontier = [
#     (state1, 8),
#     (state2, 6),
#     (state3, 1),
#     (state4, 3),
#     (state5, 12)
# ]

# most_c = tiledriver.get_n_most_conflicts(frontier, 3)
# print(most_c)


# tiledriver.shuffle_tiles(9, 29)

# r1 = tiledriver.get_random_solvable_state(4)
# r2 = tiledriver.get_random_solvable_state(9)
# r3 = tiledriver.get_random_solvable_state(16)


# print("get_random_solvable_state: {}".format(r1))
# print(tiledriver.is_solvable(r1))
# print("get_random_solvable_state: {}".format(r2))
# print(tiledriver.is_solvable(r2))
# print("get_random_solvable_state: {}".format(r3))
# print(tiledriver.is_solvable(r3))

# print("tiles: {}".format(tiles0))
# print("is_solvable: {}".format(tiledriver2.is_solvable(tiles0)))
#
# print("tiles: {}".format(tiles1))
# print("is_solvable: {}".format(tiledriver2.is_solvable(tiles1)))
#
# print("tiles: {}".format(tiles2))
# print("is_solvable: {}".format(tiledriver2.is_solvable(tiles2)))
#
# print("tiles: {}".format(tiles3))
# print("is_solvable: {}".format(tiledriver2.is_solvable(tiles3)))
