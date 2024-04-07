def is_inrange(r, c, h, w):
    for i in range(h):
        for j in range(w):
            if not (0 < r + i <= l and 0 < c + j <= l):
                return False
    return True

def move(i, d):
    r, c = pos[i][0], pos[i][1]
    nr, nc = r+dx[d], c+dy[d]
    h, w = shield[i][0], shield[i][1]

    if not is_inrange(nr, nc, h, w):
        return False

    for x in range(h):
        for y in range(w):
            if board[nr + x][nc + y] == 2:
                return False
            elif board[nr + x][nc + y] < 0 and board[nr + x][nc + y] != -i:
                ni = -board[nr + x][nc + y]
                if not move(ni, d):
                    return False

    pos[i] = (nr, nc)
    is_changed[i] = True

    for x in range(h):
        for y in range(w):
                board[r + x][c + y] = 0

    for x in range(h):
        for y in range(w):
            board[nr + x][nc + y] = -i

    return True

def check_trap(i):
    r, c, h, w = pos[i][0], pos[i][1], shield[i][0], shield[i][1]
    cnt = 0
    for i in range(h):
        for j in range(w):
            if (r+i, c+j) in trap:
                cnt += 1
    return cnt

l, n, q = map(int, input().split())
board = [[2] * (l+2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(l)] + [[2] * (l+2)]
pos = [(0, 0)] * (n+1)
shield = [(0, 0)] * (n+1)
hp = [0] * (n+1)
trap = []
is_changed = [False] * (n+1)

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for i in range(l+2):
    for j in range(l+2):
        if board[i][j] == 1:
            trap.append((i,j))
            board[i][j] = 0

for i in range(1, n+1):
    r, c, h, w, k = map(int, input().split())
    pos[i] = (r, c)
    shield[i] = (h, w)
    hp[i] = k

    for x in range(h):
        for y in range(w):
            board[r+x][c+y] = -i

start_hp = hp[:]

for _ in range(q):
    i, d = map(int, input().split())
    r, c, h, w = pos[i][0], pos[i][1], shield[i][0], shield[i][1]

    if hp[i] != 0:
        if move(i, d):
            for t in range(1, n+1):
                if hp[t] > 0 and i != t and is_changed[t]:
                    cnt = check_trap(t)
                    hp[t] -= cnt
                    is_changed[t] = False

    for t in range(1, n+1):
        if hp[t] == 0:
            for x in range(shield[t][0]):
                for y in range(shield[t][1]):
                    board[pos[t][0]+x][pos[t][1]+y] = 0

res = 0
for i in range(1, n+1):
    if hp[i] != 0:
        res += start_hp[i] - hp[i]
print(res)