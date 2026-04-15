from app import app
from models import db, User, Note, bcrypt
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("Seeding database...")

    #Clear existing data
    Note.query.delete()
    User.query.delete()

    #Create Users
    users = []
    for i in range(5):
        user = User(username=fake.user_name())
        user.set_password("password123")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    #Create Notes for each user
    for user in users:
        for _ in range(5):
            note = Note(
                title=fake.sentence(nb_words=4),
                content=fake.text(),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()

    print("✅ Done seeding!")