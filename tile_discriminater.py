# -*- coding: utf-8 -*-

import json
from tkinter import *


# ペイント後の色計算式、テラリアより抜粋し,python用に調整したもの
def after_paint_color(basecolor, paintcolor, wall):
    red = basecolor[0] / 255
    green = basecolor[1] / 255
    blue = basecolor[2] / 255

    if green > red:
        red = green
    if blue > red:
        num = red
        red = blue
        blue = num
    # Shadow
    if(paintcolor[0] == 25 and paintcolor[1] == 25 and paintcolor[2] == 25):
        shadow = blue * 0.3
        after_paint_red = int(paintcolor[0] * shadow)
        after_paint_green = int(paintcolor[1]* shadow)
        after_paint_blue = int(paintcolor[2] * shadow)
    # Negative
    if (paintcolor[0] == 200 and paintcolor[1] == 200 and paintcolor[2] == 200):
        # basecolor側の回転数がwall_startよりも多い場合は壁
        if  wall:
            after_paint_red = int((255 - basecolor[0]) * 0.5)
            after_paint_green = int((255 - basecolor[1]) * 0.5)
            after_paint_blue = int((255 - basecolor[2]) * 0.5)
        else:
            after_paint_red = int(255 - basecolor[0])
            after_paint_green = int(255 - basecolor[1])
            after_paint_blue = int(255 - basecolor[2])
    else:
        new_brightness = red
        after_paint_red = int(paintcolor[0] * new_brightness)
        after_paint_green = int(paintcolor[1] * new_brightness)
        after_paint_blue = int(paintcolor[2] * new_brightness)

    return [after_paint_red, after_paint_green, after_paint_blue]

# rgbを差し引いて絶対値判断して近い色のタイル名を返す
def tile_discrimination(r, g, b):
    input_color = [r, g, b]

    difference_score = [(abs(color[0] - input_color[0]) + abs(color[1] - input_color[1]) + abs(color[2] - input_color[2]))
         for color in all_color_list]
    # 最小スコアのインデックスがリストで表示される
    min_value = min(difference_score)
    near_value_index = [i for i, v in enumerate(difference_score) if v == min_value]

    return_tile = ''
    #　表示部分　リスト形式はtile + wall + tile(paint1) + wall(paint1) + tile(paint2)...
    for i in near_value_index:
        if i >= after_paint_start:
            paint_name = paint_list[int(i / after_paint_start) - 1]['name']
            reminder = i % after_paint_start
            if reminder >= wall_start:
                base_name = wall_list[reminder - wall_start]['name']
                return_tile += '(wall){} + {}Paint\n'.format(base_name, paint_name)
            else:
                base_name = tile_list[reminder]['name']
                return_tile += '(tile){} + {}Paint\n'.format(base_name, paint_name)
        elif i < wall_start:
            return_tile += '(tile){}\n'.format(tile_list[i]['name'])
        else:
            return_tile += '(wall){}\n'.format(wall_list[i - wall_start]['name'])

    return return_tile

class RgbInputFrame():
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
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
        self.button = Button(master, text = 'Search', command = self.send_command)
        self.button.pack()
        self.button.place(x = 150, y = 100)

    def send_command(self):
        r = int(self.r.get())
        g = int(self.g.get())
        b = int(self.b.get())
        self.label2 = Label(root, text = tile_discrimination(r, g, b), justify='left')
        self.label2.pack()
        self.label2.place(x = 50, y = 150)

import_json = json.load(open('MapColor.json'))

# jsonをtilesとwallsとPaintsに分割
tile_list = import_json['Tiles']
wall_list = import_json['Walls']
wall_start = len(tile_list)
paint_list = import_json['Paints']
sum_list = tile_list + wall_list

# 絶対値の比較用リスト
basecolor_list = [[int(color) for color in item['color'].split(',')] for item in sum_list]
paint_base_list = [[int(color) for color in paint['color'].split(',')] for paint in paint_list]
after_paint_list = [after_paint_color(basecolor_list[i], paint_base_list[j], i >= wall_start)
                    for j in range(len(paint_base_list))
                    for i in range(len(basecolor_list))]
after_paint_start = len(sum_list)
all_color_list = basecolor_list + after_paint_list
print(len(after_paint_list))


root = Tk()
root.title('Terraria Tile Discriminater')
root.geometry('350x500')
root.resizable(0, 1)
RgbInputFrame(root)
root.mainloop()
