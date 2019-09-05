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


 # 差分のスコアが一番小さいもののインデックスを作成
def return_min_scores(r, g, b):
    input_color = [r, g, b]
    scores = [(abs(color[0] - input_color[0]) + abs(color[1] - input_color[1]) + abs(color[2] - input_color[2]))
             for color in map_colors]
    min_scores = min(scores)
    min_scores_index = [i for i, v in enumerate(scores) if v == min_scores]
    return min_scores_index


# インデックスよりタイルの名前判別　リスト形式はtile + wall + tile(paint1) + wall(paint1) + tile(paint2)...
def select_tile_combination(r, g, b):
    names = []
    num = return_min_scores(r, g, b)
    for i in num:
        if i >= paint_start:
            paint_name = '+{}Paint'.format(paint_dictionary[int(i / paint_start) - 1]['name'])
        else:
            paint_name = ''

        target_index = i % paint_start
        target_item = base_dictionary[target_index]['name']
        if target_index >= wall_start:
            tile_type = 'wall'
        else:
            tile_type = 'tile'

        names += ['({}){}{}\n\n'.format(tile_type, target_item, paint_name)]

    # 検索上位5件を表示
    return_names = ''
    for i in range(len(names)):
        if i < 5:
            return_names += names[i]
        else:
            break

    return return_names

class RgbInputFrame():
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.txt = StringVar()
        self.txt.set('')

        self.description = Label(master, text = '好きな色を選択してserchを押してください')
        self.description.pack()
        self.description.place(x = 30, y = 10)

        self.lbl1 = Label(master, text='red')
        self.lbl1.pack()
        self.lbl1.place(x = 160, y = 50)
        self.lbl2 = Label(master, text='green')
        self.lbl2.pack()
        self.lbl2.place(x = 160, y = 90)
        self.lbl3 = Label(master, text='blue')
        self.lbl3.pack()
        self.lbl3.place(x = 160, y = 130)

        self.scrl1 = Scale(master, orient = HORIZONTAL, to = 255, command = self.scrl_method)
        self.scrl1.pack()
        self.scrl1.place(x = 200, y = 30)
        self.scrl2 = Scale(master, orient = HORIZONTAL, to = 255, command = self.scrl_method)
        self.scrl2.pack()
        self.scrl2.place(x = 200, y = 70)
        self.scrl3 = Scale(master, orient = HORIZONTAL, to = 255, command = self.scrl_method)
        self.scrl3.pack()
        self.scrl3.place(x = 200, y = 110)

        self.cvs = Canvas(master, bg = '#000000', width = 100, height = 100)
        self.cvs.pack()
        self.cvs.place(x = 30, y = 50)
        self.cvs1 = Canvas(master, width = 10, height = 10)
        self.cvs1.pack()
        self.cvs1.place(x = 30, y = 225)
        self.cvs2 = Canvas(master, width = 10, height = 10)
        self.cvs2.pack()
        self.cvs2.place(x = 30, y = 255)
        self.cvs3 = Canvas(master, width = 10, height = 10)
        self.cvs3.pack()
        self.cvs3.place(x = 30, y = 285)
        self.cvs4 = Canvas(master, width = 10, height = 10)
        self.cvs4.pack()
        self.cvs4.place(x = 30, y = 315)
        self.cvs5 = Canvas(master, width = 10, height = 10)
        self.cvs5.pack()
        self.cvs5.place(x = 30, y = 345)

        self.button = Button(master, text = 'Search', command = self.change_label)
        self.button.pack()
        self.button.place(x = 150, y = 180)

        self.label4 = Label(master, textvariable = self.txt, justify = 'left')
        self.label4.pack()
        self.label4.place(x = 45, y = 220)

    def hexadecimal(self, rgb):
        num = hex(rgb).replace('0x', '')
        if len(num) == 1:
            num = '0' + num
        return num

    def rgb_to_html_color(self, r, g, b):
        color = '#' + '{}{}{}'.format(self.hexadecimal(r), self.hexadecimal(g), self.hexadecimal(b))
        return color


    def scrl_method(self, event):
        r = self.scrl1.get()
        g = self.scrl2.get()
        b = self.scrl3.get()
        html_color = self.rgb_to_html_color(r, g, b)
        self.cvs.configure(bg = html_color)

    def send_message(self):
        r = self.scrl1.get()
        g = self.scrl2.get()
        b = self.scrl3.get()
        return select_tile_combination(r, g, b)

    def send_color(self):
        r = self.scrl1.get()
        g = self.scrl2.get()
        b = self.scrl3.get()
        index = return_min_scores(r, g, b)
        color1 = self.rgb_to_html_color(map_colors[index[0]][0], map_colors[index[0]][1], map_colors[index[0]][2])
        self.cvs1.configure(bg = color1)
        if  len(index) > 1 :
            color2 = self.rgb_to_html_color(map_colors[index[1]][0], map_colors[index[1]][1], map_colors[index[1]][2])
            self.cvs2.configure(bg = color2)
        if len(index) > 2:
            color3 = self.rgb_to_html_color(map_colors[index[2]][0], map_colors[index[2]][1], map_colors[index[2]][2])
            self.cvs3.configure(bg = color3)
        if len(index) > 3:
            color4 = self.rgb_to_html_color(map_colors[index[3]][0], map_colors[index[3]][1], map_colors[index[3]][2])
            self.cvs4.configure(bg = color4)
        if len(index) > 4:
            color5 = self.rgb_to_html_color(map_colors[index[4]][0], map_colors[index[4]][1], map_colors[index[4]][2])
            self.cvs5.configure(bg = color5)

    def change_label(self):
        self.txt.set(self.send_message())
        self.send_color()


data = json.load(open('MapColor.json'))
paint_dictionary = data['Paints']
base_dictionary = data['Tiles'] + data['Walls']
wall_start = len(data['Tiles'])
paint_start = len(base_dictionary)
base_colors = [[int(color) for color in item['color'].split(',')] for item in base_dictionary]
paint_colors = [[int(color) for color in paint['color'].split(',')] for paint in paint_dictionary]
painted_colors = [painted_color(base_colors[i], paint_colors[j], i >= wall_start)
                    for j in range(len(paint_colors))
                    for i in range(len(base_colors))]
map_colors = base_colors + painted_colors

if __name__ == '__main__':
    root = Tk()
    root.title('Terraria Tile Discriminater')
    root.geometry('340x400')
    RgbInputFrame(root)
    root.mainloop()