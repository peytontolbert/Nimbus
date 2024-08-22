import requests
import logging
from datetime import datetime, timedelta
import time
import json

class socialmediaautomation:
    def __init__(self):
        self.platform_credentials = {}
        self.logger = logging.getLogger("SocialMediaAutomation")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("social_media_automation.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.scheduled_posts = []

    def authenticate(self, platform: str, credentials: dict) -> dict:
        """Authenticate with the social media platform."""
        # This example assumes each platform requires a different method of authentication.
        self.platform_credentials[platform] = credentials
        self.logger.info(f"Authenticated with {platform}")
        return {"status": "success", "message": f"Authenticated with {platform}"}

    def schedule_post(self, platform: str, content: str, schedule_time: datetime) -> dict:
        """Schedule a post to be published at a specific time."""
        if platform not in self.platform_credentials:
            return {"error": f"Platform '{platform}' not authenticated. Please authenticate first."}
        
        post_details = {
            "platform": platform,
            "content": content,
            "schedule_time": schedule_time
        }
        self.scheduled_posts.append(post_details)
        self.logger.info(f"Scheduled post for {platform} at {schedule_time}")
        return {"status": "success", "message": f"Post scheduled for {platform} at {schedule_time}"}

    def publish_post(self, platform: str, content: str) -> dict:
        """Publish the content on the specified platform."""
        if platform not in self.platform_credentials:
            return {"error": f"Platform '{platform}' not authenticated. Please authenticate first."}

        # Example base URLs for different social media platforms
        platform_endpoints = {
            "twitter": "https://api.twitter.com/2/tweets",
            "facebook": "https://graph.facebook.com/me/feed",
            # Add more platforms as needed
        }

        if platform not in platform_endpoints:
            return {"error": f"Platform '{platform}' not supported."}

        url = platform_endpoints[platform]
        headers = {"Authorization": f"Bearer {self.platform_credentials[platform]['access_token']}"}

        data = {"content": content}

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            self.logger.info(f"Successfully posted to {platform}")
            return {"status": "success", "message": f"Successfully posted to {platform}"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while posting to {platform}: {e}")
            return {"error": str(e)}

    def check_scheduled_posts(self):
        """Check if any scheduled posts need to be published."""
        current_time = datetime.now()
        posts_to_remove = []

        for post in self.scheduled_posts:
            if post["schedule_time"] <= current_time:
                self.publish_post(post["platform"], post["content"])
                posts_to_remove.append(post)
        
        # Remove published posts from the schedule
        for post in posts_to_remove:
            self.scheduled_posts.remove(post)

    def run_scheduler(self, check_interval: int = 60):
        """Continuously check and publish scheduled posts at regular intervals."""
        while True:
            self.check_scheduled_posts()
            time.sleep(check_interval)

    def log_post_activity(self, platform: str, action: str, details: dict):
        """Log post-related activities for auditing."""
        log_entry = {
            "platform": platform,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"Post Activity Logged: {json.dumps(log_entry)}")
