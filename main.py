import PySimpleGUI as sg
import random

sg.theme("lightBlue2")

map = [[0 for _ in range(9)] for _ in range(9)]  # 2次元リスト1ならそこは地雷
map2 = [[0 for _ in range(9)] for _ in range(9)]
map3 = [[0 for _ in range(9)] for _ in range(9)]  # 2次元リスト1なら開いてる

todo_list = []
chacked = []

game_mode = False


def set_mines(x, y):
    global game_mode, map, map2, map3
    num_mines = 0
    while num_mines < 1:
        xx = random.randint(0, 8)
        yy = random.randint(0, 8)
        if map[xx][yy] == 0 and (1 < abs(xx - x) and 1 < abs(yy - y)):
            map[xx][yy] = 1
            num_mines += 1

    for x in range(9):
        for y in range(9):
            map2[x][y] = sum(
                map[xx][yy]
                for xx in range(max(0, x - 1), min(9, x + 2))
                for yy in range(max(0, y - 1), min(9, y + 2))
            )


layout = [
    [sg.T("00:00", k="txt1"), sg.T("⌚10", k="btn2")],
    [[sg.Button("?", k=f"b{x}{y}", size=(4, 2)) for x in range(9)] for y in range(9)],
]
win = sg.Window("マインスイーパー", layout, font=(None, 9), size=(400, 400), element_padding=(0, 0), finalize=True)


def chack():
    global game_mode, todo_list, chacked
    x = int(event[1])
    y = int(event[2])
    if not game_mode:
        for yy in range(9):
            for xx in range(9):
                win[f"b{xx}{yy}"].update("?")
        set_mines(x, y)
        game_mode = True
    if map[x][y] == 1:
        for y in range(9):
            for x in range(9):
                win[f"b{x}{y}"].update("!" if map[x][y] == 1 else f"{map2[x][y]}")
        game_mode = False
    elif map2[x][y] == 0:
        todo_list = [(x, y)]
        chacked = []
        expand()
    else:
        win[f"b{x}{y}"].update(f"{map2[x][y]}")
        map3[x][y] = 1


def expand():
    global todo_list, chacked
    count = 0
    while 0 < len(todo_list):
        count += 1
        if 20 < count:
            break
        (todo_x, todo_y) = todo_list[0]
        todo_list = todo_list[1:]
        if (todo_x, todo_y) in chacked:
            continue
        chacked.append((todo_x, todo_y))
        # todo_x, todo_yの周りを調べる
        for xx in range(max(0, todo_x - 1), min(9, todo_x + 2)):
            for yy in range(max(0, todo_y - 1), min(9, todo_y + 2)):
                if map2[xx][yy] == 0:
                    win[f"b{xx}{yy}"].update("")
                    todo_list.append((xx, yy))  # 必要なら新しい座標をtodo_listに追加
                else:
                    win[f"b{xx}{yy}"].update(f"{map2[xx][yy]}")
                map3[xx][yy] = 1
        # todo_listがから強制終了


while True:
    if 0 < len(todo_list):
        event, y = win.read(timeout=1)
        expand()
    else:
        event, values = win.read()
        if event is None:
            break
        chack()
        # map3の中の1の数すなわち合計
        total = sum(map3[y][x] for y in range(9) for x in range(9))
        if total == 71:
            win["txt1"].update("クリア！")
            game_mode = False

win.close()
