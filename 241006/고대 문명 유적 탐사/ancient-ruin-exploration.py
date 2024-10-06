from collections import deque

K, M = map(int, input().split())


graph = []
for _ in range(5):
    graph.append(list(map(int, input().split())))

support_arr = deque(list(map(int, input().split())))

dx = [0,0,-1,1]
dy = [1,-1,0,0]


# cnt만큼 90도 회전 시킨 graph를 return 하는 함수
def rotate(x, y, cnt):

    # 새로운 rotate_graph 생성용~
    rotate_graph = [row[:] for row in graph]

    target = []

    for i in range(3):
        target.append([])
        for j in range(3):
            target[i].append(graph[x+i][y+j])

    rotate_target = [row[:] for row in target]

    # cnt 수만큼 회전
    for _ in range(cnt):

        for i in range(3):
            for j in range(3):
                rotate_target[j][2-i] = target[i][j]

        # 배열 깊은 복사
        target = [row[:] for row in rotate_target]


    for i in range(3):
        for j in range(3):
            rotate_graph[i+x][j+y] = target[i][j]

    return rotate_graph

# 회전된 graph의 point를 check하고 찾아진 유물 지운 graph와 점수를 return 하는 함수
def check_point(rotate_graph):

    point_graph = [row[:] for row in rotate_graph]
    visited = [[0 for _ in range(5)] for _ in range(5)]
    total_point = 0

    for i in range(5):
        for j in range(5):

            q = deque()
            q.append((i,j))

            trace = []
            trace.append((i,j))

            visited[i][j] = 1

            while q:
                x, y = q.popleft()



                for k in range(4):
                    new_x = x + dx[k]
                    new_y = y + dy[k]

                    if new_x < 0 or new_x >= 5 or new_y < 0 or new_y >= 5:
                        continue

                    if visited[new_x][new_y] == 0 and point_graph[new_x][new_y] == point_graph[x][y]:
                        trace.append((new_x, new_y))
                        visited[new_x][new_y] = 1
                        q.append((new_x,new_y))

            if len(trace) >= 3:
                total_point += len(trace)

                for m in range(len(trace)):
                    point_graph[trace[m][0]][trace[m][1]] = 0

    return point_graph, total_point



# 빈 유물 자리 채워주는 함수
def fill(max_graph):
    for i in range(5):
        for j in range(5):
            if max_graph[4 - j][i] == 0:
                max_graph[4 - j][i] = support_arr.popleft()

    return max_graph


def main():
    global graph
    # 총 K번 탐사
    for _ in range(K):

        max_graph = None
        max_point = 0

        # 90도씩 3번 회전 시키기
        for cnt in range(1, 4):

            # rotate 기준점 제시
            for x in range(3):
                for y in range(3):

                    # 열이 행보다 높은 기준 따라서 x, y 거꾸로 넣기
                    rotate_graph = rotate(y, x, cnt)

                    final_graph, point = check_point(rotate_graph)

                    if point > max_point:
                        max_graph = final_graph
                        max_point = point

        # 만약 더 이상 찾아지는 유물이 없으면 탐사 종료
        if max_graph is None:
            break

        while True:
            max_graph = fill(max_graph)

            max_graph, point = check_point(max_graph)

            if point == 0:
                break

            max_point += point

        graph = max_graph

        print(max_point, end = ' ')



main()