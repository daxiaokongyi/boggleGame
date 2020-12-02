from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client();
        app.config['TESTING'] = True    
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


    def test_homepage(self):
        """Make sure HTML and session have correct infomations"""
        with self.client:
            # import pdb
            # pdb.set_trace()
            res = self.client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="size">Size of Board: </label>', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highest_score'))
            self.assertIsNone(session.get('play_round'))
            self.assertIsNone(session.get('size'))      
            self.assertIn(b'<p>Your Score: <span class="score">', res.data)

    def test_check_valid(self):
        """Make sure boggle game is able to check a word valid or not"""
        with self.client:
            with self.client.session_transaction() as session_change:
                session_change['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            res = self.client.get('/check_valid?word=cat')
            self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check_valid?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check_valid?word=fsjdakfkldsfjdslkfjdlksf')
            self.assertEqual(response.json['result'], 'not-word')

    def test_size(self):
        with self.client:
            res = self.client.post('/size', data = {'size': '8'})
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 302)

    def test_redirection(self):
        with self.client:
            res = self.client.get('/size')

            self.assertEqual(res.status_code, 405)

    def test_session(self):
        with self.client:
            res = self.client.get('/')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session.get('size'), None)
