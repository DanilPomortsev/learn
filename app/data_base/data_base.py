import pymongo
import gridfs
from app.settings import settings_

db_client = pymongo.MongoClient("mongodb://fastapidocker-db-1")
db = db_client[settings_.data_base_name]
user = db["user"]
sec_user = db["sec_user"]
post = db["post"]
photo = db["photo"]
comment = db["comment"]
like = db["like"]
fs = gridfs.GridFS(db)

