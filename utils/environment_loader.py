"""This module loads environment variables based on the specified environment ('dev' or 'prod')."""

import os
from dotenv import load_dotenv

def load_env():
    """Load environment variables from the common file and the environment-specific file."""
    # Load common environment variables
    load_dotenv('.env.common', verbose=True, override=True)
    
    environment = os.environ.get('ENVIRONMENT', 'prod')  # Default to 'prod' if ENVIRONMENT is not set
    if environment == 'dev':
        load_dotenv('.env.dev', verbose=True, override=True)
    else:
        load_dotenv('.env.prod', verbose=True, override=True)