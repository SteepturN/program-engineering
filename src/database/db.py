
from datetime import datetime, timedelta, timezone
from typing import Annotated

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None
