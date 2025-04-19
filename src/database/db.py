
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase
from enum import Enum
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base


class UserRole(str, Enum):
    admin = 'admin'
    user  = 'user'


# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

UsersBase = declarative_base()
PasswordsBase = declarative_base()


class User(UsersBase):
    __tablename__ = "user_account"
    username:  Mapped[str]      = mapped_column(String(300), primary_key=True)
    email:     Mapped[str]      = mapped_column(String(300))
    disabled:  Mapped[bool]     = mapped_column(Boolean, default=False)
    # it can be searched, maybe, indexes created on primary key anyway
    role:      Mapped[UserRole] = mapped_column(String(300), default=UserRole.user, index=True)

    def __repr__(self) -> str:
        return f"User({self.username} {self.email} {self.disabled} {self.role})"


class Password(PasswordsBase):
    __tablename__               = "user_passwords"
    # hypothetically should be in other db - so no foreign key
    # username:Mapped[str]      = relationship("User", cascade="all, delete")
    username:        Mapped[str]      = mapped_column(primary_key=True)
    hashed_password: Mapped[str]      = mapped_column(String(300))

    def __repr__(self) -> str:
        return f"Password({self.username} {self.hashed_password})"


class UserResponse(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None
    role: UserRole

    def __init__(self, user: User):
        super().__init__(username=user.username, email=user.email,
                         disabled=user.disabled, role=user.role)


class Message(BaseModel):
    id: str
    from_email: str
    to_email: str
    data: str
