#!/usr/bin/env python3

from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import password_db
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, Token, create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/#simple-requests
# swagger started to use OPTIONS all of a sudden
# and
# without this shit it fucking blows
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = password_db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "username\n" + form_data.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
