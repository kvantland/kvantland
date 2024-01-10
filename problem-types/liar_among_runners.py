import sys
name = ["Алик", "Боря", "Ваня", "Гена"]
def entry_form(data, kwargs):
    size = 3 # число клеточек в строке
    line_width = 0 # ширина линий 
    ind = line_width // 2 # отступ
    side = 120 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + inner_side 
    plot_height = line_width + 5 * side
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{board_side}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<rect class="top" x="{1 * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal gold" x="{1 * side + line_width}" y="{line_width + inner_side * 1}" width="{inner_side}" height="{inner_side * 3}" />'
    yield f'<text class="bottom" transform ="translate({1 * side + line_width + side / 2}, {inner_side * 3 + side / 2})">1</text>'
    yield f'<rect class="top" x="{0 * side + line_width}" y="{line_width + inner_side * 1}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal silver" x="{0 * side + line_width}" y="{line_width + inner_side * 2}" width="{inner_side}" height="{inner_side * 2}" />'
    yield f'<text class="bottom" transform ="translate({0 * side + line_width + side / 2}, {inner_side * 3 + side / 2})">2</text>'
    yield f'<rect class="top" x="{2 * side + line_width}" y="{line_width + inner_side * 2}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal wood" x="{2 * side + line_width}" y="{line_width + inner_side * 3}" width="{inner_side}" height="{inner_side}" />'
    yield f'<text class="bottom" transform ="translate({2 * side + line_width + side / 2}, {inner_side * 3 + side / 2})">3</text>'
    

    for i in range(0, 4):
        yield f'<image class="boy active num_{i + 1}" x="{pad + board_side}" y="{inner_side * i}" width="{inner_side}" height="{inner_side}" href="/static/runner/boy-{i + 1}.svg">'
        yield f'<title>{name[i]}</title>'
        yield f'</image>'
    yield f'<image class="reload" x = "{pad + board_side}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if x == answer:
            return True
    return False