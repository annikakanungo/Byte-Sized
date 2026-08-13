# AI Assistance: Portions of this code (debugging, Flask routing patterns, and structure) were developed with assistance from Claude (Anthropic AI). All logic was reviewed, tested, and understood by the author.
from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("flashcards.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    db = get_db()
    cards = db.execute("SELECT * FROM cards").fetchall()
    db.close()
    return render_template("index.html", cards=cards)

@app.route("/add", methods=["POST"])
def add():
    question = request.form.get("question")
    answer = request.form.get("answer")

    if not question or not answer:
        return redirect("/")

    db = get_db()
    db.execute("INSERT INTO cards (question, answer) VALUES (?, ?)", (question, answer))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/study")
def study():
    db = get_db()
    cards = db.execute("SELECT * FROM cards").fetchall()
    db.close()

    if not cards:
        return redirect("/")

    card = random.choice(cards)
    return render_template("study.html", card=card)

@app.route("/answer", methods=["POST"])
def answer():
    card_id = request.form.get("card_id")
    was_correct = request.form.get("result") == "correct"

    db = get_db()
    if was_correct:
        db.execute("UPDATE cards SET correct_count = correct_count + 1 WHERE id = ?", (card_id,))
    else:
        db.execute("UPDATE cards SET incorrect_count = incorrect_count + 1 WHERE id = ?", (card_id,))
    db.commit()
    db.close()

    return redirect("/study")

@app.route("/stats")
def stats():
    db = get_db()
    cards = db.execute("SELECT * FROM cards ORDER BY incorrect_count DESC").fetchall()
    db.close()
    return render_template("stats.html", cards=cards)

@app.route("/delete/<int:card_id>", methods=["POST"])
def delete(card_id):
    db = get_db()
    db.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/edit/<int:card_id>", methods=["GET", "POST"])
def edit(card_id):
    db = get_db()

    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        db.execute("UPDATE cards SET question = ?, answer = ? WHERE id = ?", (question, answer, card_id))
        db.commit()
        db.close()
        return redirect("/")

    card = db.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    db.close()
    return render_template("edit.html", card=card)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
