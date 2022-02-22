import time
from datetime import datetime
from time import sleep
from timeit import default_timer as timer

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from paths import DRIVER_PATH, CHROME_PROFILE


def is_media_in_message(message):
    '''Returns True if media is discovered within the message by checking the soup for known media flags. If not, it returns False.'''

    # First check for data-testid attributes containing 'media' or 'download' (this covers gifs, videos, downloadable content)
    possible_media_spans = message.find_all(attrs={'data-testid': True})
    for span in possible_media_spans:
        # Media types are stored in 'data-testid' attribute
        media_attr = span.get('data-testid')

        if 'media' in media_attr or 'download' in media_attr:
            return True
        else:
            continue

    # Check if the media is a shared contact e.g. vCard/VCF, or a sticker
    if message.get('class'):
        # Check for shared contact
        copyable = message.find('div', 'copyable-text')
        if copyable:
            # Get all buttons
            buttons = copyable.find_all('div', {'role': 'button'})
            if buttons:
                # Look for contact card button pattern (2 divs w/ titles of 'Message X' and 'Add to a group')
                for button in buttons:
                    # Only check buttons with Title attribute
                    if button.get('title'):
                        # Check if 'Message' is in the title (full title would be for example 'Message Bob Ross')
                        if 'Message' in button.get('title'):
                            # Next sibling should always be the 'Add to a group' button
                            if button.nextSibling:
                                if button.nextSibling.get('title') == 'Add to a group':
                                    return True

        # Check for group sticker (2 side-by-side stickers)
        if 'grouped-sticker' in message.get('data-id'):
            return True

        # Check for individual sticker
        images = message.find_all('img')
        if images:
            for image in images:
                if 'blob' in image.get('src', ''):
                    return True

    return False


def download_data_from_groups(groups):
    # Setup selenium to use Chrome browser w/ profile options
    driver = setup_selenium()

    # Load WhatsApp
    if not whatsapp_is_loaded(driver):
        print("You've quit WhatSoup.")
        driver.quit()
        return
    data_for_group = {}
    # Prompt user to select a chat for export, then locate and load it in WhatsApp
    for group in groups:
        chat_is_loaded = False
        while not chat_is_loaded:
            # Select a chat and locate in WhatsApp
            chat_is_loadable = False
            while not chat_is_loadable:
                # Ask user what chat to export
                selected_chat = group
                if not selected_chat:
                    print("You've quit WhatSoup.")
                    driver.quit()
                    return

                # Find the selected chat in WhatsApp
                found_selected_chat = find_selected_chat(driver, selected_chat)
                if found_selected_chat:
                    # Break and proceed to load/scrape the chat
                    chat_is_loadable = True
                else:
                    # Clear chat search
                    driver.find_element_by_xpath(
                        '//*[@id="side"]/div[1]/div/span/button').click()

            # Load entire chat history
            chat_is_loaded = load_selected_chat(driver)

        # Scrape the chat history
        scraped = scrape_chat(driver)
        data_for_group[group] = scraped

    driver.quit()
    return data_for_group


def setup_selenium():
    '''Setup Selenium to use Chrome webdriver'''

    # Load driver and chrome profile from local directories
    load_dotenv()
    # Configure selenium
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_PROFILE}")
    driver = webdriver.Chrome(
        executable_path=DRIVER_PATH, options=options)
    # Change default script timeout from 30sec to 90sec for execute_script tasks which slow down significantly in very large chats
    driver.set_script_timeout(90)

    return driver


def whatsapp_is_loaded(driver):
    '''Attempts to load WhatsApp in the browser'''

    print("Loading WhatsApp...", end="\r")

    # Open WhatsApp
    driver.get('https://web.whatsapp.com/')

    # Check if user is already logged in
    logged_in, wait_time = False, 20
    while not logged_in:

        # Try logging in
        logged_in = user_is_logged_in(driver, wait_time)

        # Allow user to try again and extend the wait time for WhatsApp to load
        if not logged_in:
            # Display error to user
            print(
                f"Error: WhatsApp did not load within {wait_time} seconds. Make sure you are logged in and let's try again.")

    # Success
    print("Success! WhatsApp finished loading and is ready.")
    return True


