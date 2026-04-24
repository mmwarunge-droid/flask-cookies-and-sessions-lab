from flask import Flask, jsonify, session
from models import db, Article

app = Flask(__name__)
app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

@app.route('/articles/<int:id>')
def show_article(id):
    # initialize session counter
    if "page_views" not in session:
        session["page_views"] = 0

    # block after 3 views
    if session["page_views"] >= 3:
        return jsonify({
            "message": "Maximum pageview limit reached"
        }), 401

    # find article by id
    article = next((article for article in articles if article["id"] == id), None)

    if not article:
        return jsonify({"message": "Article not found"}), 404

    # increment views after successful view
    session["page_views"] += 1

    return jsonify(article), 200


if __name__ == '__main__':
    app.run(port=5555)
