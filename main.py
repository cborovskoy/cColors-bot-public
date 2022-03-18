from PIL import Image, ImageDraw, ImageFont
import random

from settings import get_start_path

ALL_LVL = 48
IMG_SIZE = (540, 360)


def make_pic(user_id=0, lvl=1):
    im = Image.new('RGBA', IMG_SIZE, 'white')
    draw = ImageDraw.Draw(im)

    if lvl != ALL_LVL:
        colors = get_colors(ALL_LVL - lvl)
    else:
        colors = get_colors(1)

    draw.rectangle((0, 0, 540, 180), fill=colors['main'])
    draw.rounded_rectangle((50, 230, 245, 310), fill=colors['var_1'], radius=4)
    draw.rounded_rectangle((295, 230, 490, 310), fill=colors['var_2'], radius=4)

    combined = Image.alpha_composite(im, get_txt_num())
    combined.save(f'{get_start_path()}pic_{user_id}.png')

    game_over_pic(user_id=user_id, colors=colors, lvl=lvl)
    return colors


def game_over_pic(lvl, colors, user_id=0):
    im = Image.new('RGBA', IMG_SIZE, colors['main'])
    draw = ImageDraw.Draw(im)

    if colors['main'] == colors['var_1']:
        draw.rounded_rectangle((50, 230, 245, 310), radius=4, outline='white', width=2)
        draw.rounded_rectangle((295, 230, 490, 310), fill=colors['var_2'], radius=4)
    else:
        draw.rounded_rectangle((50, 230, 245, 310), fill=colors['var_1'], radius=4)
        draw.rounded_rectangle((295, 230, 490, 310), radius=4, outline='white', width=2)

    combined = Image.alpha_composite(im, get_txt_num(lvl=lvl, is_game_over=True))

    combined.save(f'{get_start_path()}pic_game_over_{user_id}.png')


def get_txt_num(lvl=None, is_game_over=False):
    txt = Image.new('RGBA', IMG_SIZE, (255, 255, 255, 0))
    draw_txt = ImageDraw.Draw(txt)
    font_num = ImageFont.truetype("arialbd.ttf", size=48)
    draw_txt.text((134, 244), '1', font=font_num, fill=(255, 255, 255, 150))
    draw_txt.text((380, 244), '2', font=font_num, fill=(255, 255, 255, 150))
    if is_game_over:
        font_go = ImageFont.truetype("arialbd.ttf", size=72)
        draw_txt.text((74, 72), 'Game Over',
                      font=font_go, fill=(255, 255, 255, 255), align='left')

        font_lvl = ImageFont.truetype("arial.ttf", size=24)
        draw_txt.text((108, 152), f'You correctly guessed {lvl} colors',
                      font=font_lvl, fill=(255, 255, 255, 200), align='left')

    return txt

def get_colors(lvl):
    result_colors = {'main': "#" + ''.join([random.choice('0123456789abcdef') for j in range(6)])}
    incorrect_color = result_colors['main']

    temp_lvl = lvl

    while temp_lvl > 0:
        sym_num = int(random.choice([2, 4, 6]))
        old_num_10 = int(incorrect_color[sym_num], 16)

        if old_num_10 < 15 - old_num_10:
            new_sym_10 = 15
            temp_lvl -= 15 - old_num_10
        else:
            new_sym_10 = 0
            temp_lvl -= old_num_10

        new_sym = str(hex(new_sym_10))[-1]
        incorrect_color = incorrect_color[:sym_num] + new_sym + incorrect_color[sym_num + 1:]

    if random.choice(['var_1', 'var_2']) == 'var_1':
        result_colors['var_1'] = result_colors['main']
        result_colors['var_2'] = incorrect_color
    else:
        result_colors['var_2'] = result_colors['main']
        result_colors['var_1'] = incorrect_color

    return result_colors


if __name__ == '__main__':
    make_pic(lvl=16)