def user_is_logged_in(driver, wait_time):
    '''Checks if the user is logged in to WhatsApp by looking for the pressence of the chat-pane'''

    try:
        chat_pane = WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located((By.ID, 'pane-side')))
        return True
    except TimeoutException:
        return False


def load_selected_chat(driver):
    '''Loads entire chat history by repeatedly scrolling up to fetch more data from WhatsApp'''
    print('loading chat history')
    time.sleep(15)
    start = timer()
    print("Loading messages...", end="\r")

    # Set focus to chat window (xpath == div element w/ aria-label set to 'Message list. Press right arrow key...')
    message_list_element = driver.find_element_by_xpath(
        "//*[@id='main']/div[3]/div/div/div[contains(@aria-label,'Message list')]")
    message_list_element.send_keys(Keys.NULL)

    # Get scroll height of the chat pane div so we can calculate if new messages were loaded
    current_scroll_height = driver.execute_script(
        "return arguments[0].scrollHeight;", message_list_element)
    previous_scroll_height = current_scroll_height

    # Load all messages by scrolling up and continually checking scroll height to verify more messages have loaded
    all_msgs_loaded = False
    retry_attempts, success_attempts = 0, 0
    while not all_msgs_loaded:
        # Scroll to anchor at top of message list (fetches more messages)
        driver.execute_script(
            "arguments[0].scrollIntoView();", message_list_element)

        # Grant some time for messages to load
        sleep(2)

        # Get scroll height of the chat pane div so we can calculate if new messages were loaded
        previous_scroll_height = current_scroll_height
        current_scroll_height = driver.execute_script(
            "return arguments[0].scrollHeight;", message_list_element)

        # Check if scroll height changed
        if current_scroll_height > previous_scroll_height:
            # New messages were loaded, reset retry counter
            retry_attempts = 0

            # Increment success attempts for user awareness
            success_attempts += 1
            print(
                f"Load new messages succeeded {success_attempts} times", end="\r")

            # Loop back and load more messages
            continue

        # Check if all messages were loaded or retry loading more
        elif current_scroll_height == previous_scroll_height:
            # All messages loaded? (xpath == 'load earlier messages' / 'loading messages...' div that is deleted from DOM after all messages have loaded)
            loading_earlier_msgs = driver.find_element_by_xpath(
                '//*[@id="main"]/div[3]/div/div/div[2]/div').get_attribute('title')
            if 'load' not in loading_earlier_msgs:
                all_msgs_loaded = True
                end = timer()
                print(
                    f"Success! Your entire chat history has been loaded in {round(end - start)} seconds.")
                break

            # Retry loading more messages
            else:
                # Make sure we grant user option to exit if ~60sec of attempting to load more messages doesn't result in new messages loading
                if retry_attempts >= 30:
                    print("This is taking longer than usual...")
                    while True:
                        response = input(
                            "Try loading more messages (y/n)? ")
                        if response.strip().lower() in {'n', 'no'}:
                            print(
                                'Error! Aborting chat load by user due to loading timeout.')
                            return False
                        elif response.strip().lower() in {'y', 'yes'}:
                            # Set focus to chat window again
                            message_list_element.send_keys(Keys.NULL)

                            # Reset counter
                            retry_attempts = 0
                            break
                        else:
                            continue

                # Increment retry acounter and load more messages
                else:
                    retry_attempts += 1
                    continue

    return True


