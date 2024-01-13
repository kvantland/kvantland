import sys
name = ["Алик", "Боря", "Ваня", "Гена"]
def entry_form(data, kwargs):
    size = 3 # число клеточек в строке
    line_width = 0 # ширина линий 
    ind = line_width // 2 # отступ
    bord = 20 # отступ пьедестала
    side = 120 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ
    inner_height = inner_side / 2
    board_side = line_width + size * side # длина стороны доски
    pad = 80 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + inner_side * 2 + bord
    plot_height = line_width + side + inner_height * 3 + bord + bord / 2
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<rect class="top" x="{1 * side + line_width + bord}" y="{line_width}" num="*" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="top" x="{0 * side + line_width + bord}" y="{line_width + inner_height * 1}" num="*" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="top" x="{2 * side + line_width + bord}" y="{line_width + inner_height * 2}" num="*" width="{inner_side}" height="{inner_side}" />'
    yield f"""<path class="border_line" d=" M {0 + line_width + bord}, {line_width + inner_side + inner_height * 3 + bord / 2}
                        v {-(line_width + 2 * inner_height)}
                        h {line_width + 1 * inner_side} 
                        v {-(line_width + 1 * inner_height)}
                        h {line_width + 1 * inner_side} 
                        v {line_width + 2 * inner_height}
                        h {line_width + 1 * inner_side} 
                        v {line_width + 1 * inner_height}
                        z"/>"""
    yield f'<rect class="border_line" x="{line_width}" y="{line_width + inner_side + inner_height * 3 + bord / 2}" width="{line_width + bord + 3 * inner_side + bord}" height="{bord}"/>'
    yield f'<rect class="border_line" x="{line_width + bord / 2}" y="{line_width + inner_side + inner_height}" width="{line_width + bord / 2 + inner_side}" height="{bord / 2}"/>'
    yield f'<rect class="border_line" x="{line_width + inner_side + bord / 2}" y="{line_width + inner_side}" width="{line_width + bord + inner_side}" height="{bord / 2}"/>'
    yield f'<rect class="border_line" x="{line_width + inner_side * 2 + bord}" y="{line_width + inner_side + inner_height * 2}" width="{line_width + bord / 2 + inner_side}" height="{bord / 2}"/>'

    yield f'<text class="bottom first" transform ="translate({1 * side + line_width + side / 2 + bord}, {inner_height / 2 + inner_side})">1</text>'
    yield f'<text class="bottom second" transform ="translate({0 * side + line_width + side / 2 + bord}, {inner_height + inner_side + inner_height / 2})">2</text>'
    yield f'<text class="bottom third" transform ="translate({2 * side + line_width + side / 2 + bord}, {inner_height * 2 + inner_side + inner_height / 2})">3</text>'


    for i in range(0, 4):
        yield f'<image class="boy active" num = "{i + 1}" x="{pad + board_side + (inner_side + bord) * (i % 2)}" y="{inner_height + (inner_side + bord) * (i // 2) + bord}" width="{inner_side}" height="{inner_side}" href="/static/runner/boy-{i + 1}.svg">'
        yield f'<title>{name[i]}</title>'
        yield f'</image>'
    yield f'<image class="reload" x = "{pad + board_side}" y="{0}" height="{inner_height}" width="{inner_height}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if x == answer:
            return True
    return False