#!/usr/bin/env python3
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
import auth
import user_db
from db import User

app = FastAPI()


@app.get("/user/me", response_model=User)
async def user_info(
    current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    return current_user


@app.get("/user/{user_login}", response_model=User)
async def find_user(
        user_login: str,
        current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    if not user_db.is_admin(user=current_user):
        raise HTTPException(status_code=404, detail="Issuer is not an admin")
    if not (user := user_db.get_user("username", user_login)):
        raise HTTPException(status_code=404, detail="User is not found")
    return user


@app.post("/user", response_model=User)
async def create_user(
        username: str,
        email: str,
        password: str,
        current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    if not (res := user_db.add_user(
            User(username=username, email=email, disabled=False), password)):
        raise HTTPException(status_code=404, detail="User already exist")

    return res