def find_selected_chat(driver, selected_chat):
    '''Searches and loads the initial chat. Returns True/False if the chat is found and can be loaded.

    Assumptions:
    1) The chat is searchable and exists because we scraped it earlier in get_chats
    2) The searched chat will always be the first element under the search input box
    '''

    print(f"Searching for '{selected_chat}'...", end="\r")

    # Find the chat via search (xpath == 'Search or start new chat' element)
    chat_search = driver.find_element_by_xpath(
        '//*[@id="side"]/div[1]/div/label/div/div[2]')
    chat_search.click()

    # Type the chat name into the search box using a JavaScript hack because Selenium/Chromedriver doesn't support all unicode chars - https://bugs.chromium.org/p/chromedriver/issues/detail?id=2269
    driver.execute_script(
        f"arguments[0].innerHTML = '{selected_chat}'", chat_search)

    # Manually fire the JS listeners/events with keyboard input that adds/removes a space at end of search string
    chat_search.send_keys(Keys.END)
    chat_search.send_keys(Keys.SPACE)
    chat_search.send_keys(Keys.BACKSPACE)

    # Wait for search results to load (5 sec max)
    try:
        # Look for the unique class that holds 'Search results.'
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(
            (By.XPATH, "//*[@id='pane-side']/div[1]/div/div[contains(@aria-label,'Search results.')]")))

        # Force small sleep to deal with issue where focus gets interrupted after wait
        sleep(2)
    except TimeoutException:
        print(
            f"Error! '{selected_chat}' produced no search results in WhatsApp.")
        return False
    else:
        # Navigate to the chat, first element below search input
        chat_search.send_keys(Keys.DOWN)

        # Fetch the element
        search_result = driver.switch_to.active_element

        try:
            # Look for the chat name header and a title attribute that matches the selected chat
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(
                (By.XPATH, f"//*[@id='main']/header/div[2]/div[1]/div/span[contains(@title,'{selected_chat}')]")))
        except TimeoutException:
            print(
                f"Error! '{selected_chat}' chat could not be loaded in WhatsApp.")
            return False
        else:
            # Get the chat name (xpath == span w/ title set to chat name, a descendant of header tag and anchored at top of chat window)
            chat_name_header = driver.find_element_by_xpath(
                '//*[@id="main"]/header/div[2]/div[1]/div/span').get_attribute('title')

            # Compare searched chat name to the selected chat name
            if chat_name_header == selected_chat:
                print(f"Success! '{selected_chat}' was found.")
                return True
            else:
                print(
                    f"Error! '{selected_chat}' search results loaded the wrong chat: '{chat_name_header}'")
                return False


