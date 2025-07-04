from app import app, db
from models import User, Mood, Post, Comment, Reaction

# Drop all tables
def reset_db():
    print(" Dropping and creating tables...")
    db.drop_all()
    db.create_all()

# Seed data
def seed_data():
    print("Seeding data...")

    # Users
    user1 = User(username="jane_doe", email="jane@example.com", password_hash="password123")
    user2 = User(username="john_smith", email="john@example.com", password_hash="mypassword")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Moods
    mood1 = Mood(label="Happy", user=user1)
    mood2 = Mood(label="Sad", user=user2)

    db.session.add_all([mood1, mood2])
    db.session.commit()

    # Posts
    post1 = Post(content="This is Jane's happy post", user=user1, mood=mood1)
    post2 = Post(content="John feels sad today", user=user2, mood=mood2)
    post3 = Post(content="Jane again, but anonymous", is_anonymous=True, user=user1)

    db.session.add_all([post1, post2, post3])
    db.session.commit()

    # Comments
    comment1 = Comment(content="I relate!", user=user2, post=post1)
    comment2 = Comment(content="Feel better!", user=user1, post=post2)

    db.session.add_all([comment1, comment2])
    db.session.commit()

    # Reactions
    reaction1 = Reaction(emoji="❤️", user=user2, post=post1)
    reaction2 = Reaction(emoji="😢", user=user1, post=post2)

    db.session.add_all([reaction1, reaction2])
    db.session.commit()

    print("Done seeding!")

if __name__ == '__main__':
    with app.app_context():
        reset_db()
        seed_data()