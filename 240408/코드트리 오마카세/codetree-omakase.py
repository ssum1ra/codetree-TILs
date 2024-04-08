import sys
sys.stdin = open('input.txt', 'r')

class Query:
    def __init__(self, cmd, t, x, name, n):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n

queries = []
p_queries = {}
names = set()
entry_time = {}
position = {}
exit_time = {}

#입력
l, q = map(int, input().split())
for _ in range(q):
    command = input().split()
    cmd, t, x, n = -1, -1, -1, -1
    name = ""
    cmd = int(command[0])
    if cmd == 100:
        t, x, name = command[1:]
        t, x = map(int, [t, x])
    elif cmd == 200:
        t, x, name, n = command[1:]
        t, x, n = map(int, [t, x, n])
    else:
        t = int(command[1])

    queries.append(Query(cmd, t, x, name, n))

    if cmd == 100:
        if name not in p_queries:
            p_queries[name] = []
        p_queries[name].append(Query(cmd, t, x, name, n))
    elif cmd == 200:
        names.add(name)
        entry_time[name] = t
        position[name] = x

for name in names:
    exit_time[name] = 0
    for q in p_queries[name]:
        time_to_lived = 0
        #입장 전 초밥 명령
        if q.t < entry_time[name]:
            t_sushi_x = (q.x + (entry_time[name] - q.t)) % l
            additional_time = (position[name] - t_sushi_x + l) % l
            time_to_lived = entry_time[name] + additional_time

        #입장 후 초밥 명령
        else:
            additional_time = (position[name] - q.x + l) % l
            time_to_lived = q.t + additional_time

        exit_time[name] = max(exit_time[name], time_to_lived)
        queries.append(Query(111, time_to_lived, -1, name, -1))

for name in names:
    queries.append(Query(222, exit_time[name], -1, name, -1))

queries.sort(key = lambda q: (q.t, q.cmd))

people_num, sushi_num = 0, 0
for q in queries:
    if q.cmd == 100:
        sushi_num += 1
    elif q.cmd == 111:
        sushi_num -= 1
    elif q.cmd == 200:
        people_num += 1
    elif q.cmd == 222:
        people_num -= 1
    else:
        print(people_num, sushi_num)