
global temp_board
global count
count = 0
temp_board = []


def calculate_ai_move(board, ai_player):
    global temp_board
    temp_board = board
    values = ai_player = 2 and -100000000 or 100000000
    record = [-1, -1]
    # 记录values最大的那步棋下的位置
    for i in range(15):
        for j in range(15):
            # 如果该点为空，假设下在该点，修改棋盘状态
            if temp_board[i][j] == 0:
                if judge_empty(i, j):
                    continue
                temp_board[i][j] = ai_player
                # 计算该下法的价值
                evaluate = ai(3 - ai_player, 1, values)
                if evaluate > values:
                    values = evaluate
                    record[0] = i
                    record[1] = j
                # 回溯
                temp_board[i][j] = 0
    print("record:{}".format(record))
    return record


# 如果该点周围米字方向上相邻的一格全都为空，就跳过该点
def judge_empty(m, n):
    global temp_board
    directions = [(-1, 0), (1, 0), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 1), (-1, -1)]
    count = 1  # 初始点本身
    for dx, dy in directions:
        for dist in range(1, 3):  # 检查每个方向上的两个位置
            x, y = m + dist * dx, n + dist * dy
            if 0 <= x < 15 and 0 <= y < 15:  # 确保在边界内
                if temp_board[x][y] == 0:  # 如果该位置为空
                    count += 1
                else:
                    break  # 如果非空，停止当前方向的检查
            else:
                break  # 如果超出边界，停止当前方向的检查

    return count == 17  # 如果所有检查的位置都是空的，返回 True


def ai(color, deep, pre_evaluate):
    global count
    global temp_board
    # 递归边界
    if deep >= 2:
        temp = evaluateBoard(2, temp_board) - evaluateBoard(1, temp_board)
        # print("{}:{}".format(deep, temp))
        return temp
    # values初始值
    if color == 2:
        values = -100000000
    else:
        values = 100000000

    # 记录values最大的那步棋下的位置
    for i in range(15):
        for j in range(15):

            # 如果该点为空，假设下在该点，修改棋盘状态
            if temp_board[i][j] == 0:
                # 如果该点周围米字方向上两格都为空，就跳过该点
                if judge_empty(i, j):
                    continue
                temp_board[i][j] = color
                # 递归评估
                evaluate = ai(3-color, deep+1, values)
                print("i,j,value:{},{},{}".format(i, j, evaluate))
                if color == 2:
                    # 剪枝，如果当前的评估值比最小的pre_evaluate要大就跳过该情况，注意要回溯
                    if evaluate > pre_evaluate:
                        # 回溯
                        temp_board[i][j] = 0
                        count += 1
                        return 100000000
                else:
                    # 剪枝，如果当前的评估值比最大的pre_evaluate要小就跳过该分支，注意要回溯
                    if evaluate < pre_evaluate:
                        # 回溯
                        temp_board[i][j] = 0
                        count += 1
                        return -100000000
                # 如果是白子回合，应当取评估值的最大值
                if color == 2:
                    # #如果当前白子下法能完成五连，则将evaluate设一个较大的值
                    # if self.judge(i,j):
                    #     evaluate = 10000000
                    if evaluate >= values:
                        values = evaluate
                # 如果是黑子回合，应当取评估值的最小值
                else:
                    if evaluate <= values:
                        values = evaluate
                # 回溯
                temp_board[i][j] = 0
    # print("{}:{}".format(deep,values))
    return values


