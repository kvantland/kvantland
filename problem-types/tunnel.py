def entry_form(data, kwargs):
    width = 8 # число клеточек в строке
    height = 8
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 40 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side + ind # длина стороны доски
    board_height = line_width + height * side + ind
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'<svg version="1.1" width="{board_height}" height="{board_width + ind + inner_side}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield '<defs>'
    yield '<linearGradient id="coinShadow" x1="0" x2="1" y1="0" y2="1">'
    yield '<stop offset="0%" stop-color="gold" />'
    yield '<stop offset="50%" stop-color="#fff2af" />'
    yield '<stop offset="100%" stop-color="gold" />'
    yield '</linearGradient>'
    yield '</defs>'
    for y in range(0, height + 1):
        yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
    for x in range(0, width + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind + height * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind}" x2="{ind}" y2="{ind + 6 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind}" y1 = "{ind + 7 * side}" x2="{ind}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind}" x2="{ind + width * side}" y2="{ind + 1 * side}" stroke-width="{line_width}"/>'
    yield f'<line class="border_line" x1="{ind + width * side}" y1 = "{ind + 2 * side}" x2="{ind + width * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
    
    for a, b, c in data['board']:
        if a == 0:
            yield f'<line class="inside_line" x1="{ind + b * side}" y1 = "{ind + c * side}" x2="{ind + (b + 1) * side}" y2="{ind + c * side}" stroke-width="{line_width}"/>'
        else:
            yield f'<line class="inside_line" x1="{ind + b * side}" y1 = "{ind + c * side}" x2="{ind + b * side}" y2="{ind + (c + 1) * side}" stroke-width="{line_width}"/>'
    yield '</svg>'
    yield '</div>'

def validate(data, answer):
    return data['correct'] == answer