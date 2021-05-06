import helpers

w = 6
h = 13
board = [[' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', '2', ' ', ' '], [' ', ' ', ' ', '4', '4', '4'], [' ', ' ', '2', '2', '2', '4']]

#board = [[' ' for x in range(w)] for y in range(h)]

for item in board:
    print(item)

ap = helpers.AttackPowers()

print()

print(helpers.projected_score(board, ap.chain_powers))

'''
helpers.remove_puyos(board, helpers.drop(board))

for item in board:
    print(item)

helpers.correct_board(board)
print()
for item in board:
    print(item)
'''