#!/usr/bin/env python3
"""
Perchance AI to Instagram Bot
Generates images from Perchance AI and posts them to Instagram
"""

import time
import random
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import instagrapi
from PIL import Image
import os
from datetime import datetime

class PerchanceInstagramBot:
    def __init__(self, instagram_username, instagram_password):
        self.instagram_username = instagram_username
        self.instagram_password = instagram_password
        self.driver = None
        self.instagram_client = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories for storing images"""
        self.images_dir = Path("generated_images")
        self.images_dir.mkdir(exist_ok=True)
        
    def setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def setup_instagram(self):
        """Setup Instagram client"""
        try:
            self.instagram_client = instagrapi.Client()
            self.instagram_client.login(self.instagram_username, self.instagram_password)
            print("Successfully logged into Instagram")
        except Exception as e:
            print(f"Failed to login to Instagram: {e}")
            raise
            
    def generate_perchance_image(self):
        """Generate an image from Perchance AI character generator"""
        try:
            print("Navigating to Perchance AI...")
            self.driver.get("https://perchance.org/ai-character-generator")
            
            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait a bit more for dynamic content
            time.sleep(5)
            
            # Look for generate button (common selectors)
            generate_selectors = [
                "button[onclick*='generate']",
                "button:contains('Generate')",
                ".generate-btn",
                "#generate",
                "input[type='button'][value*='Generate']",
                "button.btn",
                ".button"
            ]
            
            generate_button = None
            for selector in generate_selectors:
                try:
                    if "contains" in selector:
                        # Use XPath for text content
                        xpath = f"//button[contains(text(), 'Generate')]"
                        generate_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        generate_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if generate_button:
                        break
                except NoSuchElementException:
                    continue
            
            if not generate_button:
                # Try to find any clickable button
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    generate_button = buttons[0]  # Use first button as fallback
            
            if generate_button:
                print("Clicking generate button...")
                self.driver.execute_script("arguments[0].click();", generate_button)
            else:
                print("No generate button found, trying to trigger generation...")
                # Sometimes generation happens automatically or via other means
                
            # Wait for image to be generated
            print("Waiting for image generation...")
            time.sleep(10)
            
            # Look for generated image
            image_selectors = [
                "img[src*='blob:']",
                "img[src*='data:image']",
                ".generated-image img",
                ".output img",
                ".result img",
                "canvas",
                "img"
            ]
            
            image_element = None
            for selector in image_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if selector == "img":
                            # Check if it's likely a generated image
                            src = element.get_attribute("src")
                            if src and ("blob:" in src or "data:image" in src or "generated" in src.lower()):
                                image_element = element
                                break
                        else:
                            image_element = element
                            break
                    if image_element:
                        break
                except NoSuchElementException:
                    continue
            
            if not image_element:
                # Fallback: take screenshot of the page
                print("No specific image found, taking screenshot...")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = self.images_dir / f"perchance_screenshot_{timestamp}.png"
                self.driver.save_screenshot(str(screenshot_path))
                return screenshot_path
            
            # Download the image
            if image_element.tag_name.lower() == "canvas":
                # Handle canvas element
                canvas_base64 = self.driver.execute_script(
                    "return arguments[0].toDataURL('image/png').substring(21);", 
                    image_element
                )
                import base64
                image_data = base64.b64decode(canvas_base64)
            else:
                # Handle img element
                image_src = image_element.get_attribute("src")
                if image_src.startswith("data:image"):
                    # Data URL
                    import base64
                    image_data = base64.b64decode(image_src.split(",")[1])
                elif image_src.startswith("blob:"):
                    # Blob URL - take screenshot of element
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = self.images_dir / f"perchance_element_{timestamp}.png"
                    image_element.screenshot(str(screenshot_path))
                    return screenshot_path
                else:
                    # Regular URL
                    response = requests.get(image_src)
                    response.raise_for_status()
                    image_data = response.content
            
            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = self.images_dir / f"perchance_generated_{timestamp}.png"
            
            with open(image_path, "wb") as f:
                f.write(image_data)
            
            print(f"Image saved to: {image_path}")
            return image_path
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Fallback: take a screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            fallback_path = self.images_dir / f"perchance_fallback_{timestamp}.png"
            self.driver.save_screenshot(str(fallback_path))
            return fallback_path
    
    def post_to_instagram(self, image_path, caption=""):
        """Post image to Instagram"""
        try:
            if not caption:
                caption = self.generate_caption()
            
            print(f"Posting to Instagram: {image_path}")
            media = self.instagram_client.photo_upload(
                path=str(image_path),
                caption=caption
            )
            print(f"Successfully posted to Instagram! Media ID: {media.pk}")
            return media
            
        except Exception as e:
            print(f"Error posting to Instagram: {e}")
            raise
    
    def generate_caption(self):
        """Generate a random caption for the post"""
        captions = [
            "🎨 AI-generated character art! #AIart #DigitalArt #CharacterDesign",
            "✨ Fresh from the AI generator! #AIgenerated #ArtificialIntelligence #CreativeAI",
            "🤖 When AI meets creativity! #AIart #GeneratedArt #TechArt",
            "🎭 Character of the day! #CharacterArt #AIcreated #DigitalCreativity",
            "🌟 AI imagination at work! #AIartist #GenerativeArt #FutureArt"
        ]
        return random.choice(captions)
    
    def run_once(self):
        """Generate one image and post to Instagram"""
        try:
            print("Starting Perchance to Instagram bot...")
            
            # Setup
            self.setup_selenium()
            self.setup_instagram()
            
            # Generate image
            image_path = self.generate_perchance_image()
            
            if image_path and image_path.exists():
                # Post to Instagram
                self.post_to_instagram(image_path)
                print("✅ Successfully completed one cycle!")
            else:
                print("❌ Failed to generate image")
                
        except Exception as e:
            print(f"Error in run cycle: {e}")
        finally:
            if self.driver:
                self.driver.quit()
    
    def run_continuous(self, interval_hours=6, max_posts=None):
        """Run the bot continuously"""
        posts_made = 0
        
        while True:
            try:
                if max_posts and posts_made >= max_posts:
                    print(f"Reached maximum posts limit ({max_posts})")
                    break
                
                self.run_once()
                posts_made += 1
                
                if max_posts and posts_made >= max_posts:
                    break
                
                # Wait before next post
                wait_seconds = interval_hours * 3600
                print(f"Waiting {interval_hours} hours before next post...")
                time.sleep(wait_seconds)
                
            except KeyboardInterrupt:
                print("Bot stopped by user")
                break
            except Exception as e:
                print(f"Error in continuous run: {e}")
                print("Waiting 30 minutes before retry...")
                time.sleep(1800)  # Wait 30 minutes on error

def main():
    """Main function to run the bot"""
    print("Perchance AI to Instagram Bot")
    print("=============================")
    
    # Configuration
    INSTAGRAM_USERNAME = input("Enter your Instagram username: ").strip()
    INSTAGRAM_PASSWORD = input("Enter your Instagram password: ").strip()
    
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        print("Username and password are required!")
        return
    
    # Create bot instance
    bot = PerchanceInstagramBot(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    
    # Choose mode
    print("\nChoose mode:")
    print("1. Generate and post once")
    print("2. Run continuously")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        bot.run_once()
    elif choice == "2":
        interval = input("Enter interval between posts in hours (default: 6): ").strip()
        interval = int(interval) if interval.isdigit() else 6
        
        max_posts = input("Enter maximum number of posts (leave empty for unlimited): ").strip()
        max_posts = int(max_posts) if max_posts.isdigit() else None
        
        bot.run_continuous(interval_hours=interval, max_posts=max_posts)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()