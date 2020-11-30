from boggle import Boggle 
from flask import Flask, render_template, session, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boggleKey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
boggle_game = Boggle()

@app.route('/')
def display_board():
    """Show board"""
    # initialized the board
    if (session['size'] != None):
        board = boggle_game.make_board(int(session['size']))
    else:
        board = boggle_game.make_board(5)
    # add board into session
    session['board'] = board
    return render_template('home.html', board = board)

@app.route('/size', methods=["POST"])
def getSize():
    """Get Size of the board"""
    size = request.json['size']
    print(size)
    session['size'] = size

    return redirect('/')

@app.route('/check_valid')
def check_valid():
    """Check if a word is valid on the board"""
    word = request.args['word']
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
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