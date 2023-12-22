import pymongo
import json
from django.conf import settings
from mongo_app.logger import Logging
from bson import json_util


logging = Logging(__name__)


class MongoDB:
    def __init__(self, limit=0, offset=0):
        self.limit = limit
        self.offset = offset
        self.my_client = pymongo.MongoClient(settings.CONNECTION_STRING)
        self.my_db = self.my_client[settings.DATABASE_NAME]
        self.my_col = self.my_db[settings.COLLECTION_NAME]
        self.records = []
        self.email = []

    def test_fetch_data(self):
        my_col = self.my_db["email1"]
        logging.info_msg(
            "ConnectionString: {0}, Database: {1}, Collection: {2}".format(self.my_client, self.my_db, my_col))
        latest_records = my_col.find().limit(self.limit).sort("date", -1)

        for data in latest_records:
            self.records.append(json.loads(json_util.dumps(data)))
        return self.records

    def fetch_data(self):
        filter_criteria = {
            '$and': [
                {"is_completed": True}
            ]
        }
        logging.info_msg(
            "ConnectionString: {0}, Database: {1}, Collection: {2}".format(self.my_client, self.my_db, self.my_col))
        latest_records = self.my_col.find(filter_criteria).limit(self.limit).sort("date", -1)

        for data in latest_records:
            self.records.append(json.loads(json_util.dumps(data)))
        return self.records

    def filter_data(self, email_address):

        filter_criteria = {
            '$and': [
                {"is_completed": True},
                {'$or': [
                    {"to": email_address},
                    {"cc": email_address}
                ]}
            ]
        }
        logging.info_msg(
            "ConnectionString: {0}, Database: {1}, Collection: {2}".format(self.my_client, self.my_db, self.my_col))
        latest_records = self.my_col.find(filter_criteria).limit(self.limit).sort("date", -1)

        logging.info_msg("filter records: {0}".format(latest_records))
        for data in latest_records:
            self.records.append(json.loads(json_util.dumps(data)))
        return self.records

    def fetch_loop_data(self):

        logging.info_msg(
            "ConnectionString: {0}, Database: {1}, Collection: {2}".format(self.my_client, self.my_db, self.my_col))
        conversations = self.my_col.aggregate([{"$group": {"_id": "$conversationId", "totalCount": {"$sum": 1}}},
                                               {"$sort": {"date": -1}}
                                               ])

        data = []
        for conversation in conversations:
            logging.info_msg("Thread Detail: {0}".format(conversation))
            email = self.my_col.find({"conversationId": conversation["_id"]})
            data.append(email)

        for datas in data:
            self.email.append(json.loads(json_util.dumps(datas)))
        return self.email

    def insert_data(self, summary_data):
        try:
            logging.info_msg("summary_data: {0}".format(summary_data))
            # Execute the raw update
            query_result = self.my_db.command(summary_data)
            print(query_result)
            logging.info_msg("update_response: {0}".format(query_result))
            return True
        except Exception as e:
            logging.error_msg(str(e))
            return False
