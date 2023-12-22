from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from mongo_app.utils import MongoDB
from mongo_app.logger import Logging


logging = Logging(__name__)


class DataPost(APIView):
    def post(self, request):
        try:
            print(request.data)
            logging.info_msg(request.data)
            limit = request.data["limit"]

            logging.info_msg("limit: {0} ".format(limit))
            if limit:
                json_data = MongoDB(limit=limit)
                response = json_data.fetch_data()

                logging.info_msg("response: {0}".format(str(response)))
                return Response({"error": False, "data": response, "message": "Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": True, "data": {}, "message": "error"},
                                status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            logging.error_msg("Key not Present")
            return Response({"error": True, "data": "Key is missing 'limit' and 'offset'", "message": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error_msg(str(e))
            return Response({"error": True, "data": {}, "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilterData(APIView):
    def post(self, request):
        try:
            print(request.data)
            logging.info_msg(request.data)
            limit = request.data["limit"]
            email_address = request.data["email_address"]
            logging.info_msg("limit: {0} ".format(limit))
            if limit:
                json_data = MongoDB(limit=limit)
                response = json_data.filter_data(email_address)

                # logging.info_msg("response: {0}".format(str(response)))
                return Response({"error": False, "data": response, "message": "Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": True, "data": {}, "message": "error"},
                                status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            logging.error_msg("Key not Present")
            return Response({"error": True, "data": "Key is missing 'limit' and 'offset'", "message": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error_msg(str(e))
            return Response({"error": True, "data": {}, "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationDetails(APIView):
    def post(self, request):
        try:
            print(request.data)
            max_records = 10
            if request.data["limit"]:
                max_records = request.data["limit"]

            logging.info_msg("limit: {0}".format(max_records))

            json_data = MongoDB(limit=max_records)
            response = json_data.fetch_loop_data()

            logging.info_msg("response: {0}".format(str(response)))
            return Response({"error": False, "data": response, "message": "Success"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.error_msg(str(e))
            return Response({"error": True, "data": {}, "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailSummaryDetails(APIView):

    def post(self, request, *args, **kwargs):
        try:
            email_id = request.data["email_id"]
            data = {}
            email_summary = request.data.get("email_summary", {})
            email_summary_first = request.data.get("email_summary_first", {})
            draft_message = request.data.get("draft_message", {})
            is_completed = request.data.get("is_completed", {})
            if email_id and is_completed and (email_summary or email_summary_first or draft_message):
                data["is_completed"] = is_completed
                if email_summary:
                    data["summary"] = email_summary
                if email_summary_first:
                    data["summary_first"] = email_summary_first
                if draft_message:
                    data["draft"] = draft_message

                # raw update query
                update_query = {
                    'update': settings.COLLECTION_NAME,
                    'updates': [
                        {
                            'q': {'emailId': email_id},
                            'u': {'$set': data},
                            'multi': False,
                            'upsert': False
                        }
                    ]}

                # Get the MongoDB connection
                update_record = MongoDB()
                response = update_record.insert_data(summary_data=update_query)
                if response:
                    logging.info_msg("response: {0}".format(str(response)))
                    return Response({"error": False, "data": "Record Updated", "message": "Success"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"error": True, "data": {}, "message": "error"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                pass

        except KeyError:
            logging.error_msg("Key not Present")
            return Response({"error": True, "data": "Key is missing 'email_id'", "message": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error_msg(str(e))
            return Response({"error": True, "data": {}, "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestDataPost(APIView):
    def post(self, request):
        try:
            print(request.data)
            logging.info_msg(request.data)
            limit = request.data["limit"]

            logging.info_msg("limit: {0} ".format(limit))
            if limit:
                logging.info_msg("enter")

                json_data = MongoDB(limit=limit)
                response = json_data.test_fetch_data()

                logging.info_msg("response: {0}".format(str(response)))
                return Response({"error": False, "data": response, "message": "Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": True, "data": {}, "message": "error"},
                                status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            logging.error_msg("Key not Present")
            return Response({"error": True, "data": "Key is missing 'limit' and 'offset'", "message": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error_msg(str(e))
            return Response({"error": True, "data": {}, "message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
