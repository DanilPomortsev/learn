import datetime
import fastapi
import pydantic
import app.exeptions as exeptions
from fastapi.security import OAuth2PasswordBearer
from app.data_base.data_base import db, fs
import app.modules.models as models
from typing import List
from fastapi import UploadFile
from bson.objectid import ObjectId
import io
from starlette.responses import StreamingResponse
from passlib.hash import bcrypt
from jose import (
JWTError,
jwt,
)
from app.settings import settings_
#классы с операциями моделек пока только добавление в бд и вывод таблицы с модельками

oauth2_sheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')

def get_current_user(token: str = fastapi.Depends(oauth2_sheme)) -> models.AuthUser:
    return AuthOperations.validate_token(token)

class UserOperation():
    def adding_useravat(self, img: UploadFile, user: models.AuthUser):
        if img.content_type != "image":
            raise exeptions.exeption_not_image
        file_bytes = img.file.read()
        if len(file_bytes) > 120000000:
            raise exeptions.exeption_too_big_file
        key = str(fs.put(file_bytes, filename=img.filename, encoding='utf-8'))
        new_inf = db["user"].find_one({"id": user.id})["information"]
        new_inf["image"] = f"http://127.0.0.1:8000/photo/?id={key}"
        db["user"].update_one({"id": user.id}, {"$set": {"information": new_inf}})
        return new_inf["image"]
    def out_profile(self, id: str):
        user = db["user"].find_one({"id": id})
        if user == None:
            raise exeptions.exeption_no_such_user
        followers = db["SubList"].find({"User2": id})
        six_of_fillowers = []
        quantity = 0
        for elements in followers:
            if quantity == 6:
                break
            photo_fol = db["user"].find_one({"id":elements["User1"]})["information"]["image"]
            six_of_fillowers.append(models.FollowerOut(id=elements["User1"], image=photo_fol))
            quantity += 1

        followings = db["SubList"].find({"User1": id})
        six_of_fillowings = []
        quantity = 0
        for elements in followings:
            if quantity == 6:
                break
            photo_fol = db["user"].find_one({"id": elements["User2"]})["information"]["image"]
            six_of_fillowings.append(models.FollowerOut(id=elements["User2"], image=photo_fol))
            quantity += 1

        posts = db["post"].find({"userId": id})
        twenty_of_post = []
        quantity = 0
        for element in posts:
            if quantity == 20:
                break
            list_of_photo = []
            for photo in element["image"]:
                list_of_photo.append(photo)
            twenty_of_post.append(models.PrePost(idPost=str(element["_id"]), userId=element["userId"], images=list_of_photo,
                nickname=element["nickname"], numberOfLikes=element["numberOfLikes"]))
            quantity += 1

        return models.ProfileOut(id=id, nickname=user["nickname"], information=user["information"], followers=six_of_fillowers,
                                 followings=six_of_fillowings, posts=twenty_of_post)
    def out_settings(self, user: models.AuthUser):
        idd = user.id
        user = db["user"].find_one({"id": idd})
        if user == None:
            raise exeptions.exeption_no_such_user
        password = db["sec_user"].find_one({"_id": ObjectId(idd)})["password"]
        return models.Settings(id=idd, nickname=user["nickname"], password=password, information=user["information"])
    def search(self, nickname: str):
        user = db["user"].find_one({"nickname": nickname})
        if user == None:
            raise exeptions.exeption_no_such_user
        return models.UserOut(id=user["id"], nickname=user["nickname"], image=user["information"]["image"])

