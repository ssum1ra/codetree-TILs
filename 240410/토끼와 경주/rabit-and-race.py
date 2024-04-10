class Rabbit:
    def __init__(self, x, y, id, d, cnt, score):
        self.x = x
        self.y = y
        self.id = id
        self.d = d
        self.cnt = cnt
        self.score = score
    def print(self):
        print(self.x, self.y, self.id, self.d, self.cnt, self.score)

q = int(input())
running_rabbit = []
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for _ in range(q):
    query = list(map(int, input().split()))

    if query[0] == 100:
        #경주 시작 준비
        n, m, p = query[1:4]
        for i in range(p):
            running_rabbit.append(Rabbit(1, 1, query[4 + 2 * i], query[4 + (1 + 2 * i)], 0, 0))

    elif query[0] == 200:
        #경주 진행
        k, s = query[1], query[2]

        runned_rabbit = set()
        for _ in range(k):
            running_rabbit.sort(key = lambda x : (x.cnt, (x.x + x.y), x.x, x.y, x.id))
            r = running_rabbit[0]
            r.cnt += 1
            runned_rabbit.add(r.id)
            pos = []
            for i in range(4):
                nx, ny = r.x, r.y
                dir_x = dx[i]
                dir_y = dy[i]
                for _ in range(r.d):
                    if nx + dir_x < 1 or nx + dir_x > n:
                        dir_x = -dir_x
                    elif ny + dir_y < 1 or ny + dir_y > m:
                        dir_y = -dir_y
                    nx = nx + dir_x
                    ny = ny + dir_y
                pos.append((nx, ny))

            pos.sort(key = lambda x : (-(x[0] + x[1]), -x[0], -x[1]))
            r.x, r.y = pos[0]
            for t in running_rabbit:
                if t.id != r.id:
                    t.score += r.x + r.y

        running_rabbit.sort(key = lambda x : (-(x.x + x.y), -x.x, -x.y, -x.id))
        for i in range(len(running_rabbit)):
            r = running_rabbit[i]
            if r.id in runned_rabbit:
                r.score += s
                break

    elif query[0] == 300:
        #이동거리 변경
        id = query[1]
        l = query[2]
        for r in running_rabbit:
            if r.id == id:
                r.d *= l
    else:
        #최고의 토끼 선정
        running_rabbit.sort(key = lambda x : -x.score)
        print(running_rabbit[0].score)