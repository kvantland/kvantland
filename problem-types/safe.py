import sys

def entry_form(data, kwargs):
    size = 10 # число клеточек в строке
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + 2 * inner_side 
    plot_height = line_width + 1 * side
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    for card in range(len(data["start"])):
        yield f'<rect class="free gray" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
        yield f'<g class="finish passive choiced" transform="translate({card * side + line_width} {0 * side + line_width})">'
        yield f'<text class="number_value" x="{side / 2}" y="{side / 2}"> {data["start"][card]} </text>'
        yield '</g>'
    yield f'<image class="reload" x = "{pad + board_side}" y="{line_width}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    return answer == data['correct']