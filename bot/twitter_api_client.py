"""
TwitterAPI.io client for fetching tweets and posting replies.
Wrapper around TwitterAPI.io REST endpoints.
"""

import logging
import re
from typing import Optional

import requests

from config.settings import settings

logger = logging.getLogger(__name__)


class TwitterAPIClient:
    """Client for interacting with TwitterAPI.io."""

    def __init__(self):
        """Initialize TwitterAPI.io client with authentication."""
        self.base_url = settings.TWITTER_API_BASE_URL
        self.api_key = settings.TWITTER_API_KEY
        self.bearer_token = settings.TWITTER_API_BEARER_TOKEN
        
        # Use bearer token if available, otherwise use API key
        auth_token = self.bearer_token or self.api_key
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        self.timeout = settings.REQUEST_TIMEOUT

    @staticmethod
    def extract_tweet_id(url: str) -> Optional[str]:
        """
        Extract tweet ID from Twitter/X URL.

        Args:
            url: Twitter/X URL (e.g., https://twitter.com/user/status/1234567890)

        Returns:
            Tweet ID if found, None otherwise
        """
        # Pattern for standard tweet URLs
        patterns = [
            r"(?:twitter|x)\.com/\w+/status/(\d+)",  # Standard URL
            r"t\.co/\w+",  # Shortened URL (would need to follow redirect)
            r"^(\d+)$",  # Direct ID
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def get_tweet(self, tweet_id: str) -> Optional[dict]:
        """
        Fetch tweet details by ID using TwitterAPI.io.

        Args:
            tweet_id: Twitter tweet ID

        Returns:
            Tweet data dictionary or None if failed
        """
        try:
            # TwitterAPI.io endpoint for getting tweet details
            url = f"{self.base_url}/tweets/{tweet_id}"
            
            params = {
                "expansions": "author_id",
                "tweet.fields": "created_at,public_metrics,conversation_id",
                "user.fields": "username,name"
            }

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            
            # TwitterAPI.io returns data in 'data' field
            if data.get("data"):
                tweet_data = data["data"]
                # Extract text from the tweet
                text = tweet_data.get("text", "")
                
                if text:
                    logger.info(f"Successfully fetched tweet {tweet_id}")
                    return {
                        "tweet_id": tweet_id,
                        "text": text,
                        "full_text": text,
                        "created_at": tweet_data.get("created_at"),
                    }
            
            logger.warning(f"Failed to fetch tweet {tweet_id}: No text found")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tweet {tweet_id}: {str(e)}")
            return None

    def post_reply(
        self, tweet_id: str, reply_text: str, media_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Post a reply to a tweet using TwitterAPI.io.

        Args:
            tweet_id: ID of tweet to reply to
            reply_text: Text content of the reply
            media_url: Optional URL of image to attach

        Returns:
            Posted tweet ID if successful, None otherwise
        """
        try:
            # TwitterAPI.io endpoint for creating tweets
            url = f"{self.base_url}/tweets"
            
            payload = {
                "text": reply_text,
                "reply": {
                    "in_reply_to_tweet_id": tweet_id
                }
            }

            # Add media if provided
            if media_url:
                payload["media"] = {
                    "media_ids": [media_url]
                }

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            
            # TwitterAPI.io returns the created tweet data
            if data.get("data"):
                posted_id = data["data"].get("id")
                if posted_id:
                    logger.info(f"Successfully posted reply: {posted_id}")
                    return posted_id

            logger.warning(f"Failed to post reply: {data.get('errors', 'Unknown error')}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting reply: {str(e)}")
            return None

    def post_tweet(
        self, tweet_text: str, media_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Post a standalone tweet using TwitterAPI.io.

        Args:
            tweet_text: Text content of the tweet
            media_url: Optional URL of image to attach

        Returns:
            Posted tweet ID if successful, None otherwise
        """
        try:
            # TwitterAPI.io endpoint for creating tweets
            url = f"{self.base_url}/tweets"
            
            payload = {
                "text": tweet_text
            }

            # Add media if provided
            if media_url:
                payload["media"] = {
                    "media_ids": [media_url]
                }

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            
            # TwitterAPI.io returns the created tweet data
            if data.get("data"):
                posted_id = data["data"].get("id")
                if posted_id:
                    logger.info(f"Successfully posted tweet: {posted_id}")
                    return posted_id

            logger.warning(f"Failed to post tweet: {data.get('errors', 'Unknown error')}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting tweet: {str(e)}")
            return None

    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Try a simple request to validate the key
            # Using a public tweet ID for validation
            url = f"{self.base_url}/tweets/1"
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
            )
            
            # Accept 200 (success) or 404 (tweet not found but auth works)
            return response.status_code in [200, 404]

        except requests.exceptions.RequestException as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False
