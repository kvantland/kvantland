import sys

def entry_form(data, kwargs):
    width = 7 # число клеточек в строке
    height = 8
    line_width = 4 # ширина линий 
    ind = line_width // 2 # отступ
    side = 80 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side # длина стороны доски
    board_height = line_width + height * side
    pad = 6 # расстояние между доской и зоной перетаскивания

    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{board_width}" height="{board_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    for y in range(0, height + 1):
        yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
    for x in range(0, width + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind + height * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind + 4 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind + 5 * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    
    yield f'<line class="border_line" x1="{ind + 2 * side}" y1 = "{ind}" x2="{ind + 2 * side}" y2="{ind + 1 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind}" x2="{ind + 5 * side}" y2="{ind + 2 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 3 * side}" y1 = "{ind + 1 * side}" x2="{ind + 3 * side}" y2="{ind + 3 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 6 * side}" y1 = "{ind + 1 * side}" x2="{ind + 6 * side}" y2="{ind + 2 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 4 * side}" y1 = "{ind + 2 * side}" x2="{ind + 4 * side}" y2="{ind + 3 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 1 * side}" y1 = "{ind + 3 * side}" x2="{ind + 1 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 2 * side}" y1 = "{ind + 4 * side}" x2="{ind + 2 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 4 * side}" y1 = "{ind + 4 * side}" x2="{ind + 4 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind + 4 * side}" x2="{ind + 5 * side}" y2="{ind + 5 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 3 * side}" y1 = "{ind + 5 * side}" x2="{ind + 3 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind + 6 * side}" x2="{ind + 5 * side}" y2="{ind + 7 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 4 * side}" y1 = "{ind + 7 * side}" x2="{ind + 4 * side}" y2="{ind + 8 * side}" stroke-width="{line_width}"/>'
    
    yield f'<line class="border_line" x1="{ind + 3 * side}" y1 = "{ind + 1 * side}" x2="{ind + 5 * side}" y2="{ind + 1 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 1 * side}" y1 = "{ind + 2 * side}" x2="{ind + 3 * side}" y2="{ind + 2 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind + 2 * side}" x2="{ind + 6 * side}" y2="{ind + 2 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 1 * side}" y1 = "{ind + 3 * side}" x2="{ind + 3 * side}" y2="{ind + 3 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 4 * side}" y1 = "{ind + 3 * side}" x2="{ind + 7 * side}" y2="{ind + 3 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 2 * side}" y1 = "{ind + 4 * side}" x2="{ind + 3 * side}" y2="{ind + 4 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 6 * side}" y1 = "{ind + 4 * side}" x2="{ind + 7 * side}" y2="{ind + 4 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 3 * side}" y1 = "{ind + 5 * side}" x2="{ind + 4 * side}" y2="{ind + 5 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind + 5 * side}" x2="{ind + 7 * side}" y2="{ind + 5 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 0 * side}" y1 = "{ind + 6 * side}" x2="{ind + 2 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 4 * side}" y1 = "{ind + 6 * side}" x2="{ind + 7 * side}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 1 * side}" y1 = "{ind + 7 * side}" x2="{ind + 4 * side}" y2="{ind + 7 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + 5 * side}" y1 = "{ind + 7 * side}" x2="{ind + 6 * side}" y2="{ind + 7 * side}" stroke-width="{line_width}"/>'

    for x in range(0, width):
        for y in range(0, height):
            yield f'<rect class="free square" row="{y}" column="{x}" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
            if [x, y] in data['cur']:
                yield f'<g class="star passive free" transform="translate({x * side + line_width} {y * side + line_width})">'
                yield f'<circle cx="{side / 2}" cy="{side / 2}" r="{30}" fill="orange"/>'
                yield f'<circle cx="{side / 2}" cy="{side / 2}" r="{20}" fill="yellow"/>'
                yield '</g>'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if str(x) == answer:
            return True
    return False