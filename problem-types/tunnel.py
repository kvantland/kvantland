def entry_form(data, kwargs):
    width = 8 # число клеточек в строке
    height = 8
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side + ind # длина стороны доски
    board_height = line_width + height * side + ind
    rect_height = 26
    rect_width = 38
    cube_width = 22
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'<svg version="1.1" width="{board_height}" height="{board_width}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<rect class="grass" width="{board_height}" height="{board_width}"/>'
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
            if (b != 0):
                yield f'<image class="cube" x = "{b * side - cube_width / 2}" y="{c * side - cube_width / 2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11.png"/>'
            yield f'<image class="inside_line not_choiced" pos="{a}" column="{b}" row="{c}" x = "{b * side + cube_width / 2}" y="{c * side - rect_height / 2}" height="{rect_height}" width="{rect_width}" href="/static/problem_assets/tiles/rect13x19.png"/>'
            if (b != width - 1):
                yield f'<image class="cube" x = "{b * side + rect_width + cube_width / 2}" y="{c * side - cube_width / 2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11.png"/>'
            #yield f'<line class="inside_line not_choiced" pos="{a}" column="{b}" row="{c}" x1="{ind + b * side}" y1 = "{ind + c * side}" x2="{ind + (b + 1) * side}" y2="{ind + c * side}" stroke-width="{line_width}"/>'
        else:
            if (c != 0):
                yield f'<image class="cube" x = "{b * side - cube_width / 2}" y="{c * side - cube_width / 2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11.png"/>'
            yield f'<image class="inside_line not_choiced" pos="{a}" column="{b}" row="{c}" x = "{b * side - rect_height / 2}" y="{c * side + cube_width / 2}" height="{rect_width}" width="{rect_height}" href="/static/problem_assets/tiles/rect19x13.png"/>'
            if (c != height - 1):
                yield f'<image class="cube" x = "{b * side - cube_width / 2}" y="{c * side + rect_width + cube_width / 2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11.png"/>'
            #yield f'<line class="inside_line not_choiced" pos="{a}" column="{b}" row="{c}" x1="{ind + b * side}" y1 = "{ind + c * side}" x2="{ind + b * side}" y2="{ind + (c + 1) * side}" stroke-width="{line_width}"/>'
    yield '</svg>'
    yield '</div>'

def validate(data, answer):
    return data['correct'] == str(answer)