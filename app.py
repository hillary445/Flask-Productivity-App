from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from models import db, User, bcrypt, Note

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "User created"}, 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        session["user_id"] = user.id
        return {"message": "Logged in"}, 200

    return {"error": "Invalid credentials"}, 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return {"message": "Logged out"}, 200

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@app.route("/notes", methods=["GET"])
def get_notes():
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    notes = Note.query.filter_by(user_id=user.id)\
        .paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for note in notes.items:
        result.append({
            "id": note.id,
            "title": note.title,
            "content": note.content
        })

    return {
        "notes": result,
        "total": notes.total,
        "pages": notes.pages
    }, 200


@app.route("/notes", methods=["POST"])
def create_note():
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    note = Note(
        title=data["title"],
        content=data["content"],
        user_id=user.id
    )

    db.session.add(note)
    db.session.commit()

    return {"message": "Note created"}, 201


@app.route("/notes/<int:id>", methods=["PATCH"])
def update_note(id):
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note or note.user_id != user.id:
        return {"error": "Not found"}, 404

    data = request.get_json()

    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]

    db.session.commit()

    return {"message": "Updated"}, 200

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    user = get_current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note or note.user_id != user.id:
        return {"error": "Not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Deleted"}, 200

if __name__ == "__main__":
    app.run(debug=True)