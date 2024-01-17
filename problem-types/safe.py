import sys
import math

def entry_form(data, kwargs):
    size = 10 # число клеточек в строке
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 50 # длина стороны квадрата с границами
    pad = 50
    damp = pad / 2
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side + line_width + 2 * damp # длина стороны доски
    plot_height = line_width + 4 * side
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'<svg version="1.1" width="{board_side}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield '<defs>'
    yield '<linearGradient id="slotShadow" x1="0" x2="0" y1="0" y2="1">'
    yield '<stop offset="0%" stop-color="gray" />'
    yield '<stop offset="25%" stop-color="rgba(230, 230, 230, 1)" />'
    yield '<stop offset="100%" stop-color="gray" />'
    yield '</linearGradient>'
    yield '</defs>'
    yield f'<rect class="border" x="{damp / 2}" y="{side / 2}" width="{damp + line_width + size * side}" height="{line_width + 3 * side}"/>'
    yield f'<rect class="base" x="{damp}" y="{side}" width="{size * side + 2 * ind}" height="{2 * side}" />'
    cur_column = 0
    for card in range(len(data["start"])):
        if data["start"][card] == '*':
            yield f"""<path class="active top" column="{card}" num="{cur_column}" d=" M {card * side + line_width + damp},{side / 2 - side / 6}
                        l {side / 2},{-side / 3}
                        l {side / 2},{side / 3}
                        z"/>"""
            yield f"""<path class="active bottom" column="{card}" num="{cur_column}" d=" M {card * side + line_width + damp},{3 * side + side / 2 + side / 6}
                        l {side / 2},{side / 3}
                        l {side / 2},{-side / 3}
                        z"/>"""
            yield f'<svg x="{card * side + line_width + damp}" y="{side + line_width}" width="{inner_side}" height="{inner_side * 2}">'
            yield f'<rect class="passive slot" x="0" y="0" width="{inner_side}" height="{inner_side * 2}" column="{card}"/>'
            yield f'<text class="number_value up_number" column="{card}" x="{inner_side / 2}" y="{-inner_side}" angle="{2 * math.pi / 10}" num="{cur_column}" sgn="1"> 0 </text>'
            yield f'<text class="number_value unknown" unset="1" x="{inner_side / 2}" y="{inner_side}" column="{card}" angle="0" num="{cur_column}" sgn="0">{data["start"][card]}</text>'
            yield f'<text class="number_value bottom_number" column="{card}" x="{inner_side / 2}" y="{3 * inner_side}" angle="{2 * math.pi / 10}" num="{cur_column}" sgn="-1"> 9 </text>'
            yield '</svg>'
            cur_column += 1
        else:
            yield f'<svg x="{card * side + line_width + damp}" y="{side + line_width}" width="{inner_side}" height="{inner_side * 2}">'
            yield f'<rect class="passive slot" x="0" y="0" width="{inner_side}" height="{inner_side * 2}" column="{card}"/>'
            yield f'<text class="number_value known" x="{inner_side / 2}" y="{inner_side}" column="{card}">{data["start"][card]}</text>'
            yield '</svg>'
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
    ans = params['answer']
    solution = params['solution']
    if step_num > data['left']:
        return {'answer': 'no_tries'}
    if ans == data['correct']:
        return {'answer': 'true', 'answer_correct': True, 'user_answer': ans, 'solution': solution}
    if step_num == data['left']:
        return {'answer': 'false', 'answer_correct': False, 'user_answer': ans, 'solution': solution}
    return {'answer': 'false'}

def validate(data, answer):
    return answer == data['correct']

HINT_ONLY = True
HYBRID = True