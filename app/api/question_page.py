from flask import Blueprint, render_template, request, session, redirect, url_for
from app.socket_events import rooms

# QUIZ = QUIZZES[0]

question_page = Blueprint("question_page", __name__)


@question_page.route("/", methods=["POST", "GET"])
def question():
    room = session.get("room", None)
    name = session.get("room", None)
    if not room or room not in rooms:
        return redirect(url_for("join_game_page.join_view"))

    question_num = rooms[room]["question_index"]
    QUIZ = rooms[room]["quiz"]

    if question_num >= len(QUIZ["questions"]):
        # redirect to scoreboard/end of game results!

        return redirect(url_for('question_page.leaderboard'))

    return render_template(
        "game/question_page.html",
        quiz_title=QUIZ["title"],
        question=QUIZ["questions"][question_num],
        correct=QUIZ["questions"][question_num]["correct"]
    )


@question_page.route("/leaderboard", methods=["POST", "GET"])
def leaderboard():
    room = session.get("room", None)
    print(rooms[room]["usernames"])
    user_scores = {name: data["score"] for name, data in rooms[room]["usernames"].items()}
    user_scores_sorted = sorted(user_scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return render_template("game/leaderboard.html", user_scores=user_scores_sorted,
                           game_over_url=url_for('question_page.game_over'))


@question_page.route("/gameoverpage", methods=["POST", "GET"])
def game_over():
    room = session.get("room", None)
    user_scores = {name: data["score"] for name, data in rooms[room]["usernames"].items()}
    user_scores_sorted = sorted(user_scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[:3]  # Take the top 3
    return render_template("game/game_over_page.html", top_scores=user_scores_sorted)
