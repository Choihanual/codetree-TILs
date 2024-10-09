L, N, Q = map(int, input().split())

graph = []

# 나이트들의 위치만을 나타내는 그래프를 그리기
knight_graph = [[0 for _ in range(L)] for _ in range(L)]


for _ in range(L):
    graph.append(list(map(int, input().split())))

knight = []
knight_damage = [0]*N

target_knight = []

for _ in range(N):
    knight.append(list(map(int, input().split())))



# 북, 동, 남, 서
# 0, 1, 2, 3
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


# 나이트 이동시키는 함수
def move(knight_id, direction):
    # global target_night

    # 이미 유령이 된 기사일 경우
    if knight[knight_id-1][4] <= 0:
        return False

    available_move = True

    knight_x = [knight[knight_id -1][0] - 1, knight[knight_id-1][0] - 1 + knight[knight_id-1][2]]
    knight_y = [knight[knight_id -1][1] - 1, knight[knight_id-1][1] - 1 + knight[knight_id-1][3]]

    # 원하는 방향으로 이동시키기
    knight_x[0] += dx[direction]
    knight_x[1] += dx[direction]
    knight_y[0] += dy[direction]
    knight_y[1] += dy[direction]


    if knight_x[0] < 0 or knight_x[1] > L or knight_y[0] < 0 or knight_y[1] > L:
        available_move = False
        return available_move


    # 벽에 걸릴 경우 이동 불가
    for i in range(knight_x[0], knight_x[1]):
        for j in range(knight_y[0], knight_y[1]):
            if graph[i][j] == 2:
                available_move = False
                return available_move


    for i in range(N):
        # 이미 유령이 된 기사는 대상에서 무시
        if knight[i][4] <= 0:
            continue

        if i != knight_id - 1:
            target_knight_x = [knight[i][0] - 1, knight[i][0] - 1 + knight[i][2]]
            target_knight_y = [knight[i][1] - 1, knight[i][1] - 1 + knight[i][3]]


            # 겹치는 경우 체크
            if knight_x[0] <= target_knight_x[0] and target_knight_x[0] < knight_x[1] or (target_knight_x[0] <= knight_x[0] and knight_x[0] < target_knight_x[1]):
                if (knight_y[0] <= target_knight_y[0] and target_knight_y[0] < knight_y[1]) or (target_knight_y[0] <= knight_y[0] and knight_y[0] < target_knight_y[1]):


                    target_knight.append(i + 1)
                    result = move(i+1, direction)

                    if result == False:
                        available_move = False
                        return available_move

    # knight[knight_id - 1][0] = knight_x[0] + 1
    # knight[knight_id - 1][1] = knight_y[0] + 1

    return available_move

def cal_damage(knight_id):
    for i in target_knight:
        if i == knight_id:
            continue

        damage = 0
        for x in range(knight[i -1][0] - 1, knight[i-1][0] - 1 + knight[i-1][2]):
            for y in range(knight[i -1][1] - 1, knight[i-1][1] - 1 + knight[i-1][3]):
                if graph[x][y] == 1:
                    damage += 1

        knight[i - 1][4] -= damage
        knight_damage[i - 1] += damage



def real_move(knight_id, direction):

    knight[knight_id-1][0] += dx[direction]
    knight[knight_id-1][1] += dy[direction]

    for i in target_knight:
        knight[i-1][0] += dx[direction]
        knight[i-1][1] += dy[direction]


def main():
    global target_knight
    for _ in range(Q):
        knight_id, direction = map(int, input().split())

        move_check_result = move(knight_id, direction)

        # 이동했을 경우에만 기사의 체력을 감소시키면 된다.
        if move_check_result == True:
            target_knight = set(target_knight)

            real_move(knight_id, direction)
            cal_damage(knight_id)



        target_knight = []



    total_damage = 0
    for i in range(N):
        if knight[i][4] > 0:
            total_damage += knight_damage[i]

    print(total_damage)

main()