"""This module contains the logic for the User Database."""

import psycopg2
from datetime import datetime, timedelta

from components.iotod_api import get_access_token, ACCESS_TOKEN_EXPIRATION_TIME

class UserDBOperations:
    def __init__(self, db_config):
        self.conn = self.connect_db(db_config)

    def connect_db(self, db_config):
        try:
            conn = psycopg2.connect(**db_config)
            print("User Database connection established")
            self.ensure_tables_exist(conn)
            return conn
        except Exception as e:
            print(f"User Database connection failed: {e}")
            return None

    def ensure_tables_exist(self, conn):
        with conn.cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    webex_person_id VARCHAR(255) UNIQUE NOT NULL
                );
            """)

            # Create user_api_details table for storing api_key_id, organization_id, api_key triplets and the access_token
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_api_details (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    api_key_id VARCHAR(255) NOT NULL,
                    organization_id VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) NOT NULL,
                    access_token TEXT,
                    token_set_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            conn.commit()

    def create_user(self, webex_person_id, api_key_id, organization_id, api_key):
        with self.conn.cursor() as cur:
            try:
                # Check if the user already exists
                cur.execute("SELECT id FROM users WHERE webex_person_id = %s;", (webex_person_id,))
                existing_user = cur.fetchone()

                if existing_user:
                    user_id = existing_user[0]
                    print(f"User with webex_person_id {webex_person_id} already exists with ID {user_id}.")
                    return None

                # Attempt to fetch the access token before inserting the user
                access_token = get_access_token(api_key_id, api_key)

                if not access_token:
                    print(f"Failed to fetch access token for webex_person_id {webex_person_id}.")
                    return None

                # Proceed with user creation since we have an access token.
                cur.execute("INSERT INTO users (webex_person_id) VALUES (%s) RETURNING id;", (webex_person_id,))
                user_id = cur.fetchone()[0]
                
                # Insert into user_api_details table
                cur.execute("""
                    INSERT INTO user_api_details (user_id, api_key_id, organization_id, api_key, access_token) 
                    VALUES (%s, %s, %s, %s, %s);
                """, (user_id, api_key_id, organization_id, api_key, access_token))
                self.conn.commit()
                print(f"User created with ID {user_id}.")
                return user_id

            except Exception as e:
                print(f"An error occurred during user creation: {e}")
                self.conn.rollback()
                return None

    def fetch_all_users(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT u.id, u.webex_person_id, a.api_key_id, a.organization_id, a.api_key, a.access_token, a.token_set_timestamp
                FROM users u
                LEFT JOIN user_api_details a ON u.id = a.user_id;
            """)
            users = cur.fetchall()
            return [{
                "id": user[0], 
                "webex_person_id": user[1], 
                "api_key_id": user[2], 
                "organization_id": user[3], 
                "api_key": user[4],
                "access_token": user[5],
                "token_set_timestamp": user[6]
            } for user in users]

    def fetch_user_by_webex_id(self, webex_person_id):
        with self.conn.cursor() as cur:
            # Query to fetch user information based on webex_person_id
            cur.execute("""
                SELECT * FROM users WHERE webex_person_id = %s;
            """, (webex_person_id,))
            user = cur.fetchone()

            if user:
                user_id = user[0]  # Extract the user ID from the first query result

                # Query to fetch API details associated with the user
                cur.execute("""
                    SELECT api_key_id, organization_id, api_key, access_token, token_set_timestamp
                    FROM user_api_details 
                    WHERE user_id = %s;
                """, (user_id,))
                api_details = cur.fetchall()

                return {
                    "id": user[0],
                    "webex_person_id": user[1],
                    "api_details": [
                        {
                            "api_key_id": detail[0], 
                            "organization_id": detail[1], 
                            "api_key": detail[2],
                            "access_token": detail[3], 
                            "token_set_timestamp": detail[4]
                        } 
                        for detail in api_details
                    ]
                }
        return None

    def delete_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.conn.commit()
            print(f"User with ID {user_id} has been deleted.")

    def delete_all_users(self):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users;")
            self.conn.commit()
            print("All users have been deleted.")

    def is_token_expired(self, user_id):
        """Checks if the access token for a given user has expired."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT token_set_timestamp FROM user_api_details WHERE user_id = %s;
            """, (user_id,))
            result = cur.fetchone()
            if result:
                token_set_time = result[0]
                current_time = datetime.now(tz=token_set_time.tzinfo)
                # Check if more than (ACCESS_TOKEN_EXPIRATION_TIME - 60) seconds have passed since the token was set
                if current_time - token_set_time > timedelta(seconds=ACCESS_TOKEN_EXPIRATION_TIME-60):
                    return True  # Token is expired
            return False  # Token is not expired

    def get_access_token(self, user_id):
        """
        Retrieves the access token for a given user. If the token has expired, attempts to update it.
        Returns None if the token is expired and cannot be updated, or if the user cannot be found.
        """

        if self.is_token_expired(user_id):
            print(f"Access token for user_id {user_id} is expired. Updating...")
            update_success = self.update_access_key(user_id)
            if not update_success:
                print(f"Failed to update access token for user_id {user_id}.")
                return None

        with self.conn.cursor() as cur:
            cur.execute("SELECT access_token FROM user_api_details WHERE user_id = %s;", (user_id,))
            result = cur.fetchone()

            if result:
                return result[0]  # Return the access token.
            else:
                print(f"User not found for user_id {user_id}.")
                return None
                
    def update_access_key(self, user_id):
        """
        Attempts to update the access token for the specified user by fetching a new access token
        using the user's API key details and updating the database with the new token.
        """
        
        try:
            with self.conn.cursor() as cur:
                # Attempt to fetch API key details for the given user_id
                cur.execute("""
                    SELECT api_key_id, api_key FROM user_api_details WHERE user_id = %s;
                """, (user_id,))
                result = cur.fetchone()

                if not result:
                    print(f"No API details found for user_id {user_id}.")
                    return False

                api_key_id, api_key = result
                new_access_token = get_access_token(api_key_id, api_key)

                if not new_access_token:
                    print("Failed to fetch a new access token.")
                    return False

                # Update the access token in the database
                cur.execute("""
                    UPDATE user_api_details
                    SET access_token = %s, token_set_timestamp = CURRENT_TIMESTAMP
                    WHERE user_id = %s;
                """, (new_access_token, user_id))
                self.conn.commit()
                print(f"Access token updated for user_id {user_id}.")
                return True

        except Exception as e:
            print(f"Exception occurred while updating access token for user_id {user_id}: {e}")
            self.conn.rollback()
            return False
