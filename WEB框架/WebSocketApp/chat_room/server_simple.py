from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('home.html')


@socketio.on('send msg')
def handle_my_customer_namespace_event(data):
    socketio.emit('res', data)


if __name__ == '__main__':
    print('running')
    socketio.run(app)
