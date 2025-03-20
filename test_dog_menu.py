import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base URL for the site
BASE_URL = "https://qa-tipalti-assignment.tipalti-pg.com/index.html"

def open_site(driver, url=BASE_URL):
    """
    Navigates to the specified URL.
    """
    driver.get(url)
    print("Navigated to site:", url)

def open_menu(driver):
    """
    Clicks on the hamburger/menu button to open the menu options.
    Adjust the selector if needed.
    """
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#menu']"))
    )
    menu_button.click()
    print("Menu button clicked.")

def get_menu_items(driver):
    """
    Retrieves the text of all menu items and stores them in a list.
    Adjust the XPath to match the site’s HTML structure.
    """
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//ul"))
    )
    menu_links = driver.find_elements(By.XPATH, "//ul/li/a")
    # Strip text and filter out empty strings
    menu_texts = [link.text.strip() for link in menu_links if link.text.strip()]
    print("Retrieved menu items:", menu_texts)
    return menu_texts

def verify_menu_item_exists(menu_items, dog_name):
    """
    Verifies that the expected menu item (dog name) exists in the list.
    """
    assert dog_name in menu_items, f"Menu item '{dog_name}' not found in {menu_items}"
    print(f"Menu item '{dog_name}' verified to exist.")

def click_menu_item(driver, dog_name):
    """
    Clicks on the menu item corresponding to the given dog name.
    """
    dog_element = driver.find_element(By.XPATH, f"//ul/li/a[text()='{dog_name}']")
    dog_element.click()
    print(f"Clicked on menu item: {dog_name}")

def fill_contact_form(driver, name, email, message):
    """
    Fills in the contact form fields (Name, Email, and Message) with the provided details.
    Waits for each element, scrolls to it, clicks on it, clears it, and then enters text.
    """
    try:
        # Wait for and scroll to the name field
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", name_field)
        name_field.click()
        name_field.clear()
        name_field.send_keys(name)
        print("Name field filled.")

        # Wait for and scroll to the email field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        email_field.click()
        email_field.clear()
        email_field.send_keys(email)
        print("Email field filled.")

        # Wait for and scroll to the message field
        message_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "message"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", message_field)
        message_field.click()
        message_field.clear()
        message_field.send_keys(message)
        print("Message field filled.")

    except Exception as e:
        print("One or more form elements were not found. Please verify the field names and page structure.")
        raise e

def send_details(driver):
    """
    Clicks the submit button to send the contact form details.
    Attempts multiple selectors if the button is not found.
    """
    try:
        # First, try to find the button using the CSS selector "button[type='submit']"
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
    except Exception as e1:
        print("Submit button not found using button[type='submit']. Trying alternative selector...")
        try:
            # Try alternative selector: input[type='submit']
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
            )
        except Exception as e2:
            print("Submit button not found using input[type='submit'].")
            print(driver.page_source)
            raise e2

    driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
    send_button.click()
    print("Submit button clicked.")

def test_dog_menu_item(driver, dog_name):
    """
    Complete test scenario for a specific dog menu item:
    1. Navigate to the site.
    2. Open the menu.
    3. Retrieve the menu items.
    4. Verify the expected dog menu item exists.
    5. Click on the menu item.
    6. Fill in the contact form.
    7. Create a custom message containing the dog's name.
    8. Submit the form (note: an error page is expected upon submission).
    """
    open_site(driver)                   # Step 1: Navigate to the website
    open_menu(driver)                   # Step 2: Open the menu
    items = get_menu_items(driver)      # Step 3: Retrieve menu items
    verify_menu_item_exists(items, dog_name)  # Step 4: Verify the dog menu item exists
    click_menu_item(driver, dog_name)         # Step 5: Click on the menu item

    # Bonus: Create a unique message that includes the dog's name
    custom_message = f"Hello, I am interested in dog-walking with {dog_name}!"

    # Step 6: Fill in the contact form with sample details and the custom message
    fill_contact_form(
        driver,
        name="Netanel",
        email="nnati9292@gmail.com",
        message=custom_message
    )

    send_details(driver)  # Step 7: Submit the form (expected error page upon submission)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        # For example, test the menu item "Kika"
        test_dog_menu_item(driver, "Kika")
    except Exception as e:
        print("An error occurred during testing:", e)
    finally:
        time.sleep(5)  # Pause to observe the result
        driver.quit()  # Close the browser
