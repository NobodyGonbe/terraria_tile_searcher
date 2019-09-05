# -*- coding: utf-8 -*-

import json
from tkinter import *


# ペイント後の色計算式、テラリアより抜粋し,python用に調整したもの
# base_color(タイル + 壁の色リスト) paint_color(ペンキの色リスト) painted(着色されたタイルと壁)
def painted_color(base_color, paint_color, wall):
    red = base_color[0] / 255
    green = base_color[1] / 255
    blue = base_color[2] / 255

    if green > red:
        red = green
    if blue > red:
        num = red
        red = blue
        blue = num

    # Shadow
    if(paint_color[0] == 25 and paint_color[1] == 25 and paint_color[2] == 25):
        shadow = blue * 0.3
        painted_red = int(paint_color[0] * shadow)
        painted_green = int(paint_color[1]* shadow)
        painted_blue = int(paint_color[2] * shadow)
    # Negative
    if (paint_color[0] == 200 and paint_color[1] == 200 and paint_color[2] == 200):
        if  wall:
            painted_red = int((255 - base_color[0]) * 0.5)
            painted_green = int((255 - base_color[1]) * 0.5)
            painted_blue = int((255 - base_color[2]) * 0.5)
        else:
            painted_red = int(255 - base_color[0])
            painted_green = int(255 - base_color[1])
            painted_blue = int(255 - base_color[2])
    else:
        new_brightness = red
        painted_red = int(paint_color[0] * new_brightness)
        painted_green = int(paint_color[1] * new_brightness)
        painted_blue = int(paint_color[2] * new_brightness)

    return [painted_red, painted_green, painted_blue]


# rgbの差分を判断して近い色のタイル名を返す
def select_tile_combination(r, g, b):

    # 差分のスコアが一番小さいもののインデックスを作成
    input_color = [r, g, b]
    score = [(abs(color[0] - input_color[0]) + abs(color[1] - input_color[1]) + abs(color[2] - input_color[2]))
             for color in map_color_list]
    min_score = min(score)
    min_score_index = [i for i, v in enumerate(score) if v == min_score]

    # インデックスよりタイルの名前判別　リスト形式はtile + wall + tile(paint1) + wall(paint1) + tile(paint2)...
    name = []
    for i in min_score_index:
        if i >= paint_start:
            paint_name = '+{}Paint'.format(paint_dictionary[int(i / paint_start) - 1]['name'])
        else:
            paint_name = ''

        target_index = i % paint_start
        target_item = base_color_dictionary[target_index]['name']
        if target_index >= wall_start:
            tile_type = 'wall'
        else:
            tile_type = 'tile'

        name += ['({}){}{}\n'.format(tile_type, target_item, paint_name)]

    # 検索上位5件を表示
    return_name = ''
    for i in range(len(name)):
        if i < 5:
            return_name += name[i]
        else:
            break

    return return_name

class RgbInputFrame():
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.txt = StringVar()
        self.txt.set('値を入力してください')

        self.description = Label(master, text = 'RGBを入力するとマップカラーで近い色のタイルを返します。')
        self.description.pack()
        self.description.place(x = 30, y = 10)
        self.label1 = Label(master, text = 'R(レッド)       G（グリーン）        B（ブルー）')
        self.label1.pack()
        self.label1.place(x = 70, y = 30)
        self.r = Entry(master, width = 5)
        self.r.pack()
        self.r.place(x = 70, y = 60)
        self.g = Entry(master, width = 5)
        self.g.pack()
        self.g.place(x = 150, y = 60)
        self.b = Entry(master, width = 5)
        self.b.pack()
        self.b.place(x = 230, y = 60)
        self.button = Button(master, text = 'Search', command = self.change_label)
        self.button.pack()
        self.button.place(x = 150, y = 100)
        self.label2 = Label(master, textvariable  = self.txt, justify='left')
        self.label2.pack()
        self.label2.place(x = 50, y = 150)

    def send_message(self):
        r = int(self.r.get())
        g = int(self.g.get())
        b = int(self.b.get())
        return select_tile_combination(r, g, b)

    def change_label(self):
        self.txt.set(self.send_message())


data = json.load(open('MapColor.json'))
paint_dictionary = data['Paints']
base_color_dictionary = data['Tiles'] + data['Walls']
wall_start = len(data['Tiles'])
paint_start = len(base_color_dictionary)
base_color_list = [[int(color) for color in item['color'].split(',')] for item in base_color_dictionary]
paint_color_list = [[int(color) for color in paint['color'].split(',')] for paint in paint_dictionary]
painted_list = [painted_color(base_color_list[i], paint_color_list[j], i >= wall_start)
                    for j in range(len(paint_color_list))
                    for i in range(len(base_color_list))]
map_color_list = base_color_list + painted_list


if __name__ == '__main__':
    root = Tk()
    root.title('Terraria Tile Discriminater')
    root.geometry('350x250')
    RgbInputFrame(root)
    root.mainloop()
