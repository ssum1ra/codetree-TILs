n, m, h, k = map(int, input().split())

runner = [(0, 0, 0)] * m
for i in range(m):
    x, y, d = map(int, input().split())
    runner[i] = (x-1, y-1, d)

tree = [(0, 0)] * h
for i in range(h):
    x, y = map(int, input().split())
    tree[i] = (x-1, y-1)

# 술래 (x, y, d, 해당 방향으로 이동한 칸 수)
it = (n//2, n//2, 0, 0)
# 술래의 이동 방향 (시계 방향, 반시계 방향)
is_cw = True
# 술래가 한 방향으로 가야 하는 칸의 수
finish_cnt = 1

is_alive = [True] * m

dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

def is_inrange(x, y):
    return 0 <= x < n and 0 <= y < n

def runner_move(i):
    r_x, r_y, r_d = runner[i]
    it_x, it_y, _, _ = it

    if abs(r_x - it_x) + abs(r_y - it_y) > 3:
        return

    nx, ny = r_x + dxs[r_d], r_y + dys[r_d]

    if is_inrange(nx, ny):
        if not (nx == it_x and ny == it_y):
            runner[i] = (nx, ny, r_d)
    else:
        n_d = (r_d - 2) if r_d > 1 else (r_d + 2)
        runner[i] = (r_x, r_y, n_d)

        nx, ny = r_x + dxs[n_d], r_y + dys[n_d]

        if not (nx == it_x and ny == it_y):
            runner[i] = (nx, ny, n_d)

def it_move():
    global finish_cnt, is_cw, it
    it_x, it_y, it_d, it_cnt = it

    nx, ny = it_x + dxs[it_d], it_y + dys[it_d]
    nd = it_d
    ncnt = it_cnt + 1

    if nx == 0 and ny == 0:
        is_cw = False
        finish_cnt = n
        it = (nx, ny, 2, 1)
        return

    if nx == n//2 and ny == n//2:
        is_cw = True
        finish_cnt = 1
        it = (nx, ny, 0, 0)
        return

    if finish_cnt == ncnt:
        if is_cw:
            nd = (it_d + 1) % 4
            if it_d == 1 or it_d == 3:
                finish_cnt += 1
        else:
            nd = (it_d - 1 + 4) % 4
            if it_d == 0 or it_d == 2:
                finish_cnt -= 1
        ncnt = 0

    it = (nx, ny, nd, ncnt)
    return

def tag():
    cnt = 0
    it_x, it_y, it_d, _ = it
    for i in range(3):
        nx, ny = it_x + dxs[it_d] * i, it_y + dys[it_d] * i

        if (nx, ny) in tree:
            continue

        for r in range(m):
            r_x, r_y, _ = runner[r]
            if is_alive[r] and nx == r_x and ny == r_y:
                cnt += 1
                is_alive[r] = False
    return cnt

ans = 0
for t in range(1, k+1):
    #도망자 이동
    for i in range(m):
        if is_alive[i]:
            runner_move(i)

    #술래 이동
    it_move()

    # 시야 내 도망자 잡기
    ans += t * tag()

print(ans)