def scrape_chat(driver):
    '''Turns the chat into soup and scrapes it for key export information: message sender, message date/time, message contents'''

    print("Scraping messages...", end="\r")

    # Make soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Get the 'Message list' element that is a container for all messages in the right chat pane

    # Search for and only keep HTML elements which contain actual messages
    chat_messages = [
        msg for msg in soup.find("div", driver.find_element_by_xpath(
            '//*[@id="main"]/div[3]/div/div/div[2]').get_attribute('class')).contents if
        'message' in " ".join(msg.get('class'))]
    if not chat_messages:
        chat_messages = [
            msg for msg in soup.find("div", driver.find_element_by_xpath(
                '//*[@id="main"]/div[3]/div/div/div[3]').get_attribute('class')).contents if
            'message' in " ".join(msg.get('class'))] # TODO [YG] : check failure when there is no new massages
    chat_messages_count = len(chat_messages)

    # Get users profile name
    you = get_users_profile_name(chat_messages)

    # Loop thru all chat messages, scrape chat info into a dict, and add it to a list
    messages = []
    messages_count = 0
    last_msg_date = None
    for message in chat_messages:
        # Count messages for progress message to user and to compare expected vs actual scraped chat messages
        messages_count += 1
        print(
            f"Scraping message {messages_count} of {chat_messages_count}", end="\r")

        # Dictionary for holding chat information (sender, msg date/time, msg contents, message content types, and data-id for debugging)
        message_scraped = {
            "sender": None,
            "datetime": None,
            "message": None,
            "has_copyable_text": False,
            "has_selectable_text": False,
            "has_emoji_text": False,
            "has_media": False,
            "has_recall": False,
            "data-id": message.get('data-id')
        }

        # Approach for scraping: search for everything we need in 'copyable-text' to start with, then 'selectable-text', and so on as we look for certain HTML patterns. As patterns are identified, update the message_scraped dict.
        # Check if message has 'copyable-text' (copyable-text tends to be a container div for messages that have text in it, storing sender/datetime within data-* attributes)
        copyable_text = message.find('div', 'copyable-text')
        if copyable_text:
            message_scraped['has_copyable_text'] = True

            # Scrape the 'copyable-text' element for the message's sender, date/time, and contents
            copyable_scrape = scrape_copyable(copyable_text)

            # Update the message object
            message_scraped['datetime'] = copyable_scrape['datetime']
            last_msg_date = message_scraped['datetime']
            message_scraped['sender'] = copyable_scrape['sender']
            message_scraped['message'] = copyable_scrape['message']

            # Check if message has 'selectable-text' (selectable-text tends to be a copyable-text child container span/div for messages that have text in it, storing the actual chat message text/emojis)
            if copyable_text.find('span', 'selectable-text'):
                # Span element
                selectable_text = copyable_text.find(
                    'span', 'selectable-text')
            else:
                # Div element
                selectable_text = copyable_text.find(
                    'div', 'selectable-text')

            # Check if message has emojis and overwrite the message object w/ updated chat message
            if selectable_text:
                message_scraped['has_selectable_text'] = True

                # Does it contain emojis? Emoji's are renderd as <img> elements which are child to the parent span/div container w/ selectable-text class
                if selectable_text.find('img'):
                    message_scraped['has_emoji_text'] = True

                # Get message from selectable and overwrite existing chat message
                message_scraped['message'] = scrape_selectable(
                    selectable_text, message_scraped['has_emoji_text'])

        # Check if message was recalled
        if is_recall_in_message(message):
            message_scraped['has_recall'] = True

            # Update the message object
            message_scraped['datetime'] = find_chat_datetime_when_copyable_does_not_exist(
                message, last_msg_date)
            last_msg_date = message_scraped['datetime']
            message_scraped['sender'] = you
            message_scraped['message'] = "<You deleted this message>"

        # Check if the message has media
        message_scraped['has_media'] = is_media_in_message(message)
        if message_scraped['has_media']:
            # Check if it also has text
            if message_scraped['has_copyable_text']:
                # Update chat message w/ media omission (note that copyable has already scraped the sender + datetime)
                message_scraped['message'] = f"<Media omitted> {message_scraped['message']}"

            else:
                # Without copyable, we need to scrape the sender in a different way
                if 'message-out' in message.get('class'):
                    # Message was sent by the user
                    message_scraped['sender'] = you
                elif 'message-in' in message.get('class'):
                    # Message was sent from a friend of the user
                    message_scraped['sender'] = find_media_sender_when_copyable_does_not_exist(
                        message)
                    if not message_scraped['sender']:
                        # Only occurs intermittently when the senders name does not exist in the message - so we take the last message's sender
                        message_scraped['sender'] = messages[-1]['sender']
                else:
                    pass

                # Get the date/time and update the message object
                message_scraped['datetime'] = find_chat_datetime_when_copyable_does_not_exist(
                    message, last_msg_date)
                last_msg_date = message_scraped['datetime']
                message_scraped['message'] = '<Media omitted>'
        if message_scraped['message'] is None:
            continue
        # Add the message object to list
        if 'grouped-sticker' not in message.get('data-id'):
            messages.append(message_scraped.copy())
        else:
            # Make duplicate entry for grouped sticker to match behavior with WhatsApp export (i.e. a group sticker == 2 lines in the txt export both with <Media omitted> messages)
            messages.append(message_scraped.copy())
            messages.append(message_scraped.copy())

            # Finally, update expectd msg count
            chat_messages_count += 1

        # Loop to the next chat message
        continue

    # Scrape summary
    if len(messages) == chat_messages_count:
        print(f"Success! All {len(messages)} messages have been scraped.")
    else:
        print(
            f"Warning! {len(messages)} messages scraped but {chat_messages_count} expected.")

    # Create a dict with chat date as key and empty list as value which will store all msgs for that date
    messages_dict = {msg_list['datetime'].strftime(
        "%m/%d/%Y"): [] for msg_list in messages}

    # Update the dict by inserting message content as values
    for m in messages:
        messages_dict[m['datetime'].strftime("%m/%d/%Y")].append(
            {'time': m['datetime'].strftime("%I:%M %p"), 'sender': m['sender'], 'text': m['message']})

    return messages_dict


