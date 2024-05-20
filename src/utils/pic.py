import random
from io import BytesIO
from pathlib import PurePath, Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

from src.models.colors import Colors

MAX_LVL = 48
IMG_SIZE = (540, 360)


def make_pic(lvl: int = 1, colors: Colors = None) -> Tuple[BytesIO, Colors]:
    im = Image.new('RGBA', IMG_SIZE, 'white')
    draw = ImageDraw.Draw(im)

    colors = colors if colors else (get_colors(MAX_LVL - lvl) if lvl != MAX_LVL else get_colors(1))

    draw.rectangle((0, 0, 540, 180), fill=colors.main)
    draw.rounded_rectangle((50, 230, 245, 310), fill=colors.option_1, radius=4)
    draw.rounded_rectangle((295, 230, 490, 310), fill=colors.option_2, radius=4)

    # Создаем байтовый поток и записываем изображение в него
    image_stream = BytesIO()
    combined = Image.alpha_composite(im, get_txt_num())
    combined.save(image_stream, format="PNG")
    image_stream.seek(0)  # Возвращаем указатель на начало потока

    return image_stream, colors


def get_colors(lvl: int) -> Colors:
    main_color = "#" + ''.join([random.choice('0123456789abcdef') for _ in range(6)])
    incorrect_color = main_color

    while lvl > 0:
        sym_num = int(random.choice([2, 4, 6]))
        old_num_10 = int(incorrect_color[sym_num], 16)

        if old_num_10 < 15 - old_num_10:
            new_sym_10 = 15
            lvl -= 15 - old_num_10
        else:
            new_sym_10 = 0
            lvl -= old_num_10

        new_sym = str(hex(new_sym_10))[-1]
        incorrect_color = incorrect_color[:sym_num] + new_sym + incorrect_color[sym_num + 1:]

    options = [main_color, incorrect_color]
    random.shuffle(options)
    colors = Colors(main=main_color, option_1=options[0], option_2=options[1])

    return colors


def game_over_pic(lvl: int, colors: Colors) -> BytesIO:
    im = Image.new('RGBA', IMG_SIZE, colors.main)
    draw = ImageDraw.Draw(im)

    if colors.main == colors.option_1:
        draw.rounded_rectangle((50, 230, 245, 310), radius=4, outline='white', width=2)
        draw.rounded_rectangle((295, 230, 490, 310), fill=colors.option_2, radius=4)
    else:
        draw.rounded_rectangle((50, 230, 245, 310), fill=colors.option_1, radius=4)
        draw.rounded_rectangle((295, 230, 490, 310), radius=4, outline='white', width=2)

    # Создаем байтовый поток и записываем изображение в него
    image_stream = BytesIO()
    combined = Image.alpha_composite(im, get_txt_num(lvl=lvl, is_game_over=True))
    combined.save(image_stream, format="PNG")
    image_stream.seek(0)  # Возвращаем указатель на начало потока

    return image_stream


def get_txt_num(lvl: int = None, is_game_over: bool = False):
    medium_path = PurePath(Path(__file__).parent, 'fonts', 'Roboto-Medium.ttf')
    black_path = PurePath(Path(__file__).parent, 'fonts', 'Roboto-Black.ttf')

    txt = Image.new('RGBA', IMG_SIZE, (255, 255, 255, 0))
    draw_txt = ImageDraw.Draw(txt)
    font_num = ImageFont.truetype(black_path, size=48)
    draw_txt.text((134, 244), '1', font=font_num, fill=(255, 255, 255, 150))
    draw_txt.text((380, 244), '2', font=font_num, fill=(255, 255, 255, 150))
    if is_game_over:
        font_go = ImageFont.truetype(medium_path, size=72)
        draw_txt.text((74, 72), 'Game Over',
                      font=font_go, fill=(255, 255, 255, 255), align='left')

        font_lvl = ImageFont.truetype(medium_path, size=24)
        draw_txt.text((108, 152), f'You correctly guessed {lvl - 1} colors',
                      font=font_lvl, fill=(255, 255, 255, 200), align='left')

    return txt
