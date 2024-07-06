from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import UserCreate, User, PostCreate, Post, LoginRequest
from services.crud import create_user, create_post, get_users, check_login, get_posts, get_user_by_id, check_token
from config.database import get_db, test_connection, create_tables

test_connection()
create_tables()

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Server is running"}

# Users APIs
@router.get("/api/users/", response_model=list[User])
async def get_users_endpoint(db: Session = Depends(get_db)):
    users = get_users(db)
    for user in users:
        user.id = str(user.id)
    return users

@router.get("/api/users/{user_id}", response_model=User)
async def get_user_by_id_endpoint(user_id: str, db: Session = Depends(get_db)):
        try:
            user = get_user_by_id(db, user_id)
            user.id = str(user.id)
            return user
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
@router.post("/api/users/", response_model=User)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user)
    user.id = str(user.id)
    return user

@router.post("/api/users/login/")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    try:
        token, user_id = check_login(db, login_request.username, login_request.password)
        return {"token": token,"user_id": user_id}  # Assuming 'user' is the JWT token

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/api/users/check-token/")
async def check_token_endpoint(token: str):
    return {"valid": check_token(token)}

# Posts APIs
@router.get("/api/posts/", response_model=list[Post])
async def get_posts_endpoint(db: Session = Depends(get_db)):
    posts = get_posts(db)
    for post in posts:
        post.id = str(post.id)
        post.author_id = str(post.author_id)
    return posts

@router.post("/api/posts/", response_model=Post)
async def create_post_endpoint(post: PostCreate, db: Session = Depends(get_db)):
    post = create_post(db, post)
    post.id = str(post.id)
    post.author_id = str(post.author_id)
    return post

