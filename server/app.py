from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyD32B8mepuvdpnYNY2XekKlVfGgAtXEvJo",
  "authDomain": "jehoot-16c84.firebaseapp.com",
  "databaseURL": "https://jehoot-16c84-default-rtdb.firebaseio.com/",
  "projectId": "jehoot-16c84",
  "storageBucket": "jehoot-16c84.appspot.com",
  "messagingSenderId": "105518725013",
  "appId": "1:105518725013:web:44a233c436d81d07a8a89c",
  "measurementId": "G-3KWMPMTFLB"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello123'
socket = SocketIO(app)

@app.route('/new_user')
def new_user():
    try: 
        auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        return ''
    except:
        return '', 409

@app.route('/login')
def login():
    try: 
        user = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
        return {'email': user['email']}
    except:
        return '', 401

@socket.on('join_game')
def join_game(args):
    join_room(args['room'])
    emit(args['user'] + ' has joined room', to=args['room'])

@socket.on('submit_question')
def submit_question(args):
    emit(args['user'] + ': ' + args['question'])

@socket.on('pick_winner')
def pick_winner(args):
    emit(args['winner'] + ' wins the round')
    
# thinking about creating rooms
@socket.on('create_game')
def create_game():
    # generate 4 letter code and emit it? 
    pass

if __name__ == '__main__':
    socket.run(app)

# answer presented --> questions received --> winner picked --> repeat
