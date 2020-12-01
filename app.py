from boggle import Boggle 
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boggleKey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    
boggle_game = Boggle()
debug = DebugToolbarExtension(app)

@app.route('/')
def display_board():
    """Show board"""
    size = session.get('size')
    print(f'size is {size}')
    # check the value of the size
    if size:
        boggle_game = Boggle(size)
    else:
        boggle_game = Boggle(5)
    print(f'boggle game current size is {boggle_game.size}')

    board = boggle_game.make_board()

    # add board into session
    session['board'] = board
    return render_template('home.html', board = board)

@app.route('/size', methods=["POST"])
def getSize():
    """Get Size of the board"""
    size = request.form['size']
    session['size'] = int(size)
    return redirect('/')

@app.route('/check_valid')
def check_valid():
    """Check if a word is valid on the board"""
    word = request.args['word']
    board = session['board']
    size = session.get('size')

    if not size:
        result = Boggle().check_valid_word(board, word)
    else:
        result = Boggle(size).check_valid_word(board, word)
    return jsonify({'result': result})
    # return jsonify(result = result)

@app.route('/post-score', methods=["POST"])
def game_result():
    """ receive score, update play round & highest score """
    score = request.json['score']

    highest_score = max(session.get('highest_score', 0), score)
    session['highest_score'] = highest_score
    
    play_round = session.get('play_round', 0) + 1
    session['play_round'] = play_round

    return jsonify(result = highest_score, round = play_round)