def get_users_profile_name(chat_messages):
    '''Returns the user's profile name so we can determine who 'You' is in the conversation.

    WhatsApp's default 'export' fucntionality renders the users profile name and never 'You'.
    '''

    you = None
    for chat in chat_messages:
        if 'message-out' in chat.get('class'):
            chat_exists = chat.find('div', 'copyable-text')
            if chat_exists:
                you = chat.find(
                    'div', 'copyable-text').get('data-pre-plain-text').strip()[1:-1].split('] ')[1]
                break
    return you


def scrape_copyable(copyable_text):
    '''Returns a dict with values for sender, date/time, and contents of the WhatsApp message'''

    copyable_scrape = {'sender': None, 'datetime': None, 'message': None}

    # Get the elements attributes that hold the sender and date/time values
    copyable_attrs = copyable_text.get(
        'data-pre-plain-text').strip()[1:-1].split('] ')

    # Get the sender, date/time, and msg contents
    copyable_scrape['sender'] = copyable_attrs[1]
    copyable_scrape['datetime'] = parse_datetime(
        f"{copyable_attrs[0].split(', ')[1]} {copyable_attrs[0].split(', ')[0]}")

    # Get the text-only portion of the message contents (always in a span w/ copyable-text class)
    content = copyable_text.find('span', 'copyable-text')
    if content:
        copyable_scrape['message'] = content
    else:
        copyable_scrape['message'] = ''

    return copyable_scrape


def scrape_selectable(selectable_text, has_emoji=False):
    '''Returns message contents of a chat by checking for and handling emojis'''

    # Does it contain emojis?
    if has_emoji:
        # Construct the message manually because emoji content is broken up into many span/img elements that we need to loop through
        # Loop over every child span of selectable-text, as these wrap the text and emojis/imgs
        message = ''
        for span in selectable_text.find_all('span'):

            # Loop over every child element of the span to construct the message
            for element in span.contents:
                # Check what kind of element it is
                if element.name is None:
                    # Text, ignoring empty strings
                    if element == ' ':
                        continue
                    else:
                        message += str(element)
                elif element.name == 'img':
                    # Emoji
                    message += element.get('alt')
                else:
                    # Skip other elements (note: have not found any occurrences of this happening...yet)
                    continue

        return message
    else:
        # Return the text only
        return selectable_text.text


def is_recall_in_message(message):
    '''Returns True if message contains recall pattern (a span will contain 'recalled' in data-*), if not returns False.'''
    # Check if message contains spans
    spans = message.find_all('span')
    if spans:
        # Check all spans for recalled
        for span in spans:
            if span.get('data-testid') == 'recalled':
                return True

    return False


