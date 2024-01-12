import sys
name = ["Алик", "Боря", "Ваня", "Гена"]
def entry_form(data, kwargs):
    size = 3 # число клеточек в строке
    line_width = 0 # ширина линий 
    ind = line_width // 2 # отступ
    side = 120 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ
    inner_height = inner_side / 2
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = pad + board_side + inner_side * 2 
    plot_height = line_width + side + inner_height * 3
    yield '<input name="answer" type="hidden" />'
    yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield f'<rect class="top" x="{1 * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal" x="{1 * side + line_width}" y="{line_width + inner_side}" width="{inner_side}" height="{inner_height * 3}" />'
    yield f'<text class="bottom" transform ="translate({1 * side + line_width + side / 2}, {inner_height * 0 + inner_side + inner_height / 2})">1</text>'
    yield f'<rect class="top" x="{0 * side + line_width}" y="{line_width + inner_height * 1}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal" x="{0 * side + line_width}" y="{line_width + inner_side + inner_height}" width="{inner_side}" height="{inner_height * 2}" />'
    yield f'<text class="bottom" transform ="translate({0 * side + line_width + side / 2}, {inner_height * 1 + inner_side + inner_height / 2})">2</text>'
    yield f'<rect class="top" x="{2 * side + line_width}" y="{line_width + inner_height * 2}" width="{inner_side}" height="{inner_side}" />'
    yield f'<rect class="pedestal" x="{2 * side + line_width}" y="{line_width + inner_height * 2 + inner_side}" width="{inner_side}" height="{inner_height}" />'
    yield f'<text class="bottom" transform ="translate({2 * side + line_width + side / 2}, {inner_height * 2 + inner_side + inner_height / 2})">3</text>'
    #yield f'<line class="filler_line" x1="{line_width + side}" y1 = "{line_width + inner_side + inner_height + 1.5}" x2="{line_width + side}" y2="{line_width + inner_side + inner_height * 3 - 1.5}" stroke-width="{line_width}"/>'
    #yield f'<line class="filler_line" x1="{line_width + 2 * side}" y1 = "{line_width + inner_side + inner_height * 2 + 1.5}" x2="{line_width + 2 * side}" y2="{line_width + inner_side + inner_height * 3 - 1.5}" stroke-width="{line_width}"/>'
    yield f"""<path class="border_line" d=" M {0 + line_width}, {line_width + inner_side + inner_height * 3}
                        v {-(line_width + 2 * inner_height)}
                        h {line_width + 1 * inner_side} 
                        v {-(line_width + 1 * inner_height)}
                        h {line_width + 1 * inner_side} 
                        v {line_width + 2 * inner_height}
                        h {line_width + 1 * inner_side} 
                        v {line_width + 1 * inner_height}
                        z"/>"""

    for i in range(0, 4):
        yield f'<image class="boy active" num = "{i + 1}" x="{pad + board_side + inner_side * (i % 2)}" y="{inner_height + inner_side * (i // 2)}" width="{inner_side}" height="{inner_side}" href="/static/runner/boy-{i + 1}.svg">'
        yield f'<title>{name[i]}</title>'
        yield f'</image>'
    yield f'<image class="reload" x = "{pad + board_side}" y="{0}" height="{inner_height}" width="{inner_height}" href="/static/reload.png" />'
    yield '</svg>'

def validate(data, answer):
    x = data['correct']
    if x == answer:
            return True
    return False