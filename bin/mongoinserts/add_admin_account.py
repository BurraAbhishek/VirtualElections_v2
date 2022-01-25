from setup.admin_account import admin_username, admin_password
from django.contrib.auth.hashers import make_password, is_password_usable
from bin.mongodb import mongo_client

admin_hash = make_password(password=admin_password)
if not is_password_usable(admin_hash):
    raise Exception("Invalid password")

admin_details = {
    "_id": admin_username,
    "password": admin_hash
}


def add_admin():
    mongo_client.db_insert_one(collection="mod1", data=admin_details)
