import sys

def entry_form(data, kwargs):
    size = 10 # число клеточек в строке
    line_width = 2 # ширина линий 
    ind = line_width / 2 # отступ
    side = 60 # длина стороны квадрата с границами
    inner_side = side - line_width # длина стороны квадрата без границ 
    board_side = line_width + size * side + line_width # длина стороны доски
    plot_height = line_width + 4 * side
    yield '<input name="answer" type="hidden" />'
    yield '<div class="plot_area">'
    yield f'<svg version="1.1" width="{board_side}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    yield '<defs>'
    yield '<linearGradient id="slotShadow" x1="0" x2="0" y1="0" y2="1">'
    yield '<stop offset="0%" stop-color="gray" />'
    yield '<stop offset="25%" stop-color="white" />'
    yield '<stop offset="100%" stop-color="gray" />'
    yield '</linearGradient>'
    yield '</defs>'
    #yield f'<rect class="border" y={side / 2} width="{board_side}" height="{plot_height / 2}"/>'
    yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + 0 * side + side}" x2="{ind + size * side}" y2="{ind + 0 * side + side}" stroke-width="{line_width}"/>'
    yield f'<line class="grid_line" x1="{ind}" y1 = "{2 * side + side - ind}" x2="{ind + size * side}" y2="{ 2 * side + side - ind}" stroke-width="{line_width}"/>'
    for x in range(0, size + 1):
        yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind + side}" x2="{ind + x * side}" y2="{side * 3 - ind}" stroke-width="{line_width}"/>'
    for card in range(len(data["start"])):
        if data["start"][card] == '*':
            #yield f'<rect class="colored top" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            #yield f'<text class="arrow" transform ="translate({card * side + side / 2}, {ind + side / 2}) rotate(270)">-></text>'
            #yield f'<rect class="active top" x="{card * side + line_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f"""<path class="active top" column="{card}" d=" M {card * side + line_width},{side - ind}
                        l {side / 2},{-side / 3}
                        l {side / 2},{side / 3}
                        z"/>"""
            yield f'<rect class="passive gray" x="{card * side + line_width}" y="{1 * side + line_width}" width="{inner_side}" height="{inner_side * 2}" column="{card}"/>'
            yield f"""<path class="active bottom" column="{card}" d=" M {card * side + line_width},{3 * side + ind}
                        l {side / 2},{side / 3}
                        l {side / 2},{-side / 3}
                        z"/>"""
            #yield f'<rect class="colored bottom" x="{card * side + line_width}" y="{2 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            #yield f'<text class="arrow" transform ="translate({card * side + side / 2}, {2 * side + ind + side / 2}) rotate(270)"><-</text>'
            #yield f'<rect class="active bottom" x="{card * side + line_width}" y="{2 * side + line_width}" width="{inner_side}" height="{inner_side}" column="{card}"/>'
            yield f'<text class="number_value unknown" x="{card * side + ind + side / 2}" y="{2 * side + ind}" column="{card}">{data["start"][card]}</text>'
        else:
            yield f'<rect class="passive gray" x="{card * side + line_width}" y="{1 * side + line_width}" width="{inner_side}" height="{inner_side * 2}" column="{card}"/>'
            yield f'<text class="number_value known" x="{card * side + ind + side / 2}" y="{2 * side + ind}" column="{card}">{data["start"][card]}</text>'
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
        return {'answer': 'no_tries', 'answer_correct': False, 'user_answer': ans, 'solution': solution}
    if ans == data['correct']:
        return {'answer': 'true', 'answer_correct': True, 'user_answer': ans, 'solution': solution}
    return {'answer': 'false'}

def validate(data, answer):
    return answer == data['correct']

HINT_ONLY = True
HYBRID = True