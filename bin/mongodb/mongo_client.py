import pymongo


def getConnection():
    # Name of the database
    databaseName = "virtualelections"

    # Server address. Default is localhost:27017
    serveraddr = "mongodb://localhost:27017"

    # Client
    client = pymongo.MongoClient(serveraddr)

    # Database
    database = client[databaseName]

    return database


def ifCollectionExists(database, collection) -> bool:
    result = False
    collection_list = database.list_collection_names()
    if collection in collection_list:
        result = True
    return result


def db_get_collection(collection):
    database = getConnection()
    if not ifCollectionExists(database, collection):
        database.create_collection(collection)
    db_collection = database.get_collection(collection)
    return db_collection


def db_insert_one(collection, data):
    db_collection = db_get_collection(collection)
    db_collection.insert_one(data)
