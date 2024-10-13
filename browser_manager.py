from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import platform
import time

def get_chrome_profile_path(profile_name="Profile 1"):
    """
    Detects the user's operating system and constructs the path to the Chrome profile directory.
    Default is "Profile 1", but this can be changed if the user has a different profile.
    """
    home_dir = os.path.expanduser("~")  # Get the user's home directory

    if platform.system() == "Darwin":  # macOS
        profile_path = os.path.join(home_dir, "Library", "Application Support", "Google", "Chrome", profile_name)
    elif platform.system() == "Linux":  # Linux
        profile_path = os.path.join(home_dir, ".config", "google-chrome", profile_name)
    elif platform.system() == "Windows":  # Windows
        profile_path = os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data", profile_name)
    else:
        raise Exception(f"Unsupported OS: {platform.system()}")

    return profile_path

def open_chrome_with_profile(profile_name="Profile 1"):
    """
    Opens Chrome with the specified user profile.
    By default, it uses 'Profile 1', but you can specify a different profile name if needed.
    """
    chrome_options = Options()

    # Get the Chrome profile path based on the operating system
    profile_path = get_chrome_profile_path(profile_name)
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument(f"--profile-directory={profile_name}")

    # Set up the Chrome WebDriver using the WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def open_and_wait_for_user_close(profile_name="Profile 1"):
    """
    Opens Chrome, waits for the user to log in and close the window before proceeding.
    """
    driver = open_chrome_with_profile(profile_name)

    # Open the target URL or login page if needed (you can adjust this part as necessary)
    url = "https://community.aspireiq.com/client/Fo9cITmb9lG60RzwcppmtMEG7RCCYcKI/app/KyXOg4RiEupXxAFkWh3qnud6nX3tIWb4"
    driver.get(url)

    # Wait for the user to close the browser manually
    try:
        while len(driver.window_handles) > 0:
            time.sleep(1)  # Sleep for 1 second before checking again
    except Exception as e:
        print(f"Error while waiting for the browser to close: {e}")
    finally:
        driver.quit()
        print("Browser closed by user. Continuing with the script.")