def find_chat_datetime_when_copyable_does_not_exist(message, last_msg_date):
    '''Returns a message's date/time when there's no 'copyable-text' attribute within the message e.g. deleted messages, media w/ no text, etc.'''

    spans = message.find_all('span')
    # Check if spans exist
    if spans:
        for span in spans:
            # Check spans w/ text if they are dates/times
            if span.text:
                try:
                    parse_datetime(span.text, time_only=True)
                except ValueError:
                    # Span text is not a date/time value
                    continue
                else:
                    # Get the hour/minute time from the media message
                    message_time = span.text

                    # Get a sibling div holding the latest chat date, otherwise if that doesn't exist then grab the last msg date
                    try:
                        # Check if row from message list is a date and not a chat, grabs the first available prior date (this fires for all but the first date of chat history messaging)
                        sibling_date = message.find_previous_sibling(
                            "div", attrs={'data-id': False}).text
                        if not sibling_date:
                            # Use the previous messages date if it exists
                            if last_msg_date:
                                sibling_date = last_msg_date.strftime(
                                    '%m/%d/%Y')
                            else:
                                # Otherwise use the next available subsequent date (note this fires only on the first message w/ rare conditions when copyable-text doesn't exist; could assign the wrong date if for example the next available date is 1+ day in advance of the current message)
                                sibling_date = message.find_next_sibling(
                                    "div", attrs={'data-id': False}).text

                        # Try converting to a date/time object
                        media_message_datetime = parse_datetime(
                            f"{sibling_date} {message_time}")

                        # Build date/time object
                        message_datetime = parse_datetime(
                            f"{media_message_datetime.strftime('%m/%d/%Y')} {media_message_datetime.strftime('%I:%M %p')}")

                        return message_datetime

                    # Otherwise last message's date/time (note this could assign the wrong date if for example the last message was 1+ days ago)
                    except ValueError:
                        message_datetime = parse_datetime(
                            f"{last_msg_date.strftime('%m/%d/%Y')} {message_time}")

                        return message_datetime

    else:
        return None


def parse_datetime(text, time_only=False):
    '''Try parsing and returning datetimes in a North American standard, otherwise raise a ValueError'''
    # TODO lazy approach to handling variances of North America date/time values MM/DD/YYYY AM/PM or YYYY-MM-DD A.M./P.M.

    # Normalize the text
    text = text.upper().replace("A.M.", "AM").replace("P.M.", "PM")

    # Try parsing when text is some datetime value e.g. 2/15/2021 2:35 P.M.
    if not time_only:
        for fmt in ('%m/%d/%Y %I:%M %p', '%Y-%m-%d %I:%M %p'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        raise ValueError(
            f"{text} does not match a valid datetime format of '%m/%d/%Y %I:%M %p' or '%Y-%m-%d %I:%M %p'. Make sure your WhatsApp language settings on your phone are set to English.")

    # Try parsing when text is some time value e.g. 2:35 PM
    else:
        try:
            return datetime.strptime(text, '%I:%M %p')
        except ValueError:
            pass
        raise ValueError(
            f"{text} does not match expected time format of '%I:%M %p'. Make sure your WhatsApp language settings on your phone are set to English.")


def find_media_sender_when_copyable_does_not_exist(message):
    '''Returns a sender's name when there's no 'copyable-text' attribute within the message'''

    # Check to see if senders name is stored in a span's aria-label attribute (note: this seems to be where it's stored if the persons name is just text / no emoji)
    spans = message.find_all('span')
    has_emoji = False
    for span in spans:
        if span.get('aria-label'):
            # Last char in aria-label is always colon after the senders name
            if span.get('aria-label') != 'Voice message':
                return span.get('aria-label')[:-1]
        elif span.find('img'):
            # Emoji is in name and needs to be handled differently
            has_emoji = True
            break
        else:
            continue

    # Manually construct the senders name if it has an emoji by building a string from span.text and img/emoji tags
    if has_emoji:
        # Get all elements from known emoji container span (always contained within a div that uses the class 'color-#' and will be the 0th child item)
        emoji_name_elements = message.select("div[class*='color']")[0].next

        # Loop over every child element of the span to construct the senders name
        name = ''
        for element in emoji_name_elements.contents:
            # Check what kind of element it is
            if element.name is None:
                # Text, ignoring empty strings
                if element == ' ':
                    continue
                else:
                    name += str(element)
            elif element.name == 'img':
                # Emoji
                name += element.get('alt')
            else:
                # Skip other elements (note: have not found any occurrences of this happening...yet)
                continue

        return name

    # There is no sender name in the message, an issue that occurrs very infrequently (e.g. 6000+ msg chat occurred 3 times) - pattern for this seems to be 1) sender name has no emoji, 2) msg has media, 3) msg does not have text, 4) msg is a follow-up / consecutive message (doesn't have tail-in icon in message span/svg)
    else:
        # TODO: Study this pattern more and fix later if possible. Solution for now is to return None and then we take the last message's sender from our data structure.
        return None
