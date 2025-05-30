#!/usr/bin/env python3
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import message_db
from db import User
import auth

app = FastAPI(redirect_slashes=False)


@app.get("/message/{message_id}")
async def find_message(
        message_id: str,
        current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    if not (message := message_db.get_record_messages_db(current_user,
                                                         message_id)):
        raise HTTPException(status_code=404, detail="Message doesn't exist")
    return message


@app.post("/message")
async def create_message(
        message: str,
        to_email: str,
        current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    if not (result := message_db.add_record_messages_db(
            current_user, to_email, message)):
        raise HTTPException(status_code=404,
                            detail="Database error, message is not created")
    return HTMLResponse(status_code=200,
                        content=f"Success. Message id = {result.id}")
