import math


# convert rgb to lab
def rgb_to_lab(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    r = math.pow((r + 0.055) / 1.055, 2.4) if r > 0.04045 else r / 12.92
    g = math.pow((g + 0.055) / 1.055, 2.4) if g > 0.04045 else g / 12.92
    b = math.pow((b + 0.055) / 1.055, 2.4) if b > 0.04045 else b / 12.92

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    x = math.pow(x, 1 / 3) if x > 0.008856 else 7.787 * x + 16 / 116
    y = math.pow(y, 1 / 3) if y > 0.008856 else 7.787 * y + 16 / 116
    z = math.pow(z, 1 / 3) if z > 0.008856 else 7.787 * z + 16 / 116

    return ((116 * y) - 16, 500 * (x - y), 200 * (y - z))


# calculate CIE76 deltaE
def delta_e(lab1, lab2):
  return math.sqrt((lab2[0] - lab1[0]) ** 2 + (lab2[1] - lab1[1]) ** 2 + (lab2[2] - lab1[2]) ** 2)

lab_cache = {}
def lab_difference(rgb1, rgb2):
  rgb1_tuple = (rgb1[0], rgb1[1], rgb1[2])
  rgb2_tuple = (rgb2[0], rgb2[1], rgb2[2])

  if rgb1_tuple in lab_cache:
    lab1 = lab_cache[rgb1_tuple]
  else:
    lab1 = rgb_to_lab(rgb1_tuple)
    lab_cache[rgb1_tuple] = lab1

  if rgb2_tuple in lab_cache:
    lab2 = lab_cache[rgb2_tuple]
  else:
    lab2 = rgb_to_lab(rgb2_tuple)
    lab_cache[rgb2_tuple] = lab2
  return delta_e(lab1, lab2)


# calculate euclidean distance
def euclidean_distance(rgb1, rgb2):
  return math.sqrt((rgb2[0] - rgb1[0]) ** 2 + (rgb2[1] - rgb1[1]) ** 2 + (rgb2[2] - rgb1[2]) ** 2)