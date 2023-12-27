import sys

def entry_form(data, kwargs):
    size = 3 # число клеточек в строке
    line_width = 6 # ширина линий 
    ind = line_width // 2 # отступ
    side = 80 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + inner_side 
    plot_height = line_width + 5 * side
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{board_side}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<rect class="blue" x="{1 * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side * 3}" />'
    yield f'<rect class="green" x="{0 * side + line_width}" y="{line_width + inner_side * 1}" width="{inner_side}" height="{inner_side * 2}" />'
    yield f'<rect class="yellow" x="{2 * side + line_width}" y="{line_width + inner_side * 2}" width="{inner_side}" height="{inner_side}" />'
    
    yield f'<image class="boy active num_1" x="{pad + board_side}" y="0" width="{inner_side}" height="{inner_side}" href="/static/problem/boy.png" />'
    yield f'<image class="boy active num_2" x="{pad + board_side}" y="{inner_side}" width="{inner_side}" height="{inner_side}" href="/static/problem/boy.png" />'
    yield f'<image class="boy active num_3" x="{pad + board_side}" y="{inner_side * 2}" width="{inner_side}" height="{inner_side}" href="/static/problem/boy.png" />'
    yield f'<image class="boy active num_4" x="{pad + board_side}" y="{inner_side * 3}" width="{inner_side}" height="{inner_side}" href="/static/problem/boy.png" />'
    yield f'<image class="reload" x = "{pad + board_side}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if x == answer:
            return True
    return False