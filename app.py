from flask import Flask, render_template, request, jsonify
from alphabeta import calculate_ai_move
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-ai-move', methods=['POST'])
def get_ai_move():
    data = request.json
    board = data['board']
    ai_player = data['aiPlayer']
    app.logger.info('board: %s', board)
    app.logger.info('ai_player: %s', ai_player)

    move = calculate_ai_move(board, ai_player)
    if move is None:
        return jsonify({'error': 'No valid move available.'})
    else:
        x, y = move
        return jsonify({'x': x, 'y': y})


if __name__ == '__main__':
    app.run(debug=True)
