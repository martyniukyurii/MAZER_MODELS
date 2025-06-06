from motor.motor_asyncio import AsyncIOMotorClient

import data.config as CONFIG
import logging

# Model: personal info -> fullname(regex), citizenship, email(regex), phone_number(regex),
# telegram_id<hide>, agent_id<hide>, balance
# measurements -> height, bust, waist, hips, shoe size, hair color
# social media -> links

# Agent: personal info -> name,
# Pictures: models_id<hide>, name, date, country_of_shooting, team, links, telegram_pic
# Configuration: docs ->
# BannedUsers: telegram_id, name, username
# InQueue: telegram_id, name, username
# Contract: model_id, date,
# Vacancies(Options)
# Docs: model_id, expired<bool>


uri = f"mongodb://{CONFIG.LOGIN}:{CONFIG.PASSWORD}@{CONFIG.IP}:{CONFIG.PORT}/"


async def save_to_db(collection_name: str, data: dict):
    try:
        client = AsyncIOMotorClient(uri)
        db = client[CONFIG.DB_NAME]
        collection = db[collection_name]
        result = await collection.insert_one(data)
    except Exception as e:
        logging.error(f"Exception caught while trying to save data to collection '{collection_name}': {e}")


async def find_in_db(collection_name: str, data: dict):
    client = AsyncIOMotorClient(uri)
    db = client[CONFIG.DB_NAME]
    collection = db[collection_name]
    result = await collection.find_one(data)
    return result


async def find_many_in_db(collection_name: str, data: dict):
    client = AsyncIOMotorClient(uri)
    db = client[CONFIG.DB_NAME]
    collection = db[collection_name]
    result = collection.find(data)
    return await result.to_list(length=None)


async def update_to_db(collection_name: str, parameter: dict, data: dict):
    try:
        client = AsyncIOMotorClient(uri)
        db = client[CONFIG.DB_NAME]
        collection = db[collection_name]
        update = {'$set': data}
        result = await collection.update_one(parameter, update)
    except Exception as e:
        logging.error(f"Exception caught while trying to update data to collection '{collection_name}': {e}")


async def delete_from_db(collection_name: str, data: dict):
    try:
        client = AsyncIOMotorClient(uri)
        db = client[CONFIG.DB_NAME]
        collection = db[collection_name]
        result = await collection.delete_one(data)
        if result.deleted_count == 0:
            logging.warning(f"No document matched the filter criteria in collection '{collection_name}'.")
        else:
            logging.info(f"Document deleted successfully from collection '{collection_name}'.")
    except Exception as e:
        logging.error(f"Exception caught while trying to delete data from collection '{collection_name}': {e}")