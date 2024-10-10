n, m, h, k = map(int, input().split())

runner = []
runner_direction = [0] * m
runner_life = [1] * m

for _ in range(m):
    runner.append(list(map(int, input().split())))

# 도망자들의 초기 달리는 방향
for i in range(m):
    # 좌우로 움직이는 러너
    if runner[i][2] == 1:
        # 오른쪽 보고 시작
        runner_direction[i] = 1
    elif runner[i][2] == 2:
        # 아래쪽 보고 시작
        runner_direction[i] = 2

# 상, 우, 하, 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

tree = []
for _ in range(h):
    tree.append(list(map(int, input().split())))

# 술래의 위치
catcher = [n//2+1, n//2+1]

catcher_direction = 0
catcher_track_idx = 0
catcher_move_count = 0

catcher_reverse_flag = 0
# 상, 우, 하, 좌
right_direction = [0,1,2,3]
# 하, 우, 상, 좌
reverse_direction = [2, 1, 0, 3]

# 이동 경로를 미리 기입해두기
move_track = []
track_value = 0

for i in range(1, 2*n):
    # 마지막 도달
    if i == 2*n - 1:
        move_track.append(track_value)
        break

    # 홀수 일 때 증가
    if i % 2 != 0:
        track_value +=1
    move_track.append(track_value)




# 도망자들 움직이기
def runner_move():
    for i in range(m):
        # 잡힌 애들은 안 움직임~
        if runner_life == 0:
            continue

        # 술래와 거리가 3 이하인 도망자들만 이동
        if abs(runner[i][0] - catcher[0]) + abs(runner[i][1] - catcher[1]) <= 3:
            nx = runner[i][0] + dx[runner_direction[i]]
            ny = runner[i][1] + dy[runner_direction[i]]



            # 격자를 벗어날 경우 방향을 바꿔 주고 한칸 이동
            if nx < 1 or nx > n or ny < 1 or ny > n:
                # 위를 보고 있었을 경우
                if runner_direction[i] == 0:
                    runner_direction[i] = 2
                # 오른쪽
                elif runner_direction[i] == 1:
                    runner_direction[i] = 3
                # 아래
                elif runner_direction[i] == 2:
                    runner_direction[i] = 0
                # 왼쪽
                elif runner_direction[i] == 3:
                    runner_direction[i] = 1

                # 바뀐 방향으로 nx, ny 다시 구하기
                nx = runner[i][0] + dx[runner_direction[i]]
                ny = runner[i][1] + dy[runner_direction[i]]

                # 술래 만나면 이동 x
                if nx == catcher[0] and ny == catcher[1]:
                    continue

                # 이동
                runner[i][0] = nx
                runner[i][1] = ny

            # 격자를 안 벗어나면

            else:
                #만약 이동하려는 칸에 술래 있으면 안 움직임
                if nx == catcher[0] and ny == catcher[1]:
                    continue

                # 이동
                runner[i][0] = nx
                runner[i][1] = ny

# 술래 움직이기
def catcher_move():
    global catcher_move_count
    global catcher_track_idx
    global catcher_reverse_flag
    global catcher_direction

    catcher_move_count += 1
    catcher[0] += dx[catcher_direction]
    catcher[1] += dy[catcher_direction]

    # 정방향
    if catcher_reverse_flag == 0:
        # 만약 같아 졌다면 방향 바꿔 주기
        if catcher_move_count == move_track[catcher_track_idx]:
            # reverse flag활성화
            if catcher_track_idx == 2 * n - 2:
                catcher_reverse_flag = 1
                catcher_move_count = 0
                catcher_direction = reverse_direction[0]

            else:
                catcher_track_idx += 1
                catcher_move_count = 0
                catcher_direction = (catcher_direction + 1) % 4

    # 역방향
    elif catcher_reverse_flag == 1:
        if catcher_move_count == move_track[catcher_track_idx]:
            # 다시 처음으로 돌아온다면
            if catcher_track_idx == 0:
                catcher_reverse_flag = 0
                catcher_move_count = 0
                catcher_direction = right_direction[0]

            else:
                catcher_move_count = 0
                catcher_track_idx -= 1

                catcher_direction -= 1
                if catcher_direction < 0:
                    catcher_direction = 3

# 술래 시야 3칸 이내의 숲에 없는 도망자들 잡기
def catch():
    count = 0
    # 3칸
    for i in range(3):
        nx = catcher[0] + dx[catcher_direction] * i
        ny = catcher[1] + dy[catcher_direction] * i

        # 격자 밖은 확인 x
        if nx < 1 or nx > n or ny < 1 or ny > n:
            continue

        # 숲 확인 x
        if [nx, ny] in tree:
            continue

        for j in range(m):

            #같을경우 잡음
            if runner[j][0] == nx and runner[j][1] == ny:
                count += 1
                runner_life[j] = 0


    return count


def main():
    total_count = 0
    for i in range(k):
        # 술래와 거리가 3 이하인 도망자들이 움직임
        runner_move()
        # 술래가 움직이기
        catcher_move()
        # 술래가 도망자를 잡아버리기
        count = catch()

        total_count += count * (i+1)

    print(total_count)

main()