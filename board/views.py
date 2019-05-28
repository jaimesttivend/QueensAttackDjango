from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
import json
from board import queens


def index(request):
    text = queens.extract_text_from_file()
    board = queens.get_board_from_text(text)
    error = ""
    board_result = None
    if isinstance(board, str):
        error = board
        context = {
            'error': error
        }
    else:
        board_result = queens.queens_attack(n=board['size'],
                        k=board['obstacle_number'],
                        r_q=board['queen'][0],
                        c_q=board['queen'][1],
                        obstacles=board['obstacles'])
        board_result['Queen'] = board['queen']
        board_result['Obstacles'] = board['obstacles']
        board_result = mark_safe(json.dumps(board_result))
        context = {
            'rangey': range(board['size'], 0, -1),
            'rangex': range(1, board['size'] + 1),
            'result': board_result
        }

    template = loader.get_template('board/board.html')


    #return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse(template.render(context, request))
    #return HttpResponse(template.render(context, request))
