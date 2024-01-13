import sys

def entry_form(data, kwargs):
    size = 8 # число клеточек в строке
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + inner_side 
    plot_height = board_side
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    for y in range(0, size + 1):
        yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + size * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
    for x in range(0, size + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + size * side}" stroke-width="{line_width}"/>'
    for x in range(0, size):
        for y in range(0, size):
            if (x + y) % 2 == 1:
                if x == 0 or y == size - 1:
                    yield f'<rect class="free brown" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}" />'
                elif [x, y] in data['cur']:
                    yield f'<rect class="occupied brown" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}"/>'
                    yield f'<image class="pawn passive choiced" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/pawn_b.png" />'
                else:
                    yield f'<rect class="brown" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}"/>'
            else:
                if x == 0 or y == size - 1:
                    yield f'<rect class="free white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}"/>'
                elif [x, y] in data['cur']:
                    yield f'<rect class="occupied white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}"/>'
                    yield f'<image class="pawn passive choiced" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/pawn_b.png" />'
                else:
                    yield f'<rect class="white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" column="{x}" row="{y}"/>'
    yield f'<image class="rook free" x="{0 * side + line_width}" y ="{(size - 1) * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/rook_b.png" column="{0}" row="{size - 1}"/>'
    yield f'<g class="finish passive choiced" transform="translate({(size - 1) * side + line_width} {0 * side})">'
    #yield f'<circle cx="{side / 2}" cy="{side / 2}" r="{20}" fill="yellow"/>'
    yield f'<polygon class="star" points="100,10 40,198 190,78 10,78 160,198" transform="scale(0.29)"/>'
    yield '</g>'
    yield f'<image class="reload" x = "{pad + board_side}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    return answer == data['correct']