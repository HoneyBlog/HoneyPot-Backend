from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.models import User, Post
from schemas.schemas import UserCreate, PostCreate
from uuid import uuid4
import jwt
from datetime import datetime, timedelta
import bcrypt
import logging
from services.utils import user_validaton, is_valid_uuid

# Replace with your secret key in a real application
SECRET_KEY = "your-secret-key"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Users CRUD
def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    user_validaton(user)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(id=str(uuid4()), username=user.username, email=user.email, password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def check_login(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logging.info("User not found")
        raise ValueError("Invalid username or password")

    logging.info(f"Found user: {user.username}, hashed password in DB: {user.password}")

    # Check the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        logging.info("Password check failed")
        raise ValueError("Invalid username or password")

    logging.info("Password check succeeded")

    # Generate JWT token
    token = jwt.encode({
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }, SECRET_KEY, algorithm='HS256')

    return token, user.id

# Posts CRUD
def get_posts(db: Session):
    return db.query(Post).all()

def create_post(db: Session, post: PostCreate):
    is_valid_uuid(post.author_id)    
    db_post = Post(id=str(uuid4()), content=post.content, comments_number=0, likes_number=0, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# Check JWT token : return bool if token is valid
def check_token(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception:
        return False
