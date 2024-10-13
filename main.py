# main.py
from browser_manager import open_and_wait_for_user_close, open_chrome_with_profile
from filters import select_reach_and_engagement_filter
from scraper import scrape_all_pages  # Import the function to scrape all pages
import time

def main():
    # Step 1: Open the browser and wait for the user to close it after login.
    open_and_wait_for_user_close()

    # Define filter parameters
    min_follower = 6000
    max_follower = 80000
    min_views = 500
    max_views = 50000
    age_options = {
        "13-17": True,
        "18-24": True,
        "25-34": True,
        "35-44": True,
        "45-64": True,
        "65+": True
    }
    gender_choice = "male"
    locations = ["United States", "United Kingdom"]
    languages = ["English", "Spanish"]
    keyword = "fashion"  # Set the keyword for search
    channel_index = 1  # Index for selecting the TikTok channel

    # Step 2: Open browser to the filter page
    driver = open_chrome_with_profile()
    driver.get("https://community.aspireiq.com/client/Fo9cITmb9lG60RzwcppmtMEG7RCCYcKI/app/KyXOg4RiEupXxAFkWh3qnud6nX3tIWb4")
    time.sleep(8)  # Pause to allow page loading

    # Step 3: Apply filters
    print(f"Applying filters: Followers between {min_follower} and {max_follower}, views per video between {min_views} and {max_views}, "
          f"age groups, gender ({gender_choice.title()}), locations ({locations}), and languages ({languages}).")
    select_reach_and_engagement_filter(driver, min_follower, max_follower, min_views, max_views, age_options,
                                       gender_choice, locations, languages, keyword, channel_index)

    # Step 4: Scrape all pages and save to CSV with a dynamic filename
    print("Starting to scrape creators across all pages...")
    scrape_all_pages(driver, min_follower=min_follower, max_follower=max_follower, max_pages=500)

    # Step 5: Close the browser
    driver.quit()

if __name__ == "__main__":
    main()