class PostOperation():
    def adding_post(self, description: str, images: List[UploadFile], user: models.AuthUser):
        keys = []
        date = str(datetime.datetime.now().date())
        date += datetime.datetime.now().hour + datetime.datetime.now().minute
        for img in images:
            if img.content_type != "image":
                raise exeptions.exeption_not_image
            file_bytes = img.file.read()
            if len(file_bytes) > 120000000:
                raise exeptions.exeption_too_big_file
            keys.append(f"http://127.0.0.1:8000/photo/?id={str(fs.put(file_bytes, filename=img.filename, encoding='utf-8'))}")
        _id = str(db["post"].insert_one({"userId": user.id,
                                         "nickname": user.nickname,
                                         "date": date,
                                         "image": keys,
                                         "description": description,
                                         "numberOfLikes": 0}).inserted_id)

        return models.Post(id=str(_id),
                    userId=user.id,
                    nickname=user.nickname,
                    date=date,
                    images_key=keys,
                    description=description,
                    images = keys)
    def postOut(self, id_: str):
        element = db["post"].find_one({"_id": ObjectId(id_)})
        if element == None:
            raise exeptions.exeption_no_such_post
        Userphotokey = db["user"].find_one({"id": element["userId"]})["information"]["image"]
        UserphotoURL = f"http://127.0.0.1:8000/photo/?id={Userphotokey}"
        if Userphotokey == "Not stated":
            UserphotoURL = Userphotokey
        postout = models.GetPost(id=str(element["_id"]), userId=element["userId"], image=[],
                                 nickname=element["nickname"], description=element["description"],
                                 numberOfLikes=element["numberOfLikes"], date=element["date"])
        for key in element["image"]:
            if Userphotokey == "Not stated":
                postout.image.append(key)
            else:
                postout.image.append(f"http://127.0.0.1:8000/photo/?id={key}")

        comment = db["comment"].find_one({"postId": id_})
        commentator = db["user"].find_one({"id": comment["userId"]})
        commentatorImagekey = commentator["information"]["image"]
        commentatorImageURL = f"http://127.0.0.1:8000/photo/?id={commentatorImagekey}"
        if commentatorImagekey == "Not stated":
            commentatorImageURL = commentatorImagekey
        commentatorNick = commentator["nickname"]
        commentout = models.CommentOut(id=str(comment["_id"]), userId=comment["userId"], date=comment["date"],
                                       text=comment["text"], userImageComment=commentatorImageURL,
                                       nicknameComment=commentatorNick)
        return models.PostOut(userImage=UserphotoURL, post=postout,
                              comment=commentout)
    def getphoto(self, id_:str):
        bytes = io.BytesIO(fs.get(ObjectId(id_)).read())
        return StreamingResponse(bytes, media_type="image/png")
    def getcomments(self, id_:str):
        list = []
        for elements in db["comment"].find({"postId": id_}):
            commentator =db["user"].find_one(({"id": elements["userId"]}))
            list.append(models.CommentOut(id=str(elements["_id"]), userId=elements["userId"],
                                               text=elements["text"],date=elements["date"],
                                               nicknameComment=commentator["nickname"],
                                               userImageComment=commentator["information"]["image"]))
        return list
    def getlikes(self, id_:str):
        list = []
        for elements in db["like"].find({"postId": id_}):
            like_user =db["user"].find_one(({"id": elements["userId"]}))
            list.append(models.LikeOut(id=str(elements["_id"]), userId=elements["userId"],
                                       userImage=like_user["information"]["image"],
                                       nickname=like_user["nickname"]))
        return list

class CommentOperation():
    def adding_comment(self, comment: models.CommentBase, user: models.AuthUser):
        post = db["post"].find_one({"_id":comment.postId})
        if post == None:
            raise exeptions.exeption_no_such_post
        date = str(datetime.datetime.now().date())
        date += datetime.datetime.now().hour + datetime.datetime.now().minute
        element = db["comment"].insert_one({"userId": user.id,
                                            "postId": comment.postId,
                                            "text": comment.text,
                                            "date": date})

        return models.Comment(id=str(element.inserted_id),
                              userId=user.id,
                              postId=comment.postId,
                              text=comment.text,
                              date=date)

class LikeOperation():
    def adding_like(self, like: models.LikeBase, user: models.AuthUser):
        post = db["post"].find_one({"_id": like.postId})
        if post == None:
            raise exeptions.exeption_no_such_post
        element = db["like"].insert_one({"userId": user.id,
                                         "postId": like.postId})
        return models.Like(id=str(element.inserted_id),
                           userId=user.id,
                           postId=like.postId)