# 这个函数是评价当前棋盘上仅考虑某一种颜色的得分
# 想要得到考虑双方棋子的得分，就是自己得分减去对方得分即可evaluateBoard(1) - evaluateBoard(2)
# color 1-black 2-white
def evaluateBoard(color, chessboard):
    values = 0
    directions = [(-1, 0), (1, 0), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 1), (-1, -1)]
    directions_2 = [(1, 0), (1, -1), (0, 1), (1, 1)]
    for row in range(15):
        for col in range(15):
            # 如果当前棋子不是color对应的棋子就跳过
            if chessboard[row][col] != color:
                continue
            # 五个棋子，每一个都会被计算一次，所以如果出现五连，那么最后的values相当于加上5*200000
            j = 0
            while j < len(directions):
                count = 1
                a = 0
                # 记录中止原因
                record = []
                # 循环两次，分别判断两个相对的方向
                while a <= 1:
                    x, y = row, col
                    a += 1
                    for i in range(4):
                        if x + directions[j][0] < 0 or x + directions[j][0] > 14 or y + directions[j][1] < 0 or y + directions[j][1] > 14 - 1:
                            # 超过边界相当于被另一棋子堵住
                            record.append(3-color)
                            break
                        x += directions[j][0]
                        y += directions[j][1]
                        if chessboard[x][y] == chessboard[row][col]:
                            count += 1
                        else:
                            # 若当前方向上出现另一颜色棋子或者没有棋子，中止该方向的判断
                            # 记录该次中止原因
                            record.append(chessboard[x][y])
                            break
                    j += 1
                # 如果在米子方向上有连续5个子，则
                # values += 200000;
                if count >= 5:
                    values += 200000
                elif count == 4:
                    # print("4中止原因：{}".format(record))
                    # 如果有连续4个子并且两边都没有堵住，则
                    # values += 70000;
                    if record[0] == record[1] == 0:
                        values += 70000
                    # 如果同一个方向有连续4个子并且仅有一边被堵住，则
                    # values += 4000;
                    elif (record[0] == 0 and record[1] == (3-color)) or (record[0] == (3-color) and record[1] == 0):
                        values += 1000
                elif count == 3:
                    # print("3中止原因：{}".format(record))
                    # 如果是“活三”的情况，则values += 3000
                    if record[0] == record[1] == 0:
                        values += 1000
                    # 如果是“活三”被堵住了一边，则values += 500;
                    elif (record[0] == 0 and record[1] == (3-color)) or (record[0] == (3-color) and record[1] == 0):
                        values += 150
                elif count == 2:
                    # print("2中止原因：{}".format(record))
                    # 如果连续两个子且两边没有被堵住，values += 2000;
                    if record[0] == record[1] == 0:
                        values += 1000
                    # 如果连续两个子被堵住一边，values += 300;
                    elif (record[0] == 0 and record[1] == (3-color)) or (record[0] == (3-color) and record[1] == 0):
                        values += 150
                # 如果是 ** * 0 * 的情况，则values += 3000;
                # 如果是 ** 0 ** 的情况，则values += 2600;

                k = 0
                while k < len(directions_2):
                    x, y = row, col
                    record = []
                    record.append(chessboard[x][y])
                    # 向下，右，左下，右下，四个方向搜索4个格子
                    for i in range(4):
                        # 搜索一个格子，如果白棋和黑棋相邻，values += 10确保白棋第一棋下在黑棋旁边
                        if i == 1 and len(record) == 2:
                            if record[0] != record[1] and record[0] and record[1]:
                                values += 10
                        if x + directions_2[k][0] < 0 or x + directions_2[k][0] > 14 or y + directions_2[k][
                                1] < 0 or y + directions_2[k][1] > 14:
                            break
                        x += directions_2[k][0]
                        y += directions_2[k][1]
                        record.append(chessboard[x][y])
                    if len(record) == 5:
                        count = record.count(0)
                        # 如果是 *** 0 * 或* 0 * **的情况，则values += 3000;
                        # 即record中0的个数为1，且record[1]或record[3]是0,record.count(color) == 4
                        if (count == 1 and record[1] == 0 and record.count(color) == 4) or (count == 1 and record[3] == 0 and record.count(color) == 4):
                            values += 3000
                            # print("*** 0 * 或* 0 * **:{}".format(record))
                        # 如果是 ** 0 ** 的情况，则values += 2600;
                        if count == 1 and record[2] == 0 and record.count(color) == 4:
                            values += 2600
                            # print("** 0 **:{}".format(record))
                    k += 1
    return values
