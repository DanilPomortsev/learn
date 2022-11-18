import fastapi
exeption_nick = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="This nickname is alredy occupied. Choose another one",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)
exeption_password = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="The password is too easy. Enter a threshold of 3 characters or more",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)
exeption_long_nickname = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="The nickname is too long. It must be less than 50 simbols",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)
exeption_long_password = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="The password is too long. It must be less than 50 simbols",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)
exeption_no_nickname = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Enter nickname",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)
exeption_no_password = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Enter password",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)

exeption_not_validate_creditnails = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentails",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)

exeption_not_image = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Upload another file. Avatar must be a image",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)

exeption_too_big_file = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Too big file. It must be less than 120MB",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)

exeption_no_such_user = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="No such user",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)

exeption_no_such_post = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="No such user",
    headers={
        "WWW-Authenticate": "Bearer"
    }
)