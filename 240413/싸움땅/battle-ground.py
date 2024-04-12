n, m, k = map(int, input().split())

p_pos = [(0, 0)] * m
dir = [0] * m
stat = [0] * m

gun_pos = []
gun_power = []
p_gun = [-1] * m
score = [0] * m

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board = [list(map(int, input().split())) for _ in range(n)]

def is_player(i):
    for p_i in range(m):
        if p_i != i and p_pos[p_i] == p_pos[i]:
            return p_i
    return -1

for i in range(n):
    for j in range(n):
        if board[i][j]:
            gun_pos.append((i, j))
            gun_power.append(board[i][j])
            board[i][j] = 0

for i in range(m):
    x, y, d, s = map(int, input().split())
    p_pos[i] = (x - 1, y - 1)
    dir[i] = d
    stat[i] = s

for _ in range(k):
    for i in range(m):
        # 플레이어 이동
        p_d = dir[i]
        nx, ny = p_pos[i][0] + dx[p_d], p_pos[i][1] + dy[p_d]
        if not (0 <= nx < n):
            n_d = 2 - p_d
            dir[i] = n_d
            nx = p_pos[i][0] + dx[n_d]
        elif not (0 <= ny < n):
            n_d = 4 - p_d
            dir[i] = n_d
            ny = p_pos[i][1] + dy[n_d]
        p_pos[i] = (nx, ny)
        # 총이 있다면 함께 이동
        if p_gun[i] != -1:
            gun_pos[p_gun[i]] = (nx, ny)

        # 이동한 칸에 플레이어가 있는지
        o_idx = is_player(i)

        # 플레이어 x 총 o
        if o_idx == -1:
            for g in range(len(gun_pos)):
                if p_pos[i] == gun_pos[g]:
                    if p_gun[i] == -1:
                        gun_p = 0
                    else:
                        gun_p = gun_power[p_gun[i]]
                    if gun_power[g] > gun_p:
                        p_gun[i] = g

        # 플레이어 o
        else:
            if p_gun[i] == -1:
                gun_power1 = 0
            else:
                gun_power1 = gun_power[p_gun[i]]

            if p_gun[o_idx] == -1:
                gun_power2 = 0
            else:
                gun_power2 = gun_power[p_gun[o_idx]]


            if gun_power1 + stat[i] > gun_power2 + stat[o_idx]:
                winner = i
                loser = o_idx
            elif gun_power1 + stat[i] == gun_power2 + stat[o_idx]:
                if stat[i] > stat[o_idx]:
                    winner = i
                    loser = o_idx
                else:
                    winner = o_idx
                    loser = i
            else:
                winner = o_idx
                loser = i

            # 이긴 플레이어의 경우
            score[winner] += abs((gun_power1 + stat[i]) - (gun_power2 + stat[o_idx]))

            for g in range(len(gun_pos)):
                if p_pos[winner] == gun_pos[g]:
                    if gun_power[g] > gun_power[p_gun[winner]]:
                        p_gun[winner] = g

            # 진 플레이어의 경우
            p_gun[loser] = -1

            p_d = dir[loser]
            sx, sy = p_pos[loser]
            for t_d in range(4):
                nx, ny = sx + dx[(p_d + t_d) % 4], sy + dy[(p_d + t_d) % 4]
                p_pos[loser] = (nx, ny)
                if (0 <= nx < n and 0 <= ny < n) and is_player(loser) == -1:
                    dir[loser] = (p_d + t_d) % 4
                    break
                else:
                    p_pos[loser] = (sx, sy)

            gun_p = 0
            for g in range(len(gun_pos)):
                if p_pos[loser] == gun_pos[g]:
                    if gun_power[g] > gun_p:
                        gun_p = gun_power[g]
                        p_gun[loser] = g

            # 버린 총 줍기
            if p_gun[winner] == -1:
                gun_p = 0
            else:
                gun_p = gun_power[p_gun[winner]]
            for g in range(len(gun_pos)):
                if p_pos[winner] == gun_pos[g]:
                    if gun_power[g] > gun_p:
                        gun_p = gun_power[g]
                        p_gun[winner] = g

for i in range(m):
    print(score[i], end=" ")