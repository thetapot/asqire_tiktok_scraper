# scraper.py
import csv
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def scrape_creators_on_page(driver):
    """
    This function scrapes all the creator details (username and profile link) on the current page.
    It returns a list of lists containing [username, link].
    """
    # List to store creator details
    creators_data = []

    try:
        # Find all the creator elements on the current page
        creators = driver.find_elements(By.CLASS_NAME, "_name_1s2z4_344")

        for creator in creators:
            try:
                # Extract the username from the inner div element
                username = creator.find_element(By.TAG_NAME, "div").text

                # Construct the profile link
                profile_link = f"http://www.instagram.com/{username}"

                # Append the username and profile link to the list
                creators_data.append([username, profile_link])

                print(f"Scraped: {username}, {profile_link}")

            except Exception as e:
                print(f"Error scraping a creator: {e}")
                continue

    except Exception as e:
        print(f"Error while scraping creators: {e}")

    return creators_data

def navigate_to_next_page(driver):
    """
    This function clicks the next page (>) button to navigate to the next set of pages.
    It returns True if successful, False if no more pages are available.
    """
    try:
        next_page_button = driver.find_element(By.CLASS_NAME, "_rightArrow_10g2g_228")
        next_page_button.click()
        time.sleep(5)  # Wait for 5 seconds to allow the page to load
        return True
    except Exception as e:
        print("No more pages available or error navigating to the next page:", e)
        return False

def select_first_page_of_new_group(driver, page_num):
    """
    This function selects the first page of the new group after clicking the right arrow (e.g., page 11).
    """
    try:
        next_page_button = driver.find_element(By.XPATH, f"//div[@class='_item_10g2g_204'][text()='{page_num}']")
        next_page_button.click()
        time.sleep(5)  # Wait for 5 seconds to allow the page to load
        print(f"Successfully navigated to page {page_num}")
    except Exception as e:
        print(f"Error selecting the first page of the new group: {e}")

def scrape_all_pages(driver, min_follower, max_follower, max_pages=500):
    """
    This function scrapes all the creators' details across multiple pages up to max_pages.
    It saves the scraped data into a CSV file with the format:
    creators_<min_follower>_to_<max_follower>_<scrape_date>.csv
    """
    # Generate the current date in the format YYYY_MM_DD
    scrape_date = datetime.now().strftime("%Y_%m_%d")

    # Create the CSV filename in snake case: creators_<min_follower>_to_<max_follower>_<scrape_date>.csv
    output_csv = f"creators_{min_follower}_to_{max_follower}_{scrape_date}.csv"

    # Initialize an empty list to store all the creators' data
    all_creators_data = []

    current_page = 1
    pages_scraped_in_group = 0

    while current_page <= max_pages:
        print(f"Scraping page {current_page}...")

        # Scrape the current page
        creators_data = scrape_creators_on_page(driver)
        all_creators_data.extend(creators_data)

        # Check if we have reached the 10th page in the current group (1-10, 11-20, ...)
        if pages_scraped_in_group == 9:
            # Click the right arrow to load the next set of pages (after 10, go to 11-20)
            if not navigate_to_next_page(driver):
                print(f"No more pages available. Stopping at page {current_page}.")
                break

            # Select the first page of the new group (e.g., page 11 or page 21)
            select_first_page_of_new_group(driver, current_page + 1)

            pages_scraped_in_group = 0  # Reset the group counter
        else:
            # Click the next page number (e.g., 2, 3, ..., 10)
            try:
                next_page_button = driver.find_element(By.XPATH, f"//div[@class='_item_10g2g_204'][text()='{current_page + 1}']")
                next_page_button.click()
                time.sleep(5)  # Wait for 5 seconds to allow the page to load
                pages_scraped_in_group += 1
            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                break

        current_page += 1

    # Write all scraped data to a CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "link"])  # Write CSV header
        writer.writerows(all_creators_data)  # Write all creator data

    print(f"Scraped {len(all_creators_data)} creators and saved to {output_csv}")