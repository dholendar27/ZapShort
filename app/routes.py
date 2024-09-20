from flask import Blueprint, make_response, redirect
from flask import request
from flask import Response
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .models import User, Link
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
import random
import string
main = Blueprint('users', '__name__')


def generate_token(username):
    return {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }


def generate_code(length=6):
    return "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


def unique_short():
    while True:
        code = generate_code()
        if not Link.query.filter_by(shortCode=code).first():
            return code


def get_link(short_code,):
    return Link.query.filter_by(shortCode=short_code).first()


@main.route('/signup', methods=['POST'])
def signup():
    message = ""
    firstname = request.json.get("firstname", None)
    lastname = request.json.get("lastname", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not firstname:
        message = {
            "message": "First name is required. Please provide your first name."}
        return jsonify(message), 400
    elif not email:
        message = {
            "message": "Email address is required. Please provide a valid email."}
        return jsonify(message), 400
    elif not password:
        message = {"message": "Password is required. Please enter your password."}
        return jsonify(message), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    # Create the new user
    new_user = User(first_name=firstname, last_name=lastname, email=email)
    new_user.password = generate_password_hash(password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully!",
        "data": {
            "id": new_user.id,
            "firstname": new_user.first_name,
            "lastname": new_user.last_name,
            "email": new_user.email
        }
    }), 201


@main.route("/login", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        message = {
            "message": "Email address is required. Please provide a valid email."}
        return jsonify(message), 400
    elif not password:
        message = {"message": "Password is required. Please enter your password."}
        return jsonify(message), 400

    user = User.query.filter_by(email=email).first()
    check_password = check_password_hash(user.password, password=password)

    if check_password:
        token = generate_token(user.first_name)
        response = make_response(jsonify({
            "message": "Login Successfull",
            "data": {
                "id": user.id,
                "firstname": user.first_name,
                "lastname": user.last_name,
                "email": user.email
            },
            "access_token": token.get('access_token')
        }))
        response.set_cookie('refresh_token', token.get(
            'refresh_token'), httponly=True, secure=True)
        return response
    return jsonify({
        "message": "Invalid email or password. Please try again",
    }), 401


@main.route("/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@main.route('/shorten', methods=['POST'])
@jwt_required()
def create_short_code():
    url = request.json.get("url", None)
    user_id = request.json.get("user_id", None)
    user = User.query.filter(id=user_id).first()
    if not user:
        return jsonify(message="Invalid user, please try again")
    if not url:
        return jsonify(message="URL is required. Please provide a valid URL")
    shortCode = unique_short()
    link = Link(url=url, shortCode=shortCode, user_id=user_id)

    db.session.add(link)
    db.session.commit()

    url = get_link(shortCode)
    return jsonify({
        "message": "Link added Successfully",
        "data": {
            "id": url.id,
            "url": url.url,
            "shortCode": url.shortCode,
            "createdAt": url.createdAt,
            "updatedAt": url.updatedAt,
        }
    }), 201


@main.route('/shorten/<code>', methods=['PUT'])
@jwt_required()
def update_url(code):
    url = request.json.get('url', None)
    user_id = request.json.get('user_id', None)
    link = Link.query.filter_by(shortCode=code, user_id=user_id).first()
    if not link:
        return jsonify(message="Link not found or you don't have permission to update it."), 404
    link.url = url
    db.session.commit()
    url = get_link(code)
    return jsonify({
        "message": "Link added Successfully",
        "data": {
            "id": url.id,
            "url": url.url,
            "shortCode": url.shortCode,
            "createdAt": url.createdAt,
            "updatedAt": url.updatedAt,
        }
    }), 201


@main.route('/shorten/<code>', methods=["DELETE"])
@jwt_required()
def delete_link(code):
    user_id = request.json.get('user_id', None)
    link = Link.query.filter_by(shortCode=code, user_id=user_id).first()
    db.session.delete(link)
    db.session.commit()
    return jsonify(message="Link has been deleted successfully."), 200


@main.route('/links', methods=['GET'])
@jwt_required()
def get_all_links():
    user_id = request.json.get('user_id', None)
    links = Link.query.filter_by(user_id=user_id).all()
    links_data = []
    for link in links:
        links_data.append({
            "id": link.id,
            "shortCode": link.shortCode,
            "url": link.url,
            "created_at": link.createdAt,
            "updated_at": link.updatedAt
        })
    return jsonify({
        "message": "Links retrieved successfully",
        "data": links_data
    }), 200


@main.route('/shorten/<code>', methods=['GET'])
def redirect_url(code):
    link = Link.query.filter_by(shortCode=code).first()
    print(link)
    return redirect(link.url)
