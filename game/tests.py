import helpers
import ai

w = 6
h = 13
board = [[' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ']]





s = ai.Search(board,[('1','1'), ('1','2'),('1','2')])
result = s.search()

print('board: ')
for x in result.board:
    print(x)

print('score', result.score_accumulated)

print('moves', result.moves)

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

b = helpers.place(board,'1', 0)
b = helpers.place(b,'1', 1)
b = helpers.place(b,'1', 2)
b = helpers.place(b,'1', 3)
b = helpers.place(b,'2', 0)
b = helpers.place(b,'2', 1)
b = helpers.place(b,'2', 2)
b = helpers.place(b,'2', 3)

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