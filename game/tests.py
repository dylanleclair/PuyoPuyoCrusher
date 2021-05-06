import helpers
import ai

w = 6
h = 13
board = [[' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ']]


s = ai.Search(board)

results = s.root.div()

for x in results:
    for y in x:
        print(y)
    print()

'''
#board = [[' ' for x in range(w)] for y in range(h)]

for item in board:
    print(item)

ap = helpers.AttackPowers()

print()

print(helpers.projected_score(board, ap.chain_powers))

b = helpers.place(board,'1', 3)
b = helpers.place(b,'1', 3)
b = helpers.place(b,'1', 2)
b = helpers.place(b,'1', 2)

print(helpers.projected_score(b, ap.chain_powers))
for x in b:
    print(x)

helpers.remove_puyos(board, helpers.drop(board))

for item in board:
    print(item)

helpers.correct_board(board)
print()
for item in board:
    print(item)
'''