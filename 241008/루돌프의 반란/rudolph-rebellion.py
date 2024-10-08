from math import inf

N, M, P, C, D = map(int, input().split())

ru = list(map(int, input().split()))
santa = []
santa_point = [0]*P
santa_life = [1]*P

for _ in range(P):
    santa.append(list(map(int, input().split())))

santa.sort()

# 상, 우, 하, 좌, 오른쪽 위, 오른쪽 아래, 왼쪽 아래, 왼쪽 위
dx = [-1, 0, 1, 0, -1, 1, 1, -1]
dy = [0, 1, 0, -1, 1, 1, -1, -1]

# 루돌프 움직임 함수
def ru_move():

    # 가장 가까운 거리 타겟 산타 지정
    min_dis = inf
    target_santa_id = 0

    for i in range(P):
        # 죽은 산타는 배제합니다.
        if santa_life[i] == 0:
            continue

        dis = (santa[i][1] - ru[0])**2 + (santa[i][2] - ru[1])**2

        if min_dis > dis:
            min_dis = dis
            target_santa_id = santa[i][0]
        elif min_dis == dis:
            if santa[i][1] > santa[target_santa_id - 1][1]:
                target_santa_id = santa[i][0]
            elif santa[i][1] == santa[target_santa_id - 1][1]:
                if santa[i][2] > santa[target_santa_id - 1][2]:
                    target_santa_id = santa[i][0]

    # 이동 후 가장 가까워지는 위치로 사슴 이동
    move_min_dis = inf
    direction = []

    for i in range(8):
        n_x = ru[0] + dx[i]
        n_y = ru[1] + dy[i]

        dis = (santa[target_santa_id-1][1] - n_x)**2 + (santa[target_santa_id - 1][2] - n_y)**2

        if move_min_dis > dis:
            move_min_dis = dis
            direction = [dx[i], dy[i]]

    return direction


def check_conflict(key, direction, conflict_id):
    # 산타끼리의 충돌~
    if key == "conflict":
        for i in range(P):
            if i == conflict_id - 1:
                continue

            # 충돌이 발생한 산타가 있다면!
            if santa[i][1] == santa[conflict_id - 1][1] and santa[i][2] == santa[conflict_id - 1][2]:

                santa[i][1] += direction[0]
                santa[i][2] += direction[1]


                # 게임판 밖으로 밀려난 산타들이 됩니다. 죽어용~
                if santa[i][1] < 1 or santa[i][1] > N or \
                        santa[i][2] < 1 or santa[i][2] > N:
                    santa_life[i] = 0

                check_conflict("conflict", direction, i + 1)

    else:
        conflict_santa_id = 0
        for i in range(P):
            if santa[i][1] == ru[0] and santa[i][2] == ru[1]:
                conflict_santa_id = santa[i][0]

        # 충돌 자체가 일어나질 않았어요!
        if conflict_santa_id == 0:
            return False

        # 루돌프 충돌의 경우 C칸만큼 밀려나고 C 점수 받음 => 기절로직 들어가야함
        if key == "ru":
            santa_point[conflict_santa_id - 1] += C
            santa[conflict_santa_id - 1][1] += direction[0] * C
            santa[conflict_santa_id - 1][2] += direction[1] * C
            santa_life[conflict_santa_id - 1] += 2

            # 게임판 밖으로 밀려난 산타들이 됩니다. 죽어용~
            if santa[conflict_santa_id - 1][1] < 1 or santa[conflict_santa_id -1][1] > N or santa[conflict_santa_id - 1][2] < 1 or santa[conflict_santa_id - 1][2] > N:
                santa_life[conflict_santa_id - 1] = 0

            check_conflict("conflict", direction, conflict_santa_id)

        # 산타의 충돌은 D칸만큼 그리고 D 점수 => 기절로직 들어가야함
        elif key == "santa":
            santa_point[conflict_santa_id - 1] += D
            santa[conflict_santa_id - 1][1] -= direction[0] * D
            santa[conflict_santa_id - 1][2] -= direction[1] * D
            santa_life[conflict_santa_id - 1] += 2

            if santa[conflict_santa_id - 1][1] < 1 or santa[conflict_santa_id -1][1] > N or santa[conflict_santa_id - 1][2] < 1 or santa[conflict_santa_id - 1][2] > N:
                santa_life[conflict_santa_id - 1] = 0

            direction[0] = -direction[0]
            direction[1] = -direction[1]

            check_conflict("conflict", direction, conflict_santa_id)



def santa_move(santa_id):
    # 정신 말짱한 산타만 움직여요~
    if santa_life[santa_id - 1] != 1:
        return False

    min_dis = (santa[santa_id - 1][1] - ru[0])**2 + (santa[santa_id - 1][2] - ru[1])**2
    direction = []
    for i in range(4):
        n_x = santa[santa_id - 1][1] + dx[i]
        n_y = santa[santa_id - 1][2] + dy[i]

        # 게임판 밖이면 땡~
        if 1 > n_x or n_x > N or 1 > n_y or n_y > N:
            continue


        # 다른 산타의 위치면 땡~
        is_santa = 0
        for j in range(P):
            if n_x == santa[j][1] and n_y == santa[j][2]:
                is_santa = 1

        if is_santa == 1:
            continue

        dis = (n_x - ru[0])**2 + (n_y - ru[1])**2

        if min_dis > dis:
            min_dis = dis
            direction = [dx[i], dy[i]]

    if len(direction) == 0:
        return False

    return direction


def main():
    global ru

    # 총 M번의 턴에 걸쳐서 게임이 진행됨
    for _ in range(M):

        # 루돌프의 이동 방향
        ru_direction = ru_move()



        ru[0] += ru_direction[0]
        ru[1] += ru_direction[1]


        check_conflict("ru", ru_direction, 0)

        # P번에 걸쳐 산타가 움직일 차례입니다.
        for i in range(P):
            santa_direction = santa_move(i + 1)

            if santa_direction == False:
                continue


            santa[i][1] += santa_direction[0]
            santa[i][2] += santa_direction[1]


            check_conflict("santa", santa_direction, 0)

        is_life = 0
        # 탈락 안 했으면 1점씩 더 주기~
        for i in range(P):
            if santa_life[i] >= 2:
                santa_life[i] -=1

            if santa_life[i] != 0:
                santa_point[i] += 1
                is_life += 1

        if is_life == 0:
            break

    for i in range(P):
        print(santa_point[i], end = ' ')


main()