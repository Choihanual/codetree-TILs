from collections import deque

R, C, K = map(int, input().split())

graph = [[0 for _ in range(C)] for _ in range(R)]
door_position = [[0 for _ in range(C)] for _ in range(R)]

# 북, 동, 남, 서
# 0, 1, 2, 3
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 골렘의 이동 방식을 판단하고 이동시킴
def move(number, position, door):
    q = deque()

    # 골렘의 중심부와 진행 방향까지 append
    q.append((-2, position, 2))

    # 첫 움직임 => 남쪽으로 이동
    while q:
        x, y, direction = q.popleft()

        if x == R - 2:
            graph[x][y] = number

            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                graph[nx][ny] = number

            if door == 0:
                door_position[x - 1][y] = number
            elif door == 1:
                door_position[x][y + 1] = number
            elif door == 2:
                door_position[x + 1][y] = number
            else:
                door_position[x][y - 1] = number

            # 최종 골렘 중심부 위치
            return x, y

        # 남쪽으로 이동
        if direction == 2:

            move_available = 1
            for i in range(1, 4):
                # 골렘의 하단부로 이동 => x에 +1
                nx, ny = x + dx[i] + 1, y + dy[i]

                if nx >= R or ny >= C or ny < 0:
                    move_available = 0
                    continue

                if nx >= 0:
                    # 골렘이 위치하고 있을 경우 이동 불가
                    if graph[nx][ny] != 0:
                        move_available = 0

            if move_available:
                q.append((x + 1, y, 2))
            else:
                q.append((x, y, 3))

        # 서쪽으로 이동, 입구의 회전까지 고려
        elif direction == 3:
            move_available = 1
            for i in 0, 2, 3:
                # 골렘의 서쪽부로 이동 => y에 -1
                nx, ny = x + dx[i], y + dy[i] -1

                if nx >= R or ny >= C or ny < 0:
                    move_available = 0
                    continue

                # 골렘이 위치하고 있을 경우 이동 불가
                if graph[nx][ny] != 0:
                    move_available = 0

            for i in 2, 3:
                nx, ny = x + dx[i] + 1, y + dy[i] -1

                if nx >= R or ny >= C or ny < 0:
                    move_available = 0
                    continue

                # 골렘이 위치하고 있을 경우 이동 불가
                if graph[nx][ny] != 0:
                    move_available = 0

            # door 위치 회전시키기~
            if move_available:
                q.append((x + 1, y - 1, 2))

                door -= 1
                if door == -1:
                    door = 3

            else:
                q.append((x, y, 1))

        # 동쪽으로 이동, 입구의 회전까지 고려 => 여기서 이동할 곳이 없다? 그것은 마지막 위치라는 뜻!
        elif direction == 1:
            move_available = 1
            for i in range(3):
                # 골렘의 동쪽부로 이동 => y에 +1
                nx, ny = x + dx[i], y + dy[i] + 1

                if nx >= R or ny >= C or ny < 0:
                    move_available = 0
                    continue

                # 골렘이 위치하고 있을 경우 이동 불가
                if graph[nx][ny] != 0:
                    move_available = 0

            for i in 1, 2:
                nx, ny = x + dx[i] + 1, y + dy[i] + 1

                if nx >= R or ny >= C or ny < 0:
                    move_available = 0
                    continue

                # 골렘이 위치하고 있을 경우 이동 불가
                if graph[nx][ny] != 0:
                    move_available = 0

            # door 위치 회전시키기~
            if move_available:
                q.append((x + 1, y + 1, 2))

                door += 1
                if door == 4:
                    door = 0

            # 여기가 골렘의 종착지!!
            else:
                # 큐에 넣어주는게 아닌 골렘 위치, door 위치 그려주기~
                graph[x][y] = number
                for i in range(4):
                    nx, ny = x + dx[i], y + dy[i]
                    graph[nx][ny] = number

                if door == 0:
                    door_position[x-1][y] = number
                elif door == 1:
                    door_position[x][y+1] = number
                elif door == 2:
                    door_position[x+1][y] = number
                else:
                    door_position[x][y-1] = number

                # 최종 골렘 중심부 위치
                return x, y


def move_angel(x, y):

    angel_graph = [[0 for _ in range(C)] for _ in range(R)]

    q = deque()

    q.append((x,y))

    angel_graph[x][y] = 1

    while q:
        x, y = q.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx >= R or nx < 0 or ny >= C or ny < 0:
                continue

            if graph[nx][ny] == 0:
                continue

            if angel_graph[nx][ny] == 1:
                continue

            # 다른 골렘으로 넘어갈 생각임.
            if graph[nx][ny] != graph[x][y]:
                if door_position[x][y] != 0:
                    angel_graph[nx][ny] = 1
                    q.append((nx, ny))

            else:
                angel_graph[nx][ny] = 1
                q.append((nx, ny))

    for i in range(R):
        for j in range(C):
            if angel_graph[R - 1 - i][j] == 1:
                return R - i


def main():
    global graph
    global door_position

    total_point = 0

    for number in range(1, K+1):

        start, door = map(int, input().split())

        # graph의 위치에서 -1 해줘야함
        start -= 1

        # 골렘을 이동시킴, return은 골렘의 중앙 포지션
        x, y = move(number, start, door)

        # 골렘이 바깥에 있다는 뜻으로 그래프를 완전히 초기화 해야 한다.
        if x <= 0 :
            graph = [[0 for _ in range(C)] for _ in range(R)]
            door_position = [[0 for _ in range(C)] for _ in range(R)]
            continue

        # 정령 이동 및 점수 계산
        point = move_angel(x, y)

        total_point += point

    print(total_point)







main()