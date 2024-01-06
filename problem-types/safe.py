import sys

def entry_form(data, kwargs):
    size = 10 # число клеточек в строке
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side # длина стороны доски
    pad = 6 # расстояние между доской и зоной перетаскивания
    plot_width = board_side
    plot_height = line_width + 3 * side
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'<svg version="1.1" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    for card in range(len(data["start"])):
        if data["start"][card] == '*':
            yield f'<rect class="colored top" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<text class="arrow" transform ="translate({card * side + side / 2}, {ind + side / 2}) rotate(270)">-></text>'
            yield f'<rect class="active top" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<rect class="passive gray" x="{card * side + line_width}" y="{1 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<rect class="colored bottom" x="{card * side + line_width}" y="{2 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<text class="arrow" transform ="translate({card * side + side / 2}, {2 * side + ind + side / 2}) rotate(270)"><-</text>'
            yield f'<rect class="active bottom" x="{card * side + line_width}" y="{2 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<text class="number_value unknown" x="{card * side + ind + side / 2}" y="{1 * side + ind + side / 2}" column="{card}">{data["start"][card]}</text>'
        else:
            yield f'<rect class="passive top" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<rect class="passive gray" x="{card * side + line_width}" y="{1 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<rect class="passive bottom" x="{card * side + line_width}" y="{2 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<text class="number_value known" x="{card * side + ind + side / 2}" y="{1 * side + ind + side / 2}" column="{card}">{data["start"][card]}</text>'
    #yield f'<text style="font-size: {inner_side * 0.4}px" x="{ + board_side + 2 * inner_side}" y="{inner_side * 1.2}">Попыток осталось: {data["left"]}</text>'
    #yield f'<image class="reload" x = "{pad + board_side}" y="{line_width}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
    yield '</svg>'
    yield '<div class="interface_zone">'
    yield '<button type="button" class="check"> Проверить </button>'
    yield '<button type="button" class="reload"> Сбросить </button>'
    yield '<div class="remaining_checks">'
    yield f"<p> Осталось проверок: {max(0, data['left'] - kwargs['step'])}<p>"
    yield '</div>'
    yield '</div>'
    yield '</div>'

def steps(step_num, params, data):
    if step_num > 2:
        return {'answer': 'no_tries'}
    weight = data['weight']
    left, right = 0, 0
    conf = params['conf']
    if left > right:
        return {'answer': 'left'}
    elif right > left:
        return {'answer': 'right'}
    return {'answer': 'equal'}

def validate(data, answer):
    return answer in data['correct']

WITHOUT_BUTTONS = True