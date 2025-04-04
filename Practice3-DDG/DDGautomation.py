from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

def chat_with_duckduckgo(prompt):
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open DuckDuckGo AI Chat page
        driver.get("https://duckduckgo.com/aichat")
        time.sleep(3)  # Allow time for the page to load
        
        # Click the "Give It a Try" button
        try:
            button = driver.find_element(By.TAG_NAME, "button")
            ActionChains(driver).move_to_element(button).click().perform()
            time.sleep(3)  # Wait for transition
        except Exception as e:
            print("Button click failed:", e)
        
        # Click the "I Agree" button (Privacy Policy)
        try:
            agree_button = driver.find_element(By.XPATH, "//button[contains(text(),'I Agree')]")
            ActionChains(driver).move_to_element(agree_button).click().perform()
            time.sleep(3)  # Allow time for transition
        except Exception as e:
            print("Privacy policy acceptance failed:", e)

        # Find the input field and enter the prompt
        input_box = driver.find_element(By.TAG_NAME, "textarea")
        input_box.send_keys(prompt)
        input_box.send_keys(Keys.RETURN)
        
        # Wait for the response to load properly
        time.sleep(7)  # Increased delay to ensure response is fully generated
        
        # Retrieve the response
        responses = driver.find_elements(By.XPATH, "//div[contains(@class, 'chat-bubble')]//li")
        if responses:
            ai_response = "\n".join([r.text for r in responses])  # Get all list items
        else:
            ai_response = "No response received."
        
        return ai_response
    
    finally:
        driver.quit()

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    response = chat_with_duckduckgo(user_prompt)
    print("DuckDuckGo AI Response:\n", response)
