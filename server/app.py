from flask import Flask, jsonify, session
from models import db, Article
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/articles/<int:id>")
def show_article(id):

    if "page_views" not in session:
        session["page_views"] = 0

    if session["page_views"] >= 3:
        return jsonify({
            "message": "Maximum pageview limit reached"
        }), 401

    article = Article.query.filter_by(id=id).first()

    if not article:
        return jsonify({"message": "Article not found"}), 404

    session["page_views"] += 1

    return jsonify({
        "id": article.id,
        "title": article.title,
        "author": article.author,
        "content": article.content,
        "preview": article.preview,
        "minutes_to_read": article.minutes_to_read,
        "date": article.date
    }), 200


if __name__ == "__main__":
    app.run(debug=True)