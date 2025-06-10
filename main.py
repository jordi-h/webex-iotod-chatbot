# -*- coding: utf-8 -*-

"""This script initializes and runs a Webex bot server using Flask and MindMeld."""

import os
import argparse
from dotenv import load_dotenv
from flask import Flask
from mindmeld.components import NaturalLanguageProcessor
from mindmeld import configure_logs
from webex_bot_server_extended import WebexBotServerExtended
from utils.environment_loader import load_env

def create_app():
    """Function to create Flask app and configure the MindMeld components."""

    app = Flask(__name__)
    configure_app(app)
    configure_logs()

    nlp = NaturalLanguageProcessor(app_path='.')
    try:
        # Load the pre-trained models. nlp.build() and nlp.dump() have to be run prior the following command.
        nlp.load() 
    except Exception as e:
        app.logger.error(f"Failed to build NLP components: {e}")

    # Initialize the server with necessary parameters
    server = create_webex_bot_server(app, nlp)

    return server

def configure_app(app):
    """Configure app environment variables."""

    app.config['MESSAGE_WEBHOOK_ID'] = os.environ.get('MESSAGE_WEBHOOK_ID')
    app.config['CARD_WEBHOOK_ID'] = os.environ.get('CARD_WEBHOOK_ID')
    app.config['ACCESS_TOKEN'] = os.environ.get('BOT_ACCESS_TOKEN')

def create_webex_bot_server(app, nlp):
    """Function to create and configure the WebexBotServer."""

    db_config = {
        'dbname': os.environ.get('DB_NAME', 'postgres'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'iotod'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', 5432)),
    }

    server = WebexBotServerExtended(
        name='webex_bot',
        app_path='.',
        nlp=nlp,
        message_webhook_id=app.config['MESSAGE_WEBHOOK_ID'],
        card_webhook_id=app.config['CARD_WEBHOOK_ID'],
        access_token=app.config['ACCESS_TOKEN'],
        db_config=db_config
         
    )
    return server

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start the Webex Bot Server.")
    parser.add_argument("--env", type=str, default='prod', help="Set the environment to 'prod' or 'dev'")
    
    args = parser.parse_args()
    
    # Override environment based on command-line argument
    if args.env:
        os.environ['ENVIRONMENT'] = args.env
        
    # Load environment variables
    load_env()
        
    print(f"Current working directory: {os.getcwd()}")

    server = create_app()
    port_number = 8080
    server.app.logger.info(f'Running server on port {port_number}...')
    server.run(host='0.0.0.0', port=port_number)
