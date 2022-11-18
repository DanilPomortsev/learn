from pydantic import BaseModel
from typing import List

#модельки
class UserInf(BaseModel):
    description: str = "Not stated"
    firstname: str = "Not stated"
    secondname: str = "Not stated"
    image: str = "Not stated"
    dateOfBirth: str = "Not stated"
    gender: str = "Not stated"

class UserBase(BaseModel):
    nickname: str
    password: str

class User(UserBase):
    id:str
    inf:UserInf

class AuthUser(BaseModel):
    nickname: str
    id: str

class PostBase(BaseModel):
    userId: str
    nickname: str
    date: str
    description: str

class Post(PostBase):
    id: str
    numberOfLikes: int = 0
    images: List[str]

class CommentBase(BaseModel):
    postId: str
    text: str

class Comment(CommentBase):
    id: str

class CommentGet(BaseModel):
    id: str
    userId: str
    text: str
    date: str

class LikeBase(BaseModel):
    postId: str

class Like(LikeBase):
    id: str

class LikeOut(BaseModel):
    userId: str
    userImage: str
    nickname: str
    id : str

class GetPost(BaseModel):
    id: str
    userId: str
    nickname: str
    date: str
    image: List[str]
    description: str
    numberOfLikes: int

class CommentOut(BaseModel):
    id: str
    userId: str
    text: str
    date: str
    nicknameComment: str
    userImageComment: str

class PostOut(BaseModel):
    userImage: str
    post: GetPost
    comment: CommentOut

class SubList(BaseModel):
    user1: str
    user2: str

class FollowerOut(BaseModel):
    id: str
    image: str

class PrePost(BaseModel):
    idPost: str
    userId: str
    images: List[str]
    nickname: str
    numberOfLikes: int

class ProfileOut(BaseModel):
    id: str
    nickname: str
    information: UserInf
    followers: List[FollowerOut]
    followings: List[FollowerOut]
    posts: List[PrePost]

class Settings(BaseModel):
    id: str
    nickname: str
    password: str
    information: UserInf

class UserOut(BaseModel):
    id: str
    nickname: str
    image: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

