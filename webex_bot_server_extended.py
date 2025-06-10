# -*- coding: utf-8 -*-

"""This module contains the Webex Bot Server component."""

import json
import logging

from ciscosparkapi import CiscoSparkAPI
from flask import Flask, request
import requests

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation

from components.user_db_operations import UserDBOperations
from cards.AuthenticationAdaptiveCard import AuthenticationAdaptiveCard

CISCO_API_URL = "https://api.ciscospark.com/v1"
ACCESS_TOKEN_WITH_BEARER = "Bearer "
BAD_REQUEST_NAME = "BAD REQUEST"
BAD_REQUEST_CODE = 400
APPROVED_REQUEST_NAME = "OK"
APPROVED_REQUEST_CODE = 200

class WebexBotServerException(Exception):
    pass


class WebexBotServerExtended:
    """
    A sample server class for Webex Teams integration with any MindMeld application
    """

    def __init__(self, name, app_path, nlp=None, message_webhook_id=None, card_webhook_id=None, access_token=None, db_config=None):
        """
        Args:
            name (str):                     The name of the server.
            app_path (str):                 The path of the MindMeld application.
            nlp (NaturalLanguageProcessor): MindMeld NLP component, will try to load from app path if None.
            message_webhook_id (str):       Webex Team webhook id for messages resources, will raise exception if not passed.
            card_webhook_id (str):          Webex Team webhook id for attachmentActions resources, will raise exception if not passed.
            access_token (str):             Webex Team bot access token, will raise exception if not passed.
            db_config (dict):               The user database configurations.
        """

        #* Attribute Initialisations *#
        self.app = Flask(name)
        self.message_webhook_id = message_webhook_id
        self.card_webhook_id = card_webhook_id
        self.access_token = access_token

        if not self.message_webhook_id:
            raise WebexBotServerException("MESSAGE_WEBHOOK_ID not set")
        if not self.card_webhook_id:
            raise WebexBotServerException("CARD_WEBHOOK_ID not set")
        if not self.access_token:
            raise WebexBotServerException("BOT_ACCESS_TOKEN not set")
        
        if not nlp:
            self.nlp = NaturalLanguageProcessor(app_path)
            self.nlp.load()
        else:
            self.nlp = nlp
        self.conv = Conversation(nlp=self.nlp, app_path=app_path)

        self.logger = logging.getLogger(__name__)

        self.spark_api = CiscoSparkAPI(self.access_token)
        self.access_token_with_bearer = ACCESS_TOKEN_WITH_BEARER + self.access_token

        # Database connection
        if db_config:
            self.db_operations = UserDBOperations(db_config)
        else:
            self.db_operations = None

        self._register_routes()

    def _register_routes(self):
        """
        Register the Flask routes for handling incoming webhooks.
        """

        @self.app.route("/message", methods=["POST"])
        def handle_primary_webhook():
            data = request.get_json()
            me = self.spark_api.people.me()
            person_id = data["data"]["personId"]
            # if person_id != me.id:
            #     print("Received on message webhook:", data)

            return self._handle_message()

        @self.app.route("/card", methods=["POST"])
        def handle_secondary_webhook():
            data = request.get_json()
            me = self.spark_api.people.me()
            person_id = data["data"]["personId"]
            # if person_id != me.id:
            #     print("Received on card webhook:", data)

            return self._handle_card()

        @self.app.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def test_route():
            return 'This is a test route to check if the server is reachable.\n'

    def _handle_message(self):
        me = self.spark_api.people.me()
        data = request.get_json()

        for key in ["personId", "id", "roomId"]:
            if key not in data["data"].keys():
                payload = {"message": "personId/id/roomID key not found"}
                return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload

        if data["id"] != self.message_webhook_id:
            self.logger.debug("Retrieved message_webhook_id %s doesn't match", data["id"])
            payload = {"message": "message_webhook_id mismatch"}
            return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload

        person_id = data["data"]["personId"]
        msg_id = data["data"]["id"]
        room_id = data["data"]["roomId"]
        txt = self._get_message(msg_id)

        if "text" not in txt:
            payload = {"message": "Query not found"}
            return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload

        # Ignore the bot's own responses, else it would go into an infinite loop
        # of answering it's own questions.
        if person_id == me.id:
            payload = {
                "message": "Input query is the bot's previous message, \
                        so don't send it to the bot again"
            }
            return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload

        # #! === User Authentication and Postgres DB Logic === !#
        # #* With IoT OD being decommissioned, platfrom-related code is not enabled (e.g., authentication).

        # user = self.db_operations.fetch_user_by_webex_id(person_id)
        # if not user:
        #     print(f"User with ID {person_id} does not exist in the database.")
        # else:
        #     print(f"User with ID {person_id} exists in the database.")
        #     user_id = user['id']
        #     token = self.db_operations.get_access_token(user_id)
        #     if token is None:  # If token has expired and failed to update
        #         print(f"Failed to retrieve or update access token for user ID {user_id}.")
        #     else:
        #         print(f"Access token for user ID {user_id} is available and valid.")

        # #! === ========================================= === !#
        user = 1

        message = str(txt["text"]).lower() # Text message sent by the user

        # Send either a card for authentication or a message
        self.conv.context = {'user' : user}
        payload = {
            "message": self._post_message(room_id, self.conv.say(message)[0], None)
        }

        return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload

    def _handle_card(self):
        me = self.spark_api.people.me()
        data = request.get_json()

        for key in ["personId", "id", "roomId"]:
            if key not in data["data"].keys():
                payload = {"message": "personId/id/roomID key not found"}
                return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload
            
        if data["id"] != self.card_webhook_id:
            self.logger.debug("Retrieved card_webhook_id %s doesn't match", data["id"])
            payload = {"message": "CARD_WEBHOOK_ID mismatch"}
            return BAD_REQUEST_NAME, BAD_REQUEST_CODE, payload
                
        person_id = data["data"]["personId"]
        msg_id = data["data"]["id"]
        room_id = data["data"]["roomId"]
        card = self._get_card_content(msg_id)

        # Ignore the bot's own responses, else it would go into an infinite loop
        # of answering it's own questions.
        if person_id == me.id:
            payload = {
                "message": "Input query is the bot's previous message, \
                        so don't send it to the bot again"
            }
            return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload

        card_inputs = card["inputs"]
        # Create a new user using the extracted inputs
        new_user_id = self.db_operations.create_user(person_id, card_inputs['1'], card_inputs['2'], card_inputs['3'])
        if new_user_id is not None:
            payload = {
                "message": self._post_message(room_id, "Credentials successfuly submited! You may now interract with me.")
            }
        else:
            payload = {
                "message": self._post_message(room_id, "Oops, something went wrong. Make sure you submit the right credentials.")
            }

        return APPROVED_REQUEST_NAME, APPROVED_REQUEST_CODE, payload
    
    def _post_message(self, room_id, text, card=None):
        headers = {
            "Authorization": self.access_token_with_bearer,
            "content-type": "application/json",
        }

        if card is not None:
            payload = card.copy()
            payload['roomId'] = room_id

        else:
            payload = {"roomId": room_id, "text": text}
        resp = requests.post(url=self._url("/messages"), json=payload, headers=headers)
        response = json.loads(resp.text)
        response["status_code"] = str(resp.status_code)
        # print(response)
        return response

    @staticmethod
    def _url(path):
        return "{0}{1}".format(CISCO_API_URL, path)
    
    def _get_message(self, msg_id):
        """
        Retrieves the message from the Webex Teams service using the message ID.
        """
        headers = {"Authorization": self.access_token_with_bearer}
        resp = requests.get(self._url("/messages/{0}".format(msg_id)), headers=headers)
        response = json.loads(resp.text)
        response["status_code"] = str(resp.status_code)
        # print(response)
        return response
    
    def _get_card_content(self, msg_id):
        """
        Retrieves the message containing a card from the Webex Teams service using the message ID.
        """
        headers = {"Authorization": self.access_token_with_bearer}
        resp = requests.get(self._url("/attachment/actions/{0}".format(msg_id)), headers=headers)
        response = json.loads(resp.text)
        response["status_code"] = str(resp.status_code)
        # print(response)
        return response

    def run(self, host="localhost", port=8080):
        """
        Starts the Flask application on the specified host and port.
        """
        self.app.run(host=host, port=port)
