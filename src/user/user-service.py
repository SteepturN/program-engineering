#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
import auth
import user_db
import password_db
from db import User, UserResponse, UserRole

app = FastAPI()


@app.get("/user/me", response_model=UserResponse)
async def user_info(
    current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    return UserResponse(current_user)


@app.get("/user/{user_login}", response_model=UserResponse)
async def find_user(
        user_login: str,
        current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    if not user_db.is_admin(user=current_user):
        raise HTTPException(status_code=404, detail="Issuer is not an admin")
    if not (user := user_db.get_user(username=user_login)):
        raise HTTPException(status_code=404, detail="User is not found")
    return UserResponse(user)


@app.post("/user", response_model=UserResponse)
async def create_user(
        username: str,
        email: str,
        password: str,
        role: UserRole,
        current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    if not user_db.is_admin(current_user):
        raise HTTPException(status_code=404,
                            detail="You don't have rights for user creation")
    new_user = User(username=username, email=email, disabled=False, role=role)
    if not (res := user_db.add_user(new_user)):
        raise HTTPException(status_code=404, detail="User already exist")
    if not password_db.add_user(new_user, password):
        user_db.delete_user(new_user)
        raise HTTPException(status_code=404, detail="Password DB error")

    return UserResponse(res)
