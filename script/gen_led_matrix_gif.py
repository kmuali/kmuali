# File: gen_led_matrix_gif.py
# Author: Karim M. Ali
# Date: April 26, 2024
# Description: This script generates animated LED matrix of a given text.
# License: GNU General Public License v3.0 (GPL-3.0)

from PIL import Image, ImageDraw
from font_8x8 import bitmap

## Edit This Constants #################################################

TEXT = "Karim M. Ali"
CHARS_PER_ROW_N = 8

FRAMES_PER_SECOND = 24

FILENAME = "banner.gif"

DO_OPTIMIZE_GIF = True

_BLUE_ON = (0, 192, 255)
_BLUE_OFF = (0, 48, 64)
_BLUE_BG = (0, 0, 0)

_RED_ON = (255, 0, 0)
_RED_OFF = (64, 0, 0)
_RED_BG = (32, 0, 0)

LED_ON_RGB = _BLUE_ON
LED_OFF_RGB = _BLUE_OFF
BG_RGB = _BLUE_BG

########################################################################

DIAMETER_PX = 10
MARGIN_PX = DIAMETER_PX // 5
DOT_PX = (MARGIN_PX * 2 + DIAMETER_PX)
CHAR_PX = 8 * DOT_PX
FRAME_WIDTH_PX = CHAR_PX * CHARS_PER_ROW_N

def main():
    frames = gen_frames_from_right()

    frames[0].save(FILENAME, save_all=True, 
                   append_images=frames[1:], optimize=DO_OPTIMIZE_GIF, 
                   duration=1000/FRAMES_PER_SECOND, loop=0)

def gen_frames_from_right():
    frames_n = (CHARS_PER_ROW_N + len(TEXT)) * 8 - 1
    return [gen_image(FRAME_WIDTH_PX - index * DOT_PX, 0, TEXT) 
            for index in range(frames_n)]

def gen_image(x_offset, y_offset, text):
    frame = Image.new("RGB", (FRAME_WIDTH_PX, CHAR_PX), BG_RGB)
    draw = ImageDraw.Draw(frame)

    draw_background(draw)

    for index, char in enumerate(text):
        draw_char(draw, x_offset + index * CHAR_PX, y_offset, char)

    return frame

def draw_char(draw, x_offset, y_offset, char):
    for row in range(8):
        for col in range(8):
            beg_x = MARGIN_PX + col * (MARGIN_PX * 2 + DIAMETER_PX) + x_offset
            beg_y = MARGIN_PX + row * (MARGIN_PX * 2 + DIAMETER_PX) + y_offset
            end_x = DIAMETER_PX + beg_x
            end_y = DIAMETER_PX + beg_y
            is_on = bitmap[char][row] & (1 << col)
            if is_on:
                draw.ellipse([(beg_x, beg_y), (end_x, end_y)], LED_ON_RGB)

def draw_background(draw):
    for row in range(8):
        for col in range(8 * CHARS_PER_ROW_N):
            beg_x = MARGIN_PX + col * (MARGIN_PX * 2 + DIAMETER_PX) 
            beg_y = MARGIN_PX + row * (MARGIN_PX * 2 + DIAMETER_PX)
            end_x = DIAMETER_PX + beg_x
            end_y = DIAMETER_PX + beg_y
            draw.ellipse([(beg_x, beg_y), (end_x, end_y)], LED_OFF_RGB)

if __name__ == '__main__':
    main()