class SubListOperation():
    def adding_sub(self, subscription: str, user: models.AuthUser):
        sub = db["user"].find_one({"id": subscription})
        if sub == None:
            raise exeptions.exeption_no_such_user
        element = db["SubList"].insert_one({"user1": user.id,
                                         "user2": subscription})
        return models.SubList(id=str(element.inserted_id),
                           user1=user.id,
                           user2=subscription)

class TapeOperation():
    def tape_out(self, user: models.AuthUser):
        sub = db["SubList"].find({"user1": user.id})
        id_of_sub = []
        for element in sub:
            id_of_sub.append(element["user2"])
        list_of_post = db["post"].find({"userId": {"$in": id_of_sub}})
        result = []
        count = 0
        for element in list_of_post:
            list_of_photo = []
            for photo in element["image"]:
                list_of_photo.append(photo)
            post_out = models.PrePost(idPost=str(element["_id"]), userId=element["userId"], images=list_of_photo,
                nickname=element["nickname"], numberOfLikes=element["numberOfLikes"])
            result.append(post_out)
            if count == 20:
                break
        return result

class AuthOperations():
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> models.AuthUser:
        try:
            payload = jwt.decode(
                token,
                settings_.jwt_secret,
                algorithms=[settings_.jwt_algoritm]
            )
        except JWTError:
            raise exeptions.exeption_not_validate_creditnails from None
        user_data = payload.get("user")
        try:
            user = models.AuthUser.parse_obj(user_data)
        except pydantic.ValidationError:
            raise exeptions.exeption_not_validate_creditnails from None
        return user

    @classmethod
    def create_token(cls, user_data: models.AuthUser) -> models.Token:
        now = datetime.datetime.utcnow()
        payload = {
            'iat':now,
            'nbf':now,
            'exp': now + datetime.timedelta(seconds=settings_.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token: str = jwt.encode(
            payload,
            settings_.jwt_secret,
            algorithm=settings_.jwt_algoritm
        )
        return models.Token(access_token=token)

    def register_new_user(self, user_data: models.UserBase) -> models.Token:
        find = db["sec_user"].find_one({"nickname":user_data.nickname})
        if find != None:
            raise exeptions.exeption_nick
        if len(user_data.password) < 3:
            raise exeptions.exeption_password
        if len(user_data.password) > 50:
            raise exeptions.exeption_long_password
        if len(user_data.nickname) > 50:
            raise exeptions.exeption_long_nickname
        if len(user_data.nickname) == 0:
            raise exeptions.exeption_no_nickname
        if len(user_data.password) == 0:
            raise exeptions.exeption_no_password

        sec_element = db["sec_user"].insert_one({"nickname": user_data.nickname, "password": self.hash_password(user_data.password)})
        id = str(sec_element.inserted_id)
        user_auth = models.AuthUser(nickname=user_data.nickname, id=id)
        db["user"].insert_one({"id": id,
                               "nickname": user_data.nickname,
                               "information": {
                                   "description": "Not stated",
                                   "firstname": "Not stated",
                                   "secondname": "Not stated",
                                   "image": "Not stated",
                                   "dateOfBirth": "Not stated",
                                   "gender": "Not stated"}})
        return self.create_token(user_auth)

    def authenticate_user(self, user_data: models.UserBase) -> models.Token:
        if len(user_data.password) > 50:
            raise exeptions.exeption_long_password
        if len(user_data.nickname) > 50:
            raise exeptions.exeption_long_nickname
        if len(user_data.nickname) == 0:
            raise exeptions.exeption_no_nickname
        if len(user_data.password) == 0:
            raise exeptions.exeption_no_password
        user = db["sec_user"].find_one({"nickname": user_data.nickname})
        if not user:
            raise exeptions.exeption_not_validate_creditnails
        if not self.verify_password(user_data.password, user["password"]):
            raise exeptions.exeption_not_validate_creditnails
        return self.create_token(models.AuthUser(id=str(user["_id"]), nickname=user_data.nickname))

