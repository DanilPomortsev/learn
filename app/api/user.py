import fastapi
from fastapi import APIRouter,FastAPI, File, UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import app.modules.models as models
import app.services.user as operation
import app.services.user as services


app = FastAPI()
auth_router = APIRouter(prefix='/auth')
photo_router = APIRouter(prefix='/photo')
user_router = APIRouter(prefix='/user')
post_router = APIRouter(prefix="/post")
sub_router = APIRouter(prefix="/subscription")


@auth_router.post('/sign-up', response_model=models.Token)
def sign_up(user_data: models.UserBase, service: operation.AuthOperations = fastapi.Depends()):
    return service.register_new_user(user_data)

@auth_router.post('/sign-in', response_model=models.Token)
def sign_in(form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
            service: operation.AuthOperations = fastapi.Depends()):
    return service.authenticate_user(models.UserBase(nickname=str(form_data.username)
                                                     ,password=str(form_data.password)))

@user_router.post('/avatar', response_model=str)
def create_user_avatar(image: UploadFile = File(...), user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.UserOperation().adding_useravat(image, user)

@post_router.post('/', response_model=models.Post)
def create_post(description: str = Form(...),images: List[UploadFile] = File(...),
                user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.PostOperation().adding_post(description, images, user)

@post_router.get('/', response_model=models.PostOut)
def get_post(id: str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.PostOperation().postOut(id)

@post_router.get('/comment', response_model=List[models.CommentOut])
def get_comments_post(id: str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.PostOperation().getcomments(id)

@post_router.get('/like', response_model=List[models.LikeOut])
def get_likes(id: str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.PostOperation().getlikes(id)

@photo_router.get('/')
def get_photo(id: str):
    return operation.PostOperation().getphoto(id)

@post_router.post('/comment', response_model=models.Comment)
def create_comment(comment: models.CommentBase, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.CommentOperation().adding_comment(comment, user)

@post_router.post('/like', response_model=models.Like)
def create_like(like : models.LikeBase, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.LikeOperation().adding_like(like, user)

@sub_router.post('/', response_model=models.SubList)
def create_sub(sub: str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.SubListOperation().adding_sub(sub, user)

@user_router.get('/profile', response_model=models.ProfileOut)
def get_profile(id: str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.UserOperation().out_profile(id)

@user_router.get('/tape', response_model=List[models.PrePost])
def get_tape(user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.TapeOperation().tape_out(user)

@user_router.get('/settings', response_model=models.Settings)
def get_settings(user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.UserOperation().out_settings(user)

@user_router.get('/search', response_model=models.UserOut)
def user_search(nickname : str, user: models.AuthUser = fastapi.Depends(services.get_current_user)):
    return operation.UserOperation().search(nickname)


