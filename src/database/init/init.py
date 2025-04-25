#!/usr/bin/env python3

import db
import user_db
import password_db
import message_db
# https://stackoverflow.com/a/8566951
# MongoDB creates databases and collections automatically for you if they
# don't exist already.
from session_params import create_users_db_engine, create_passwords_db_engine
from faker import Faker
fake = Faker()

users_engine = create_users_db_engine()
passwords_engine = create_passwords_db_engine()
db.User.__table__.drop(users_engine, checkfirst=True)
db.Password.__table__.drop(passwords_engine, checkfirst=True)


db.UsersBase.metadata.create_all(users_engine)
db.PasswordsBase.metadata.create_all(passwords_engine)




admin = db.User(
    username="admin",
    email='admin@admin.com',
    disabled=False,
    role=db.UserRole.admin
)


user_db.add_record_user_db(admin)
password_db.add_record_password_db(admin, "secret")

for i in range(10):
    user = db.User(username=fake.unique.name() + "_" + fake.unique.name(),
                   email=fake.unique.email(),
                   disabled=False,
                   role=db.UserRole.user)
    user_db.add_record_user_db(user)
    password_db.add_record_password_db(user, str(hash(user)))
    message_db.add_record_messages_db(user, fake.email(), fake.text())
