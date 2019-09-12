
# -*- coding: utf-8 -*-

import json
import os
from tkinter import *
import color_helper


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


 # 差分のスコアが小さいタイル5件を作成
def return_min_scores(r, g, b, target_color_list):
    input_color = [r, g, b]
    scores = [(available_matrices[config['matrix']](input_color, color), i) for i,
              color in enumerate(target_color_list)]
    min_scores_index = sorted(scores)[:5]
    return min_scores_index


# return_min_scoresのインデックスより名前を判別して返す
# リスト形式はtile + wall + tile(paint1) + wall(paint1) + tile(paint2)...
def select_tile_combination(r, g, b, target_color_list):
    names = ''
    num = return_min_scores(r, g, b, target_color_list)
    for i in num:
        if i[1] >= paint_start:
            paint_name = '+{}Paint'.format(paint_dictionary[int(i[1] / paint_start) - 1]['name'])
        else:
            paint_name = ''

        target_index = i[1] % paint_start
        target_item = base_dictionary[target_index]['name']
        if target_index >= wall_start:
            tile_type = 'wall'
        else:
            tile_type = 'tile'

        names += '({}){}{}\n\n'.format(tile_type, target_item, paint_name)
    return names

class RgbInputFrame():
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.txt = StringVar()
        self.txt.set('')
        self.bool1 = BooleanVar()
        self.bool1.set(True)

        self.description = Label(master, text = '検索したい色を選択してsearchボタンを押してください')
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
        self.cvs.place(x = 30, y = 45)
        self.cvs1 = Canvas(master, width = 20, height = 20)
        self.cvs1.pack()
        self.cvs1.place(x = 30, y = 240)
        self.cvs2 = Canvas(master, width = 20, height = 20)
        self.cvs2.pack()
        self.cvs2.place(x = 30, y = 270)
        self.cvs3 = Canvas(master, width = 20, height = 20)
        self.cvs3.pack()
        self.cvs3.place(x = 30, y = 300)
        self.cvs4 = Canvas(master, width = 20, height = 20)
        self.cvs4.pack()
        self.cvs4.place(x = 30, y = 330)
        self.cvs5 = Canvas(master, width = 20, height = 20)
        self.cvs5.pack()
        self.cvs5.place(x = 30, y = 360)

        self.CheckBox = Checkbutton(master, text = 'Paintを使用する',  variable = self.bool1)
        self.CheckBox.pack()
        self.CheckBox.place(x = 30, y = 160)

        self.button = Button(master, text = 'Search', command = self.change_label)
        self.button.pack()
        self.button.place(x = 150, y = 195)

        self.label4 = Label(master, textvariable = self.txt, justify = 'left')
        self.label4.pack()
        self.label4.place(x = 55, y = 240)

    def hexadecimal(self, rgb):
        num = hex(rgb).replace('0x', '')
        if len(num) == 1:
            num = '0' + num
        return num

    def rgb_to_html_color(self, r, g, b):
        color = '#' + '{}{}{}'.format(self.hexadecimal(r), self.hexadecimal(g), self.hexadecimal(b))
        return color

    def get_rgb(self):
        r = self.scrl1.get()
        g = self.scrl2.get()
        b = self.scrl3.get()
        return [r, g, b]

    def use_paint(self):
        if self.bool1.get():
            return map_colors
        else:
            return base_colors

    def scrl_method(self, event):
        html_color = self.rgb_to_html_color(self.get_rgb()[0], self.get_rgb()[1], self.get_rgb()[2])
        self.cvs.configure(bg = html_color)

    def send_message(self):
        return select_tile_combination(self.get_rgb()[0], self.get_rgb()[1],  self.get_rgb()[2], self.use_paint())

    def send_color(self):
        index = return_min_scores(self.get_rgb()[0], self.get_rgb()[1], self.get_rgb()[2], self.use_paint())
        color1 = self.rgb_to_html_color(map_colors[index[0][1]][0], map_colors[index[0][1]][1], map_colors[index[0][1]][2])
        self.cvs1.create_rectangle(0, 0, 25, 25, fill = color1)
        color2 = self.rgb_to_html_color(map_colors[index[1][1]][0], map_colors[index[1][1]][1], map_colors[index[1][1]][2])
        self.cvs2.create_rectangle(0, 0, 25, 25, fill = color2)
        color3 = self.rgb_to_html_color(map_colors[index[2][1]][0], map_colors[index[2][1]][1], map_colors[index[2][1]][2])
        self.cvs3.create_rectangle(0, 0, 25, 25, fill = color3)
        color4 = self.rgb_to_html_color(map_colors[index[3][1]][0], map_colors[index[3][1]][1], map_colors[index[3][1]][2])
        self.cvs4.create_rectangle(0, 0, 25, 25, fill = color4)
        color5 = self.rgb_to_html_color(map_colors[index[4][1]][0], map_colors[index[4][1]][1], map_colors[index[4][1]][2])
        self.cvs5.create_rectangle(0, 0, 25, 25, fill = color5)

    def change_label(self):
        self.cvs1.delete('all')
        self.cvs2.delete('all')
        self.cvs3.delete('all')
        self.cvs4.delete('all')
        self.cvs5.delete('all')
        self.txt.set(self.send_message())
        self.send_color()


# コンフィグの読み込みに失敗した時に投げられる
class BadConfigException(BaseException):
    'Raises when config load fails'

#検索に使用するリスト
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

# 計算関数名と関数のペア
available_matrices = {'absolute': lambda rgb1, rgb2: abs(rgb2[0] - rgb1[0]) + abs(rgb2[1] - rgb1[1]) + abs(rgb2[2] - rgb1[2]),
                      'euclid': color_helper.euclidean_distance,
                      'cie-lab': color_helper.lab_difference}

# コンフィグの読み込み
config_file_name = 'config.json'
if os.path.exists(config_file_name):
  with open(config_file_name) as f:
    config = json.load(f)
    if not config['matrix'] in available_matrices:
      raise BadConfigException('The matrix `{}` is not available. Please specify from [{}]'.format(config['matrix'], ', '.join(available_matrices.keys())))
else:
  # デフォルトを設定してコンフィグを作成
  config = {'matrix': 'absolute'}
  with open(config_file_name, 'w') as f:
    json.dump(config, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    root = Tk()
    root.title('Terraria Tile Searcher')
    root.geometry('340x430')
    RgbInputFrame(root)
    root.mainloop()
