# filters.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def select_channel_by_occurrence(driver, channel_index=1):
    """
    Selects a channel button by its occurrence index.
    For example, if TikTok is the second channel, set channel_index=1.
    """
    try:
        channel_buttons = driver.find_elements(By.CLASS_NAME, "_networkIcon_5wxyi_4")
        if channel_index < len(channel_buttons):
            channel_buttons[channel_index].click()
            print(f"Selected channel at index {channel_index}.")
            time.sleep(1)
        else:
            print(f"No channel found at index {channel_index}. Check the specified index.")
    except Exception as e:
        print(f"Error selecting channel at index {channel_index}: {e}")


def input_keyword(driver, keyword):
    """
    This function inputs a keyword into the search bar.
    It will delete any existing text and enter the specified keyword.
    """
    try:
        keyword_input = driver.find_elements(By.CLASS_NAME, "_input_c76r6_251")[0]
        keyword_input.click()
        keyword_input.clear()
        keyword_input.send_keys(keyword)
        keyword_input.send_keys(Keys.ENTER)
        print(f"Keyword set to: {keyword}")
    except Exception as e:
        print(f"Error setting keyword: {e}")


def select_gender(driver, gender_choice):
    """
    Selects the gender radio button based on user input: "All", "Male", or "Female".
    """
    gender_choice = gender_choice.title()
    gender_radio_buttons = {
        "All": "//div[@class='_dot_1ef8j_46'][following-sibling::div[contains(text(), 'All')]]",
        "Male": "//div[@class='_dot_1ef8j_46'][following-sibling::div[contains(text(), 'Male')]]",
        "Female": "//div[@class='_dot_1ef8j_46'][following-sibling::div[contains(text(), 'Female')]]"
    }
    try:
        gender_button = driver.find_element(By.XPATH, gender_radio_buttons[gender_choice])
        gender_button.click()
        print(f"Selected gender: {gender_choice}")
    except Exception as e:
        print(f"Error selecting gender {gender_choice}: {e}")


def select_creator_demographics(driver, age_options, gender_choice):
    """
    Clicks 'Creator Demographics' and selects age checkboxes and gender radio button
    based on user input, adjusting for checkbox index offset.
    """
    try:
        demographics_button = driver.find_element(By.XPATH, "//span[contains(text(),'Creator Demographics')]")
        demographics_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking 'Creator Demographics': {e}")
        return

    checkboxes = driver.find_elements(By.CLASS_NAME, "_Checkbox_1v8tf_169")
    age_groups = ["13-17", "18-24", "25-34", "35-44", "45-64", "65+"]

    # Adjusted offset: reduce by 2 to correct checkbox occurrence
    for i, age in enumerate(age_groups):
        try:
            if age_options[age]:
                checkbox = checkboxes[i].find_element(By.CLASS_NAME, "_box_1v8tf_169")
                checkbox.click()
                print(f"Checked age group: {age}")
            else:
                print(f"Skipped age group: {age}")
        except Exception as e:
            print(f"Error checking age group {age}: {e}")

    # Select the gender radio button
    select_gender(driver, gender_choice)


def input_location_and_language(driver, locations, languages):
    """
    Inputs locations and languages into respective fields.
    After typing each value, it pauses and selects the first suggestion.
    """
    try:
        location_input = driver.find_elements(By.CLASS_NAME, "_input_vi7i2_245")[0]
        for location in locations:
            location_input.click()
            location_input.clear()
            location_input.send_keys(location)
            time.sleep(3)

            # Select the first suggestion
            first_suggestion = driver.find_element(By.CLASS_NAME, "_option_vi7i2_320")
            first_suggestion.click()
            print(f"Location set to: {location}")
            time.sleep(3)
    except Exception as e:
        print(f"Error setting location: {e}")

    try:
        language_input = driver.find_elements(By.CLASS_NAME, "_input_vi7i2_245")[1]
        for language in languages:
            language_input.click()
            language_input.clear()
            language_input.send_keys(language)
            time.sleep(1)

            # Select the first suggestion
            first_suggestion = driver.find_element(By.CLASS_NAME, "_option_vi7i2_320")
            first_suggestion.click()
            print(f"Language set to: {language}")
            time.sleep(1)
    except Exception as e:
        print(f"Error setting language: {e}")


def select_reach_and_engagement_filter(driver, min_follower, max_follower, min_views, max_views, age_options,
                                       gender_choice, locations, languages, keyword=None, channel_index=None):
    """
    Applies filters including reach, engagement, age, gender, locations, languages, and keyword/channel.
    """
    if channel_index is not None:
        select_channel_by_occurrence(driver, channel_index)

    if keyword:
        input_keyword(driver, keyword)

    try:
        reach_engagement_button = driver.find_element(By.XPATH, "//span[contains(text(),'Reach & Engagement')]")
        reach_engagement_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking 'Reach & Engagement' filter: {e}")
        return

    try:
        min_follower_input = driver.find_elements(By.CLASS_NAME, "_input_c76r6_251")[1]
        actions = ActionChains(driver)
        actions.double_click(min_follower_input).perform()
        min_follower_input.send_keys(Keys.BACKSPACE)  # Delete existing content
        min_follower_input.send_keys(str(min_follower))
        min_follower_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"Error setting min follower count: {e}")
        return

    try:
        max_follower_input = driver.find_elements(By.CLASS_NAME, "_input_c76r6_251")[2]
        actions.double_click(max_follower_input).perform()
        max_follower_input.send_keys(Keys.BACKSPACE)
        max_follower_input.send_keys(str(max_follower))
        max_follower_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"Error setting max follower count: {e}")
        return

    try:
        min_views_input = driver.find_elements(By.CLASS_NAME, "_input_c76r6_251")[3]
        actions.double_click(min_views_input).perform()
        min_views_input.send_keys(Keys.BACKSPACE)
        min_views_input.send_keys(str(min_views))
        min_views_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"Error setting min views count: {e}")
        return

    try:
        max_views_input = driver.find_elements(By.CLASS_NAME, "_input_c76r6_251")[4]
        actions.double_click(max_views_input).perform()
        max_views_input.send_keys(Keys.BACKSPACE)
        max_views_input.send_keys(str(max_views))
        max_views_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"Error setting max views count: {e}")
        return

    select_creator_demographics(driver, age_options, gender_choice)
    input_location_and_language(driver, locations, languages)

    try:
        apply_button = driver.find_element(By.XPATH, "//div[contains(text(),'Apply Search & Filters')]")
        apply_button.click()
        time.sleep(2)
        print(
            f"Filters applied: Followers between {min_follower} and {max_follower}, views per video between {min_views} and {max_views}.")
    except Exception as e:
        print(f"Error applying filters: {e}")