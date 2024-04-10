from collections import deque

class Turrent:
    def __init__(self, x, y, r, p):
        self.x = x
        self.y = y
        self.r = r
        self.p = p

def init():
    global turn

    turn += 1
    for i in range(n):
        for j in range(m):
            vis[i][j] = False
            is_active[i][j] = False

def awake():
    live_turret.sort(key=lambda x: (x.p, -x.r, -(x.x + x.y), -x.y))
    weak_turrent = live_turret[0]
    x = weak_turrent.x
    y = weak_turrent.y

    board[x][y] += n+m
    rec[x][y] = turn
    weak_turrent.p = board[x][y]
    weak_turrent.r = rec[x][y]
    is_active[x][y] = True

    live_turret[0] = weak_turrent


def laser_attack():
    weak_turrent = live_turret[0]
    sx, sy = weak_turrent.x, weak_turrent.y
    power = weak_turrent.p

    strong_turrent = live_turret[-1]
    ex, ey = strong_turrent.x, strong_turrent.y

    q = deque()
    vis[sx][sy] = True
    q.append((sx, sy))

    can_attack = False

    while q:
        x, y = q.popleft()

        if x == ex and y == ey:
            can_attack = True
            break

        for dx, dy in zip(dx1, dy1):
            nx = (x + dx + n) % n
            ny = (y + dy + m) % m

            if vis[nx][ny]:
                continue

            if board[nx][ny] == 0:
                continue

            vis[nx][ny] = True
            back_x[nx][ny] = x
            back_y[nx][ny] = y
            q.append((nx, ny))

    if can_attack:
        board[ex][ey] -= power
        if board[ex][ey] < 0:
            board[ex][ey] = 0
        is_active[ex][ey] = True

        cx = back_x[ex][ey]
        cy = back_y[ex][ey]

        while not (cx == sx and cy == sy):
            board[cx][cy] -= power//2
            if board[cx][cy] < 0:
                board[cx][cy] = 0
            is_active[cx][cy] = True

            next_cx = back_x[cx][cy]
            next_cy = back_y[cx][cy]

            cx = next_cx
            cy = next_cy

    return can_attack

def bomb_attack():
    weak_turrent = live_turret[0]
    sx, sy = weak_turrent.x, weak_turrent.y
    power = weak_turrent.p

    strong_turrent = live_turret[-1]
    ex, ey = strong_turrent.x, strong_turrent.y

    for x, y in zip(dx2, dy2):
        nx = (ex + x + n) % n
        ny = (ey + y + m) % m

        if sx == nx and sy == ny:
            continue

        if ex == nx and ey == ny:
            board[nx][ny] -= power
            if board[nx][ny] < 0:
                board[nx][ny] = 0
            is_active[nx][ny] = True
        else:
            board[nx][ny] -= power//2
            if board[nx][ny] < 0:
                board[nx][ny] = 0
            is_active[nx][ny] = True

def reserve():
    for i in range(n):
        for j in range(m):
            if is_active[i][j]:
                continue
            if board[i][j] == 0:
                continue
            board[i][j] += 1

n, m, k = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
rec = [[0] * m for _ in range(n)]
turn = 0
vis = [[False] * m for _ in range(n)]
is_active = [[False] * m for _ in range(n)]
back_x = [[0] * m for _ in range(n)]
back_y = [[0] * m for _ in range(n)]
dx1 = [0, 1, 0, -1]
dy1 = [1, 0, -1, 0]
dx2 = [0, -1, -1, 0, 1, 1, 1, 0, -1]
dy2 = [0, 0, 1, 1, 1, 0, -1, -1, -1]

for t in range(1, k+1):
    live_turret = []
    for i in range(n):
        for j in range(m):
            if board[i][j]:
                new_turret = Turrent(i, j, rec[i][j], board[i][j])
                live_turret.append(new_turret)

    if len(live_turret) <= 1:
        break

    init()

    awake()

    is_suc = laser_attack()
    if not is_suc:
        bomb_attack()

    reserve()

res = 0
for i in range(n):
    for j in range(m):
        res = max(res, board[i][j])
print(res)