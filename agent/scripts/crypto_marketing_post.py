#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import requests
import json
import sys
import random
from datetime import datetime
from requests_oauthlib import OAuth1

# Load environment variables
load_dotenv()

def get_trending_coins():
    """
    Fetch trending cryptocurrencies from CoinGecko API
    
    Returns:
        dict: JSON response with trending coins data
    """
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        headers = {}
        
        # Add API key if available
        api_key = os.getenv("COINGECKO_API_KEY")
        if api_key:
            headers["x-cg-pro-api-key"] = api_key
            
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching trending coins: {response.status_code}")
            print(f"Response: {response.text}")
            return {"coins": []}
        
        return response.json()
    except Exception as e:
        print(f"Error in get_trending_coins: {e}")
        return {"coins": []}

def get_coin_price(coin_id):
    """
    Get current price of a cryptocurrency
    
    Args:
        coin_id (str): CoinGecko coin ID
        
    Returns:
        float: Current price in USD, or None if error
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        headers = {}
        
        # Add API key if available
        api_key = os.getenv("COINGECKO_API_KEY")
        if api_key:
            headers["x-cg-pro-api-key"] = api_key
            
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching coin price: {response.status_code}")
            return None
        
        data = response.json()
        return data.get(coin_id, {}).get("usd")
    except Exception as e:
        print(f"Error in get_coin_price: {e}")
        return None

def generate_tweet_content(trending_data):
    """
    Generate engaging tweet content based on trending cryptocurrency data
    
    Args:
        trending_data (dict): Trending cryptocurrency data
        
    Returns:
        str: Tweet content
    """
    if not trending_data or not trending_data.get("coins"):
        return f"Exploring the crypto markets today! What coins are you watching? #Crypto #Bitcoin #Trading #{datetime.now().strftime('%A')}"
    
    # Get top 3 trending coins
    top_coins = trending_data.get("coins", [])[:3]
    
    # Different tweet formats
    tweet_formats = [
        "🔥 Today's trending #crypto coins: {coins_list}. Which one are you most bullish on? #CryptoTrading #Investing",
        "📊 Market watch: {coins_list} are trending today! What's your price prediction? #Cryptocurrency #Trading",
        "👀 Keep an eye on these trending coins: {coins_list}. Interesting market movements today! #Crypto #Trading",
        "🚀 Trending on CoinGecko: {coins_list}. Are you adding any to your portfolio? #CryptoInvesting #Markets",
        "💹 Market intelligence: {coins_list} showing strong momentum today. Thoughts? #CryptoAnalysis #Trading"
    ]
    
    # Format coin names and symbols
    coins_text = []
    for coin in top_coins:
        item = coin.get("item", {})
        name = item.get("name", "")
        symbol = item.get("symbol", "").upper()
        price = get_coin_price(item.get("id", ""))
        
        if price:
            coins_text.append(f"#{symbol} (${price:.2f})")
        else:
            coins_text.append(f"#{symbol}")
    
    coins_list = ", ".join(coins_text)
    
    # Select random tweet format
    tweet_format = random.choice(tweet_formats)
    
    # Generate tweet
    tweet = tweet_format.format(coins_list=coins_list)
    
    # Add timestamp hashtag to make each tweet unique
    timestamp = datetime.now().strftime("%H%M")
    tweet += f" #CryptoUpdate{timestamp}"
    
    return tweet

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
    # Get trending cryptocurrency data
    trending_data = get_trending_coins()
    
    # Generate tweet content
    tweet_content = generate_tweet_content(trending_data)
    print(f"Generated tweet: {tweet_content}")
    
    # Post to X
    success = post_to_x(tweet_content)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 