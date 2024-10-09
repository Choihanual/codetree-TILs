from math import inf
from collections import deque

N, M, K = map(int, input().split())

graph = [[0 for _ in range(M+1)] for _ in range(N+1)]

for i in range(1, N + 1):
    graph[i] = [0] + list(map(int, input().split()))

# 우, 하, 좌, 상, 오른쪽 위, 오른쪽 아래, 왼쪽 아래, 왼쪽 위
dx = [0, 1, 0, -1, -1, +1, +1, -1]
dy = [1, 0, -1, 0, +1, +1, -1, -1]

# 가장 최근한 공격한 포탑이 0에 더 가깝다 => 공격자 포탑만 0으로 초기화 해줌 나머지는 계속 +1
attack_history = [[0 for _ in range(M+1)] for _ in range(N+1)]

# 턴마다 공격과 상관있는 포탑의 position들
relative_attack = []

# 부서지지 않은 포탑 중 가장 약한 포탑을 선정해주는 함수.
def select_attack():
    attacker = []
    min_attack = inf
    for i in range(1, N+1):
        for j in range(1, M+1):

            # 죽은 포탑 제외
            if graph[i][j] <= 0:
                continue

            # 공격력이 작으면 가장 약한 포탑
            if min_attack > graph[i][j]:
                attacker = [i, j]
                min_attack = graph[i][j]

            elif min_attack == graph[i][j]:
                # 가장 최근에 공격한 포탑
                if attack_history[attacker[0]][attacker[1]] > attack_history[i][j]:
                    attacker = [i, j]
                    min_attack = graph[i][j]

                elif attack_history[attacker[0]][attacker[1]] == attack_history[i][j]:

                    # 행과 열의 합이 가장 큰 포탑
                    if attacker[0] + attacker[1] < i + j:
                        attacker = [i, j]
                        min_attack = graph[i][j]

                    elif attacker[0] + attacker[1] == i + j:

                        # 열이 가장 큰 포탑
                        if attacker[1] < j:
                            attacker = [i, j]
                            min_attack = graph[i][j]

    return attacker


# 공격자 제외 가장 강한 포탑을 정하기
def select_target(attacker):

    target = []
    max_attack = 0
    for i in range(1, N+1):
        for j in range(1, M+1):

            # 공격자 제외
            if i == attacker[0] and j == attacker[1]:
                continue

            # 죽은 포탑 제외
            if graph[i][j] <= 0:
                continue

            # 공격력이 크면 가장 강한 포탑
            if max_attack < graph[i][j]:
                target = [i, j]
                max_attack = graph[i][j]

            elif max_attack == graph[i][j]:
                # 가장 예전에 공격한 포탑
                if attack_history[target[0]][target[1]] < attack_history[i][j]:
                    target = [i, j]
                    max_attack = graph[i][j]

                elif attack_history[target[0]][target[1]] == attack_history[i][j]:

                    # 행과 열의 합이 가장 작은 포탑
                    if target[0] + target[1] > i + j:
                        target = [i, j]
                        max_attack = graph[i][j]

                    elif target[0] + target[1] == i + j:

                        # 열이 가장 작은 포탑
                        if target[1] > j:
                            target = [i, j]
                            max_attack = graph[i][j]

    return target

# 최단거리 bfs 로직
def rasor_attack(attacker, target):
    # 지나간 위치 기록을 위한 track이 필요
    track = []

    visit = [[0 for _ in range(M+1)] for _ in range(N+1)]

    q = deque()

    q.append(attacker)

    # 공격자는 방문한 상태로 시작
    visit[attacker[0]][attacker[1]] = 1

    rasor_available = 0
    while q:
        position = q.popleft()

        # 목표지점에 도착(이 때의 track이 필요)
        if position == target:
            rasor_available = 1

            break

        for i in range(4):
            nx, ny = position[0] + dx[i], position[1] + dy[i]

            # 반대편 격자로 넘어가는 로직
            if nx < 1:
                nx = N
            elif nx > N:
                nx = 1

            if ny < 1:
                ny = M
            elif ny > M:
                ny = 1

            # 이미 방문된 포탑은 못가요
            if visit[nx][ny] == 1:
                continue

            # 부서진 포탑이 아니면
            if graph[nx][ny] > 0:
                q.append([nx, ny])
                visit[nx][ny] = 1
                track.append([position, [nx, ny]])

    # 레이저 공격 불가능
    if rasor_available == 0:
        return False

    # 레이저 공격 효과 적용

    # 직접 대상은 온전한 피해
    graph[target[0]][target[1]] -= graph[attacker[0]][attacker[1]]

    track_target = [target[0], target[1]]
    # 레이저 길에 있던 애들은 절반의 피해
    for i in range(len(track)):
        if track[len(track) - 1 - i][0] == attacker:
            break

        # 거꾸로 탐색
        if track[len(track) - 1 - i][1] == track_target:
            graph[track[len(track) - 1 - i][0][0]][track[len(track) - 1 - i][0][1]] -= graph[attacker[0]][attacker[1]]//2
            relative_attack.append([track[len(track) - 1 - i][0][0], track[len(track) - 1 - i][0][1]])
            track_target = track[len(track) - 1 - i][0]



    return True


def tank_attack(attacker, target):

    graph[target[0]][target[1]] -= graph[attacker[0]][attacker[1]]
    for i in range(8):
        nx, ny = target[0] + dx[i], target[1] + dy[i]

        # 반대편 격자로 넘어가는 로직
        if nx < 1:
            nx = N
        elif nx > N:
            nx = 1

        if ny < 1:
            ny = M
        elif ny > M:
            ny = 1

        # 부서진 포탑
        if graph[nx][ny] <= 0:
            continue

        if nx == attacker[0] and ny == attacker[1]:
            continue

        graph[nx][ny] -= graph[attacker[0]][attacker[1]]//2
        relative_attack.append([nx, ny])

    return True

def main():
    global relative_attack

    # K 번의 턴 반복
    for _ in range(K):
        # 공격자 선정 및 공격자 위치 return
        attacker = select_attack()

        # 공격자의 공격력 증가
        graph[attacker[0]][attacker[1]] += M+N

        # 공격자 제외 가장 강한 포탑 위치 return
        target = select_target(attacker)

        relative_attack.append(attacker)
        relative_attack.append(target)

        # 레이저 공격부터 진행
        result = rasor_attack(attacker, target)



        # 레이저 공격 불가일 경우 포탄 공격
        if result == False:
            tank_attack(attacker, target)

        # 만약 남은 포탑이 1개이면 종료
        live_count = 0
        for i in range(1, N+1):
            for j in range(1, M+1):
                if graph[i][j] > 0:
                    live_count += 1

        if live_count == 1:
            break

        # 공격과 관련없는 포탑 +1
        for i in range(1, N+1):
            for j in range(1, M+1):
                # 망가진 포탑은 넘어가
                if graph[i][j] <= 0:
                    continue

                if [i, j] in relative_attack:
                    continue

                graph[i][j] += 1

        relative_attack = []

        # 공격자를 attack_history에 초기화 해주고 나머지 +1 로직 추가
        for i in range(1, N+1):
            for j in range(1, M+1):
                attack_history[i][j] += 1

        attack_history[attacker[0]][attacker[1]] = 0



    max_attack = 0
    for i in range(1, N+1):
        for j in range(1, M+1):
            if graph[i][j] > max_attack:
                max_attack = graph[i][j]

    print(max_attack)

main()