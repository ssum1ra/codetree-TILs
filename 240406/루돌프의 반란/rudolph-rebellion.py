def is_inrange(x, y):
    return 1 <= x and x <= n and 1 <= y and y <= n

n, m, p, c, d = map(int, input().split())
rudolf = tuple(map(int, input().split()))

points = [0 for _ in range(p + 1)]
pos = [(0, 0) for _ in range(p + 1)]
board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
is_live = [False for _ in range(p + 1)]
stun = [0 for _ in range(p + 1)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board[rudolf[0]][rudolf[1]] = -1

for _ in range(p):
    id, x, y = tuple(map(int, input().split()))
    pos[id] = (x, y)
    board[pos[id][0]][pos[id][1]] = id
    is_live[id] = True

for t in range(1, m+1):
    # 살아있는 산타 중 가장 루돌프에 가장 가까운 산타 찾기
    closestX, closestY, closestIdx = 10000, 10000, 0

    for i in range(1, p + 1):
        if not is_live[i]:
            continue

        currentBest = ((closestX - rudolf[0]) ** 2 + (closestY - rudolf[1]) ** 2, (-closestX, -closestY))
        currentValue = ((pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2, (-pos[i][0], -pos[i][1]))

        if currentValue < currentBest:
            closestX, closestY = pos[i]
            closestIdx = i

    # 가장 가까운 산타의 방향으로 루돌프 이동
    if closestIdx:
        prevRudolf = rudolf
        moveX = 0
        if closestX > rudolf[0]:
            moveX = 1
        elif closestX < rudolf[0]:
            moveX = -1

        moveY = 0
        if closestY > rudolf[1]:
            moveY = 1
        elif closestY < rudolf[1]:
            moveY = -1

        rudolf = (rudolf[0] + moveX, rudolf[1] + moveY)
        board[prevRudolf[0]][prevRudolf[1]] = 0

    # 루돌프의 이동으로 산타와 충돌한 경우
    if rudolf[0] == closestX and rudolf[1] == closestY:
        firstX = closestX + moveX * c
        firstY = closestY + moveY * c
        lastX, lastY = firstX, firstY

        stun[closestIdx] = t + 1

        # 만약 이동한 위치에 산타가 있는 경우
        while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
            lastX += moveX
            lastY += moveY

        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY

            if not is_inrange(beforeX, beforeY):
                break

            idx = board[beforeX][beforeY]

            if not is_inrange(lastX, lastY):
                is_live[idx] = False
            else:
                board[lastX][lastY] = board[beforeX][beforeY]
                pos[idx] = (lastX, lastY)

            lastX, lastY = beforeX, beforeY

        points[closestIdx] += c
        pos[closestIdx] = (firstX, firstY)
        if is_inrange(firstX, firstY):
            board[firstX][firstY] = closestIdx
        else:
            is_live[closestIdx] = False
    board[rudolf[0]][rudolf[1]] = -1

    # 루돌프와 가장 가까운 방향으로 산타 이동
    for i in range(1, p+1):
        if not is_live[i] or stun[i] >= t:
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
                stun[i] = t + 1
                moveX = -dx[move_dir]
                moveY = -dy[move_dir]
                firstX = nx + moveX * d
                firstY = ny + moveY * d
                lastX, lastY = firstX, firstY

                if d == 1:
                    points += 1
                else:
                    while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY
                    while not (firstX == lastX and firstY == lastY):
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY

                        if not is_inrange(beforeX, beforeY):
                            break

                        idx = board[beforeX][beforeY]
                        if not is_inrange(lastX, lastY):
                            is_live[idx] = False
                        else:
                            board[lastX][lastY] = board[beforeX][beforeY]
                            pos[idx] = (lastX, lastY)
                        lastX, lastY = beforeX, beforeY
                    points[i] += d
                    board[pos[i][0]][pos[i][1]] = 0
                    pos[i] = (firstX, firstY)
                    if is_inrange(firstX, firstY):
                        board[firstX][firstY] = i
                    else:
                        is_live[i] = False
            else:
                board[pos[i][0]][pos[i][1]] = 0
                pos[i] = (nx, ny)
                board[nx][ny] = i

    # 턴이 끝나고 탈락하지 않은 산타들의 점수를 1 증가
    for i in range(1, p+1):
        if is_live[i]:
            points[i] += 1

# 결과 출력
for i in range(1, p+1):
    print(points[i], end=" ")