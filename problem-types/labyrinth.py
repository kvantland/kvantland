import sys

def entry_form(data, kwargs):
    width = 7 # число клеточек в строке
    height = 8
    line_width = 2 # ширина линий 
    ind = line_width // 2 # отступ
    side = 80 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side # длина стороны доски
    board_height = line_width + height * side
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_width + inner_side 
    plot_height = board_height
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{board_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    for y in range(0, height + 1):
        yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
    for x in range(0, width + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    for x in range(0, width):
        for y in range(0, height):
            yield f'<rect class="free white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
            if [x, y] in data['cur']:
                yield f'<g class="star passive choiced" transform="translate({x * side + line_width + side / 2} {y * side + line_width + side / 2})">'
                yield f'<circle cx="0" cy="0" r="{30 / 2}" />'
                yield '</g>'
                #yield f'<image class="star passive choiced" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/pawn_b.png" />'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if str(x) == answer:
            return True
    return False