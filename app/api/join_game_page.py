from flask import Blueprint, render_template, request, session, url_for, redirect
import random
from string import ascii_uppercase
from app.socket_events import rooms
from app.fixtures.quiz_generate import generate_quiz
import requests

# join_game blueprint for landing page of app
# should maintain logic over joining quiz queue and redirection to game_room

join_game_page = Blueprint("join_game_page", __name__)


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


@join_game_page.route("/", methods=["POST", "GET"])
def join_view():
    # receives POST request from form listed in join_game_page.html
    if request.method == "POST":

        # if name input is provided log the name, store data in session object, redirect user
        # else no name, display current template and send error to template

        join_name = request.form.get('join_name')
        create_name = request.form.get('create_name')

        name = join_name or create_name

        code = request.form.get("code").upper()
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name and not code:
            if session.get('room') and rooms.get(session['room']):
                return redirect(url_for(rooms[session['room']]['page']))
            else:
                return render_template('game/join_game_page.html', error="You have no active games!", code=code, name=name)

        if not name:
            return render_template(
                "game/join_game_page.html",
                error="Please enter a name.",
                code=code,
                name=name,
            )

        if join and not code:
            return render_template(
                "game/join_game_page.html",
                error="Please enter a room code.",
                code=code,
                name=name,
            )

        room = code

        if create != False:
            room = generate_unique_code(4)
            quiz = generate_quiz(9)
            rooms[room] = {"usernames": {}}
            rooms[room]["usernames"] = {name: {"score": 0, "active": True}}
            rooms[room]["question_index"] = 0
            rooms[room]["timer_started"] = False
            rooms[room]["replies"] = 0
            rooms[room]["page"] = "game_room_page.join_view"
            rooms[room]["quiz"] = quiz

        elif code not in rooms:
            return render_template(
                "game/join_game_page.html",
                error="Room does not exist.",
                code=code,
                name=name,
            )
        elif name.lower() in rooms[room]["usernames"]:
            return render_template(
                "game/join_game_page.html",
                error="Username already exists, please list another name",
            )

        session["name"] = name
        session["room"] = room
        session["score"] = 0

        return redirect(url_for("game_room_page.join_view"))

    return render_template("game/join_game_page.html")
