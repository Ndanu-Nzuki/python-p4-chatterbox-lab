from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Message API</h1>'

# GET /messages: returns an array of all messages as JSON
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return make_response(jsonify([message.to_dict() for message in messages]), 200)

# POST /messages: creates a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return make_response(jsonify(new_message.to_dict()), 201)

# PATCH /messages/<int:id>: updates the body of the message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    with app.app_context():
        session = db.session
        message = session.get(Message, id)  # Updated to use session.get()
        
        if message is None:
            return make_response(jsonify({"error": "Message not found"}), 404)
        
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

# DELETE /messages/<int:id>: deletes the message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    with app.app_context():
        session = db.session
        message = session.get(Message, id)  # Updated to use session.get()
        
        if message is None:
            return make_response(jsonify({"error": "Message not found"}), 404)

        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({"message": "Message successfully deleted"}), 200)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
