def entry_form(data, kwargs):
    width = 7 # число клеточек в строке
    height = 8
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 40 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side + ind # длина стороны доски
    board_height = line_width + height * side + ind

    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{board_height}" height="{board_width}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<g transform="translate({board_width + side} 0 )rotate(90)">'
    for y in range(0, height + 1):
        yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
    for x in range(0, width + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind + height * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind + 4 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind + 5 * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    
    for a, b, c, d in data['board']:
        yield f'<line class="border_line" x1="{ind + a * side}" y1 = "{ind + b * side}" x2="{ind + c * side}" y2="{ind + d * side}" stroke-width="{line_width}"/>'

    for x in range(0, width):
        for y in range(0, height):
            if [x, y] in data['cur']:
                yield f'<g class="star" transform="translate({x * side + ind} {y * side + ind})">'
                yield f'<circle cx="{side / 2}" cy="{side / 2}" r="{15}" fill="yellow" stroke="orange" stroke-width="{5}"/>'
                yield '</g>'
            yield f'<rect class="free square" row="{y}" column="{x}" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
    yield f'</g>'
    yield '</svg>'

def validate(data, answer):
    return data['correct'] == answer