def entry_form(data, kwargs):
    width = 8 # число клеточек в строке
    height = 8
    rect_height = 26
    rect_width = 38
    cube_width = 22
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    ind2 = rect_height / 2
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_width = line_width + width * side + ind # длина стороны доски
    board_height = line_width + height * side + ind
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'''<svg version="1.1" 
                preserveAspectRatio="xMidYMid meet" 
                viewBox="0 0 {board_height + rect_height + side * 2} {board_width + rect_height}" 
                width="{board_height + rect_height + side * 2}" height="{board_width + rect_height}" 
                overflow="visible" xmlns="http://www.w3.org/2000/svg" 
                xmlns:xlink="http://www.w3.org/1999/xlink">'''
    yield '<defs>'
    yield '<linearGradient id="grassGradient" x1="0" x2="1" y1="1" y2="0">'
    yield '<stop offset="0%" stop-color="#88a24b"/>'
    yield '<stop offset="50%" stop-color="#d7de90"/>'
    yield '<stop offset="100%" stop-color="#88a24b"/>'
    yield '</linearGradient>'
    yield '</defs>'
    yield f'<rect class="grass" x="{ind2 + side}" y="{ind2}" width="{board_height - ind}" height="{board_width - ind}"/>'
    for y in range(0, height + 1):
        yield f'<line class="grid_line" x1="{ind + ind2 + side}" y1 = "{ind + y * side + ind2}" x2="{ind + width * side + ind2 + side}" y2="{ind + y * side + ind2}" stroke-width="{line_width}"/>'
    for x in range(0, width + 1):
        yield f'<line class="grid_line" x1="{ind + x * side + ind2 + side}" y1 = "{ind + ind2}" x2="{ind + x * side + ind2 + side}" y2="{ind + height * side + ind2}" stroke-width="{line_width}"/>'

    yield f'<image class="border_cube" x = "{-cube_width / 2 + ind2 + side}" y="{-cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_cornerleft.png"/>'
    yield f'<image class="border_cube" x = "{width * side - cube_width / 2 + ind2 + side}" y="{-cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_corner.png"/>'
    for x in range(1, width):
        yield f'<image class="border_cube" x = "{x * side - cube_width / 2 + ind2 + side}" y="{-cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_shade.png"/>'
    for x in range(0, width):
        yield f'<image class="border_line" x = "{x * side + cube_width / 2 + ind2 + side}" y="{-rect_height / 2 + ind2}" height="{rect_height}" width="{rect_width}" href="/static/problem_assets/tiles/grass13x19.png"/>'

    yield f'<image class="border_cube" x = "{-cube_width / 2 + ind2 + side}" y="{side * width - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_cornerleft.png"/>'
    yield f'<image class="border_cube" x = "{width * side - cube_width / 2 + ind2 + side}" y="{side * width - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_corner.png"/>'
    for x in range(1, width):
        yield f'<image class="border_cube" x = "{x * side - cube_width / 2 + ind2 + side}" y="{side * width - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11_shade.png"/>'
    for x in range(0, width):
        yield f'<image class="border_line" x = "{x * side + cube_width / 2 + ind2 + side}" y="{side * width - rect_height / 2 + ind2}" height="{rect_height}" width="{rect_width}" href="/static/problem_assets/tiles/grass13x19.png"/>'

    for y in range(1, width):
        yield f'<image class="border_cube" x = "{- cube_width / 2 + ind2 + side}" y="{y * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11.png"/>'
    for y in range(0, width):
        if (y != 6):
            yield f'<image class="border_line" x = "{-rect_height / 2 + ind2 + side}" y="{y * side + cube_width / 2 + ind2}" height="{rect_width}" width="{rect_height}" href="/static/problem_assets/tiles/grass19x13.png"/>'

    for y in range(1, width):
        yield f'<image class="border_cube" x = "{width * side - cube_width / 2 + ind2 + side}" y="{y * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/grass11x11.png"/>'
    for y in range(0, width):
        if (y != 1):
            yield f'<image class="border_line" x = "{width * side - rect_height / 2 + ind2 + side}" y="{y * side + cube_width / 2 + ind2}" height="{rect_width}" width="{rect_height}" href="/static/problem_assets/tiles/grass19x13.png"/>'
    yield f'<text class="gate" x="{ind2 + cube_width}" y="{ind2 + 7 * side - ind2}" width="{side}" height="{side}">A</text>'
    yield f'<text class="gate" x="{ind2 + 9 * side + ind2}" y="{ind2 + 2 * side - ind2}" width="{side}" height="{side}">B</text>'
    for y in range(0, width - 1):
        for x in range (0, width - 1):
            tmp = data['board'][y][x]
            if (tmp // 10 == 1):
                yield f'<image class="cube" x = "{(x + 1) * side - cube_width / 2 + ind2 + side}" y="{(y + 1) * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11.png"/>'
            elif (tmp // 10 == 2):
                yield f'<image class="cube" x = "{(x + 1) * side - cube_width / 2 + ind2 + side}" y="{(y + 1) * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11_shade.png"/>'
            elif (tmp // 10 == 3):
                yield f'<image class="cube" x = "{(x + 1) * side - cube_width / 2 + ind2 + side}" y="{(y + 1) * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11_cornerleft.png"/>'
            elif (tmp // 10 == 4):
                yield f'<image class="cube" x = "{(x + 1) * side - cube_width / 2 + ind2 + side}" y="{(y + 1) * side - cube_width / 2 + ind2}" height="{cube_width}" width="{cube_width}" href="/static/problem_assets/tiles/block11x11_corner.png"/>'
            if (tmp % 10 == 1):
                yield f'<image class="inside_line not_choiced" pos="{0}" column="{x + 1}" row="{y + 1}" x = "{(x + 1) * side + cube_width / 2 + ind2 + side}" y="{(y + 1) * side - rect_height / 2 + ind2}" height="{rect_height}" width="{rect_width}" href="/static/problem_assets/tiles/rect13x19.png"/>'
            elif (tmp % 10 == 2):
                yield f'<image class="inside_line not_choiced" pos="{1}" column="{x + 1}" row="{y + 1}" x = "{(x + 1) * side - rect_height / 2 + ind2 + side}" y="{(y + 1) * side + cube_width / 2 + ind2}" height="{rect_width}" width="{rect_height}" href="/static/problem_assets/tiles/rect19x13.png"/>'
            elif (tmp % 10 == 3):
                yield f'<image class="inside_line not_choiced" pos="{0}" column="{x + 1}" row="{y + 1}" x = "{(x + 1) * side + cube_width / 2 + ind2 + side}" y="{(y + 1) * side - rect_height / 2 + ind2}" height="{rect_height}" width="{rect_width}" href="/static/problem_assets/tiles/rect13x19.png"/>'
                yield f'<image class="inside_line not_choiced" pos="{1}" column="{x + 1}" row="{y + 1}" x = "{(x + 1) * side - rect_height / 2 + ind2 + side}" y="{(y + 1) * side + cube_width / 2 + ind2}" height="{rect_width}" width="{rect_height}" href="/static/problem_assets/tiles/rect19x13.png"/>'
    yield '</svg>'
    yield '</div>'

def validate(data, answer):
    return data['correct'] == str(answer)