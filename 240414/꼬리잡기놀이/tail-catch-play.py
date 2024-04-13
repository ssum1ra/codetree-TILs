n, m, k = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(n)]

team = []

dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

def is_inrange(x, y):
    return 0 <= x < n and 0 <= y < n

def move_team(i):
    next_team = team[i][:]
    sx, sy = team[i][0]
    for dx, dy in zip(dxs, dys):
        nx, ny = sx + dx, sy + dy
        if is_inrange(nx, ny) and board[nx][ny] == 4 and (not (nx, ny) in team[i]):
            next_team[0] = (nx, ny)
            break
    for t in range(len(team[i]) - 1):
        next_team[t + 1] = team[i][t]
    team[i] = next_team

def change_dir(i):
    next_team = team[i][:]
    for t in range(len(team[i])):
        next_team[t] = team[i][len(team[i]) - t - 1]
    team[i] = next_team

def throw_ball(t):
    if 0 < t % (4*n) <= n:
        x = t - 1
        for y in range(n):
            for t in range(m):
                for i in range(len(team[t])):
                    if (x, y) == team[t][i]:
                        change_dir(t)
                        return (i+1) ** 2

    elif n < t % (4*n) <= 2*n:
        y = t - (n + 1)
        for x in range(n-1, -1, -1):
            for t in range(m):
                for i in range(len(team[t])):
                    if (x, y) == team[t][i]:
                        change_dir(t)
                        return (i+1) ** 2

    elif 2*n < t % (4*n) <= 3*n:
        x = n - (t % (2*n))
        for y in range(n-1, -1, -1):
            for t in range(m):
                for i in range(len(team[t])):
                    if (x, y) == team[t][i]:
                        change_dir(t)
                        return (i+1) ** 2

    elif 3*n < t % (4*n) <= 4*n:
        y = n - (t % (3*n))
        for x in range(n):
            for t in range(m):
                for i in range(len(team[t])):
                    if (x, y) == team[t][i]:
                        change_dir(t)
                        return (i+1) ** 2

    return 0

#팀 초기화
for i in range(n):
    for j in range(n):
        if board[i][j] == 1:
            team.append([(i, j)])
            board[i][j] = 4

for i in range(m):
    not_found_end = True

    head_x, head_y = team[i][0]
    sx, sy = head_x, head_y

    while not_found_end:
        for dx, dy in zip(dxs, dys):
            nx, ny = sx + dx, sy + dy
            if is_inrange(nx, ny) and (not (nx, ny) in team[i]):
                if board[nx][ny] == 2:
                    team[i].append((nx, ny))
                    board[nx][ny] = 4
                    sx, sy = nx, ny
                    break
                elif board[nx][ny] == 3 and len(team[i]) > 1:
                    team[i].append((nx, ny))
                    board[nx][ny] = 4
                    not_found_end = False
                    break

score = 0
for t in range(1, k+1):
    #팀 한칸 이동
    for i in range(m):
        move_team(i)

    #공 던지기
    score += throw_ball(t)
    print(team)

print(score)