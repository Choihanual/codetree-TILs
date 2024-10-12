from math import inf
from collections import deque

n, m = map(int, input().split())

graph = [[0 for _ in range(n+1)]]

for _ in range(n):
    graph.append([0] + list(map(int, input().split())))

store = [[]]

for _ in range(m):
    store.append(list(map(int, input().split())))

#graph에 올라온 사람들 => [x, y ,target]
human = []
arrive = []

# 편의점에서 사람 위치로 최단 거리 구할 예정이기 때문에 반대로
# 상, 좌, 우, 하
# dx = [-1, 0, 0, 1]
# dy = [0, -1, 1, 0]

dx = [1, 0, 0, -1]
dy = [0, 1, -1, 0]

# 격자 위의 사람들 움직이기. 단, 사람들이 없다면 안 움직임~
def move_graph():

    # 그래프 위에 올라온 사람들에 한해서 for문, 최단거리를 계산해서 그 루트로 이동해야함
    for i in range(len(human)):
        # target으로부터 사람으로 bfs를 구현하면 마지막에 사람의 위치에 왔을 때 이동방향의 역방향으로만 움직여주면 된다.

        # 이미 도착한 애들은 움직이지마
        if human[i][2] in arrive:
            continue

        target = [human[i][0], human[i][1]]

        visit = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

        q = deque()
        q.append(store[human[i][2]])

        visit[store[human[i][2]][0]][store[human[i][2]][1]] = 1

        while q:
            x, y = q.popleft()
            flag = 0
            for j in range(4):
                nx = x + dx[j]
                ny = y + dy[j]

                # 목적지에 도착했을 경우
                if nx == target[0] and ny == target[1]:
                    human[i][0] = x
                    human[i][1] = y
                    flag = 1
                    break

                # 격자 밖일 경우
                if nx < 1 or nx > n or ny < 1 or ny > n:
                    continue

                # 못 지나가는 영역
                if graph[nx][ny] < 0:
                    continue

                # 이미 방문한 경우
                if visit[nx][ny] == 1:
                    continue



                q.append([nx, ny])

            if flag == 1:
                break

def check_arrive():
    for i in range(len(human)):
        if human[i][2] in arrive:
            continue

        target = human[i][2]

        # 도착했다면 사용 불가하게 바꿔 버리기
        if human[i][0] == store[target][0] and human[i][1] == store[target][1]:
            graph[human[i][0]][human[i][1]] = -1
            arrive.append(human[i][2])

# 최단거리 계산해서 사람 할당시키기 => 베이스캠프 칸 이동불가 처리까지
def base_camp(t):
    target_store = t

    dist = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    q = deque()
    q.append(store[target_store])

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 1 or nx > n or ny < 1 or ny > n:
                continue

            if graph[nx][ny] < 0:
                continue

            # 이미 지나쳐 감
            if dist[nx][ny] > 0:
                continue

            dist[nx][ny] = dist[x][y] + 1
            q.append([nx, ny])


    min_dist = inf
    start_basecamp = 0
    for i in range(1, n+1):
        for j in range(1, n+1):
            # 베이스 캠프라는 뜻
            if graph[i][j] == 1 and dist[i][j] > 0:
                if min_dist > dist[i][j]:
                    min_dist = dist[i][j]
                    start_basecamp = [i, j]

    # 사람 배치
    human.append([start_basecamp[0], start_basecamp[1], t])

    # 그래프 못 지나가게 하기
    graph[start_basecamp[0]][start_basecamp[1]] = -1


def main():
    t = 0
    while True:
        t += 1

        # graph위 사람들 이동
        move_graph()

        # 편의점에 도착했는지 체크해서 지나갈 수 없게 막기
        check_arrive()

        # 베이스 캠프에 할당하기
        if t <= m:
            base_camp(t)

        #  모든 사람들이 편의점에 도달했는지 체크하기
        if len(arrive) == m:
            break

    print(t)
main()