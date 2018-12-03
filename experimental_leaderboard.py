fin = open('leaderboard.txt')

fin_list = [x.strip() for x in fin.readlines()]

fin.close()

print(fin_list)

names = []
scores = []

for player in fin_list:
    name, score = player.split()
    names.append(name)
    scores.append(score)

name = input().upper()
score = input()

for x in range(len(scores)):
    if score > scores[x]:
        names.insert(x, name)
        scores.insert(x, score)
        break
    elif score == scores[x]:
        if tuple(name) <= tuple(names[x]):
            names.insert(x, name)
            scores.insert(x, score)
            break
        else:
            names.insert(x+1, name)
            scores.insert(x+1, score)
            break

names = names[:10]
scores = scores[:10]

for_writing = ''

for i in range(10):
    for_writing += '{} {}\n'.format(names[i], scores[i])

fin = open('leaderboard.txt', 'w')

fin.write(for_writing)

fin.close()