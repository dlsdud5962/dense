from flask import Blueprint, render_template, request, jsonify, redirect
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/main')
def main_page():
    return render_template('main.html')

@main.route('/main/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        hashed_pw = bcrypt.generate_password_hash(data['pw']).decode('utf-8')
        user = User(userid=data['userid'], pw=hashed_pw, name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    return render_template('signup.html')

@main.route('/main/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(userid=data['userid']).first()
    if user and bcrypt.check_password_hash(user.pw, data['pw']):
        access_token = create_access_token(identity={'userid': user.userid, 'name': user.name})
        return jsonify({'token': access_token, 'username': user.name}), 200
    return jsonify({'message': 'Login failed'}), 401

@main.route('/main/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()
    return jsonify({'username': current_user['name']}), 200
