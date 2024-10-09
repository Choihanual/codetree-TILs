from math import inf

N, M, K = map(int, input().split())
maze = []

for _ in range(N):
    maze.append(list(map(int, input().split())))

player = []
player_record = [0]*M
winner = [0] * M

for _ in range(M):
    player.append(list(map(int, input().split())))

door = list(map(int, input().split()))

# 상, 하, 좌, 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 모든 참가자가 동시에 움직인다.
def move_player():
    # player 수만큼
    for i in range(M):
        # 이미 탈출한 친구들은 이동불가
        if winner[i] == 1:
            continue

        min_dis = abs(player[i][0] - door[0]) + abs(player[i][1] - door[1])
        position = []

        for j in range(4):
            nx = player[i][0] + dx[j]
            ny = player[i][1] + dy[j]

            # 미로 밖은 제외
            if nx < 1 or nx > N or ny < 1 or ny > N:
                continue

            # 미로는 (0,0) 부터 시작...
            # 벽의 위치로는 이동 불가
            if maze[nx - 1][ny - 1] > 0:
                continue

            # 이전 길이보다 작은 경우에만 이동
            if min_dis > abs(nx - door[0]) + abs(ny - door[1]):
                min_dis = abs(nx - door[0]) + abs(ny - door[1])
                position = [nx, ny]

        # 이동한 경우에만 player 위치 update
        if len(position) != 0:
            player[i][0] = position[0]
            player[i][1] = position[1]

            # 이동거리는 이동할 시 +1 하기
            player_record[i] += 1

            # 출구에 도달했다면 탈출 시켜버리기!
            if player[i][0] == door[0] and player[i][1] == door[1]:
                winner[i] = 1

def rotate_target():
    # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 찾기
    # 출구, 참가자를 포함한 가장 작은 정사각형 구하기
    # 길이 2부터 시작하는 정사각형 브루트포스
    for i in range(2, N + 1):

        for j in range(0, N + 1 - i):
            for k in range(0, N + 1 - i):
                is_door = 0
                is_player = 0

                for x in range(j, j + i):
                    for y in range(k, k + i):
                        # 출구를 포함했는지 체크
                        if x == door[0] - 1 and y == door[1] - 1:
                            is_door = 1

                        # 참가자 포함했는지 체크
                        for p in range(M):

                            # 이미 탈출한 참가자는 넘어가기
                            if winner[p] == 1:
                                continue

                            if player[p][0] - 1 == x and player[p][1] - 1 == y:
                                is_player = 1


                # 둘 다 포함됐다면
                if is_door and is_player:

                    return j, j + i, k, k + i

#미로를 회전시키고 벽 내구도 깎기
def rotate_maze(x_start, x_end, y_start, y_end):
    n = x_end - x_start
    # 회전을 목표로 하는 미로 부분
    target = [row[y_start:y_end] for row in maze[x_start:x_end]]

    rotate_target = [[0 for _ in range(n)]for _ in range(n)]

    # 미로 회전 시키기
    for i in range(0, n):
        for j in range(0, n):
            rotate_target[j][n - i - 1] = target[i][j]

    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            maze[i][j] = rotate_target[i - x_start][j - y_start]

            # 벽 내구도 감소시키기
            if maze[i][j] > 0:
                maze[i][j] -= 1

    # 출구 회전 시키기
    new_door = [0, 0]
    new_door[0] = door[1] - 1 - y_start
    new_door[1] = n - (door[0] - 1 - x_start) - 1
    door[0] = new_door[0] + 1 + x_start
    door[1] = new_door[1] + 1 + y_start

    # 사람 회전 시키기
    for i in range(M):
        if player[i][0] - 1 >= x_start and player[i][0] - 1 < x_end and player[i][1] - 1 >= y_start and player[i][1] - 1 < y_end:
            new_player = [player[i][1] - 1 - y_start, n - (player[i][0] - 1 - x_start) - 1]
            player[i][0] = new_player[0] + 1 + x_start
            player[i][1] = new_player[1] + 1 + y_start


def main():
    for _ in range(K):

        # 모든 참가자 이동
        move_player()

        is_loser = 0
        for i in range(M):
            if winner[i] == 0:
                is_loser = 1

        if is_loser == 0:
            break

        # 미로 회전 대상 구하기
        x_start, x_end, y_start, y_end = rotate_target()

        rotate_maze(x_start, x_end, y_start, y_end)



    total_move = 0
    for i in range(M):
        total_move += player_record[i]

    print(total_move)
    print(door[0], door[1])


main()