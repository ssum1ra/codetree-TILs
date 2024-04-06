def is_inrange(x, y):
    return 0 < x <= N and 0 < y <= N

N, M, P, C, D = map(int, input().split())
rudolf = tuple(map(int, input().split()))

board = [[0] * (N+1) for _ in range(N+1)]
pos = [(0,0) for _ in range(P+1)]
score = [0] * (P+1)
is_lived = [False] * (P+1)
wait = [0] * (P+1)

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board[rudolf[0]][rudolf[1]] = -1

for _ in range(P):
    i, x, y = map(int, input().split())
    pos[i] = (x, y)
    board[x][y] = id
    is_lived[i] = True

for turn in range(1, M+1):
    # 살아있는 산타 중 가장 루돌프에 가장 가까운 산타 찾기
    closest_santa = 0
    closest_santa_pos = (2*N, 2*N)
    for i in range(1, P+1):
        if not is_lived[i]:
            continue
        min_dist = ((closest_santa_pos[0] - rudolf[0])**2 + (closest_santa_pos[1] - rudolf[1]) ** 2, (-closest_santa_pos[0], -closest_santa_pos[1]))
        dist = ((pos[i][0] - rudolf[0])**2 + (pos[i][1] - rudolf[1])**2, (-pos[i][0], -pos[i][1]))
        if min_dist > dist:
            closest_santa = i
            closest_santa_pos = pos[i]


    # 가장 가까운 산타의 방향으로 루돌프 이동
    if closest_santa:
        prev_rudolf = rudolf
        move_x = 0
        if pos[closest_santa][0] > rudolf[0]:
            move_x = 1
        elif pos[closest_santa][0] < rudolf[0]:
            move_x = -1
        move_y = 0
        if pos[closest_santa][1] > rudolf[1]:
            move_y = 1
        elif pos[closest_santa][1] < rudolf[1]:
            move_y = -1
        rudolf = (rudolf[0]+move_x, rudolf[1]+move_y)
        board[prev_rudolf[0]][prev_rudolf[1]] = 0

    # 루돌프의 이동으로 산타와 충돌한 경우
    if rudolf[0] == pos[closest_santa][0] and rudolf[1] == pos[closest_santa][1]:
        fx = pos[closest_santa][0] + move_x * C
        fy = pos[closest_santa][1] + move_y * C
        lx, ly = fx, fy

        wait[closest_santa] = turn + 1

        # 만약 이동한 위치에 산타가 있는 경우
        while is_inrange(lx, ly) and board[lx][ly] > 0:
            lx += move_x
            ly += move_y

        while not (fx == lx and fx == ly):
            bx = lx - move_x
            by = ly - move_y

            if not is_inrange(bx, by):
                break

            tmp_santa = board[bx][by]

            if not is_inrange(lx, ly):
                is_lived[tmp_santa] = False
            else:
                board[lx][ly] = board[bx][by]
                pos[tmp_santa] = (lx, ly)

            lx, ly = bx, by

        score[closest_santa] += C
        pos[closest_santa] = (fx, fy)
        if is_inrange(fx, fy):
            board[fx][fy] = closest_santa
        else:
            is_lived[closest_santa] = False
    board[rudolf[0]][rudolf[1]] = -1

    # 루돌프와 가장 가까운 방향으로 산타 이동
    for i in range(1, P+1):
        if not is_lived[i] or wait[i] >= turn:
            continue
        min_dist = (pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2
        move_dir = -1
        for j in range(4):
            nx = pos[i][0]+dx[j]
            ny = pos[i][1]+dy[j]
            if not is_inrange(nx, ny) or board[nx][ny] > 0:
                continue
            dist = (nx-rudolf[0]) ** 2 + (ny-rudolf[1]) ** 2
            if dist < min_dist:
                min_dist = dist
                move_dir = j
        if move_dir != -1:
            nx = pos[i][0]+dx[move_dir]
            ny = pos[i][1]+dy[move_dir]
            # 산타의 이동으로 루돌프와 충돌한 경우
            if nx == rudolf[0] and ny == rudolf[1]:
                wait[i] = turn + 1
                move_x = -dx[move_dir]
                move_y = -dy[move_dir]
                fx = nx + move_x * D
                fy = ny + move_y * D
                lx, ly = fx, fy

                if D == 1:
                    score += 1
                else:
                    while is_inrange(lx, ly) and board[lx][ly] > 0:
                        lx += move_x
                        ly += move_y
                    while not (fx == lx and fy == ly):
                        bx = lx - move_x
                        by = ly - move_y

                        if not is_inrange(bx, by):
                            break

                        tmp_santa = board[bx][by]
                        if not is_inrange(lx, ly):
                            is_lived[tmp_santa] = False
                        else:
                            board[lx][ly] = board[bx][by]
                            pos[tmp_santa] = (lx, ly)
                        lx, ly = bx, by
                    score[i] += D
                    board[pos[i][0]][pos[i][1]] = 0
                    pos[i] = (fx, fy)
                    if is_inrange(fx, fy):
                        board[fx][fy] = i
                    else:
                        is_lived[i] = False
            else:
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = (nx, ny)
                board[nx][ny] = i

    # 턴이 끝나고 탈락하지 않은 산타들의 점수를 1 증가
    for i in range(1, P+1):
        if is_lived[i]:
            score[i] += 1

# 결과 출력
for i in range(1, P+1):
    print(score[i], end=" ")