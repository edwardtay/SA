#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import requests
import sys
import json
from datetime import datetime
from requests_oauthlib import OAuth1

# Load environment variables
load_dotenv()

def post_to_x(message):
    """
    Post a message to X (Twitter) using direct API calls with OAuth1 authentication.
    
    Args:
        message (str): The message to post
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get X API credentials from environment variables
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_KEY_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        # Check if credentials are available
        if not all([api_key, api_secret, access_token, access_token_secret]):
            print("Error: X API credentials not found in environment variables.")
            return False
        
        # X API v2 endpoint for posting tweets
        url = "https://api.twitter.com/2/tweets"
        
        # Set up OAuth1 authentication
        auth = OAuth1(
            api_key,
            client_secret=api_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )
        
        # Prepare the request payload
        payload = {
            "text": message
        }
        
        # Make the POST request with OAuth1 authentication
        response = requests.post(
            url,
            auth=auth,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        # Check if successful
        if response.status_code in [200, 201]:
            data = response.json()
            tweet_id = data.get('data', {}).get('id')
            print(f"Successfully posted tweet with ID: {tweet_id}")
            return True
        else:
            print(f"Error: Failed to post tweet. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

def main():
    # Default message if none provided
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    default_message = f"Testing my crypto marketing bot at {current_time}. #Crypto #Bitcoin #Trading #SuperiorAgents"
    
    # Get message from command line argument or use default
    message = sys.argv[1] if len(sys.argv) > 1 else default_message
    
    # Post to X
    success = post_to_x(message)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 