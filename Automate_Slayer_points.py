import selenium.webdriver as Webdriver
import selenium.webdriver.chrome.options as option
import selenium.webdriver.common.keys as Key
import selenium.webdriver.common.by as by
import selenium.webdriver.support.ui as ui
import selenium.common.exceptions as exceptions
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.common.desired_capabilities as DC
import sys, re, pickle, os

def openWindow(link, mainwindow):
    # A function to open new window with the link given
    href = link.get_attribute('href')
    if href:
        browser.execute_script("window.open(arguments[0]);", href)
    else:
        link.click()
    # A window that IS NOT the current window is grabbed, in this case, this is always browser.window_handles[1]
    new_window = [window for window in browser.window_handles if window != mainwindow][0]
    # But we still use a loop just to make sure, explicit is better than implicit
    browser.switch_to.window(new_window)

def closeWindow(mainwindow):
    # A function to close current window and switch to given window hanlde
    browser.close()
    browser.switch_to.window(mainwindow)

def sanitycheckInfo(list):
    # A function to check whether the event informations are actual numbers
    try:
       int(list[0][0])
       int(list[0][1])
       int(list[0][2])
       return True
    except:
        return False

def userCreation():
    # A function to create User-Settings.txt
    with open("User-Settings.txt", 'w') as userfile:
        name = input("Enter Slayers Club Username: ")
        password = input("Enter Slayers club Password: ")
        userfile.write("User=" + str(name) + " Pass=" + str(password) + "\neventview=0 eventshare=0 calenderview=0 giveawayview=0 ")
    os.system("attrib +h User-Settings.txt")

def extractInfo(flag):
    # A function to extract desired info from User-Settings.txt
    try: 
        with open("User-Settings.txt", 'r') as statusfile:
            content = str(statusfile.read(100))
    except: 
        with open("User-Settings.txt", 'w+') as statusfile:
            # If the file does not exist, it is created
            userCreation()
            content = str(statusfile.read(100))
    if flag == 0:
        # Regex to grab the username and password
        infolist = re.findall(r"User=(.+) Pass=(.+)", content)
        return infolist
    elif flag == 1:
        # Regex to grab the event information
        infolist = re.findall(r"eventview=(.+) eventshare=(.+) calenderview=(.+) g", content)
        return infolist if sanitycheckInfo(infolist) else exitScript(5)
    elif flag == 2:
        # Regex to grab the giveaway information
        info = re.findall(r"giveawayview=(.+) ", content)
        try: 
            return True if info[0] is '1' else False
        except: 
            return False

def checkSharelimit():
    # A function check whether the user has reached max daily shares
    item = browser.find_element_by_class_name("share-bar__title")
    text = item.find_element_by_class_name("text").text
    if text == "You've reached the 3 maximum shares for today":
        return True
    else:
        return False

def exitScript(code, message = None):
    # A function to handle various exit conditions
    if code == 0:
        input("Tasks completed successfully!\n    You may close this console or press any key\n")
        browser.close()
        sys.exit(0)
    elif code == 1:
        input("ERROR: Request timed out, please try again later.\nMessage: " + message + "\n    You may close this console or press any key\n")
        browser.close()
        sys.exit(1)
    elif code == 2:
        input("ERROR: Invalid Credentials, please try again.\n    You may close this console or press any key\n")
        # The User-Settings file is removed if the credentials are invalid
        # So it can be created again from scratch
        os.remove("User-Settings.txt")
        browser.close()
        sys.exit(2)
    elif code == 3:
        input("ERROR: Discord widget took too long to respond, please try again later.\n    You may close this console or press any key\n")
        browser.close()
        sys.exit(3)
    elif code == 4:
        input("ERROR: An unexpected error occured, make sure that chromedriver is present in the same directory.\n    You may close this console or press any key\n")
        browser.close()
        sys.exit(4)
    elif code == 5:
        input("ERROR: User-Settings.txt Sanity check failed, please try again later.\n    You may close this console or press any key\n")
        # The User-Settings file is removed if the event/giveaway informations are invalid
        # So it can be created again from scratch
        os.remove("User-Settings.txt")
        browser.close()
        sys.exit(5)

if __name__ == "__main__":
    print("Starting Tasks\n    DO NOT CLOSE THIS CONSOLE")
    # Setting up the selenium environment - Using Chromedriver
    # chromedriver.exe is expected to be found at the same directory as the program
    CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
    WINDOW_SIZE = "1920,1080"
    chrome_options = option.Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-notifications")

    caps = DC.DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    try: 
        browser = Webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, 
                                   options = chrome_options, desired_capabilities = caps)
    except:
        #Exit code 4 is when chromedriver.exe isn't found in the directory (usually)
        exitScript(4)
    #Setting up a few explicit wait classes, for standard, extended and discord widget (iframe) loading respectively
    std_wait = ui.WebDriverWait(browser, 10)
    extended_wait = ui.WebDriverWait(browser, 30)
    iframe_wait = ui.WebDriverWait(browser, 60)

    """
    Here, Username and Password are extracted from
    User-Settings.txt first
    If the credentials exist: 
        The browser opens the homepage and sign in 
        if the attempt is successfull, it'll move on
        To determine whether the attempt was successfull, the browser
        tries to find an element only visible after being logged in
        This element is- <a class="button button--outlined points-button" href="/en">
    If the credentials don't exist:
        userCreation() method is called and the user is asked
        for username and password, which are then stored in
        User-Settings.txt
    """

    userinfolist = extractInfo(0)
    # Userinfolist holds username and password like so (regex method) : [(name, pass)]
    try:
        USER_NAME = str(userinfolist[0][0])
        PASSWORD = str(userinfolist[0][1])
    except:
        exitScript(2)
    print("Loading webpage....")
    try:
        browser.get(r"https://slayersclub.bethesda.net/en/#")
        std_wait.until(EC.element_to_be_clickable((by.By.CLASS_NAME, "sc-options__button"))
                       ).click()
        print("Signing in....")
        extended_wait.until(EC.presence_of_element_located((by.By.NAME, "username"))
                       ).send_keys(USER_NAME)
        browser.find_element_by_name("password").send_keys(PASSWORD)
        browser.find_element_by_id("submitLoginBtn").click()
        std_wait.until(EC.presence_of_element_located((by.By.XPATH, "//*[@class = 'button button--outlined points-button']"))
                       )
        print("Succesfully logged in")
    except exceptions.TimeoutException:
        # Exit code 2 is when the input credentials are wrong
        # as in, failure to find the element at line 155
        exitScript(2)

    """
    This part is for visiting the Forum page
    The element being clicked on is the 'Visit Forum' button on the sidebar
    Usually links are passed onto openWindow() function for them
    to be opened on another window, however, this link's href
    is not direct so a window is opened manually
    browser.window_handles[0] stands for current window handle
    browser.window_handles[1] stands for another window
    (only applicable when there's a single window open)
    The new window (forum) is then closed as soon as it's fully loaded
    through the use of closeWindow() method
    """

    print("Visiting forum....")
    try: 
        mainwindow = browser.current_window_handle
        link = std_wait.until(EC.presence_of_element_located((by.By.XPATH, "//a[@class = 'button button--outlined points-button']"))
                          ).click()

        new_window = browser.window_handles[1]
        browser.switch_to.window(new_window)
        std_wait.until(EC.presence_of_element_located((by.By.ID, "category-251"))
                       )
        closeWindow(mainwindow)
    except:
        # Exit code 1 is when the page takes too long to load
        exitScript(1, "Forum Page")

    sharelimit = False      # This variable is to determine whether user has already reached daily share limit

    """
    This part is for visiting the Events page
    Firstly, information about how many events have already
    been viewed/shared/added to calender is extracted
    This is always [(0, 0, 0)] for the first use of the program

    Then, a list of all events is stored in a webelement list
    It is iterated through on reverse (since newest events are on the top),
    skipping through events that have already been seen AND shared AND added to calender(line 218)
    If any of those conditions aren't met, the event page is opened 
    in a new window and looked through for "check" icons
    
    The check sign for viewing has class = 'check check--small', this should
    always be found as even when it's not there, the std_wait makes sure the website
    registers the page as 'viewed' and adds the check icon

    The check signs for calender and share have the same class = 'check check--small check--inline'
    If both are found, there are no exceptions and the program moves on, adding a +1 to the 
    share counter (not counting towards sharelimit)
    If only one found (regardless of which), a exception is caught and
    here, the attempt to BOTH share the event AND add to calender is made
    first the sharelimit is checked
    If sharelimit has not been reached (Value = False): 
        The browser clicks on the share button (facebook) which opens a new window
        The browser then switches to the new window, in this case browser.window_handles[2]
        Waits until it's loaded and then closes it, switching back to the event page window
    If sharelimit has been reached (Value = True):
        Sharing is skipped altogether
    Then, the browser clicks on the google calender link, which automatically opens a new window
    The browser switches to the new window, in this case browser.window_handles[2]
    Waits until it's loaded and then closes it, switching back to the event page window
    Finally, the event page is closed which means the only remaining window is the Events page again
    This is repeated until All events are viewed and added to calender
    """

    print("Viewing Events....")
    i = 0
    shared = 0
    infolist = extractInfo(1)
    eventsviewed = int(infolist[0][0])
    eventsshared = int(infolist[0][1])
    calenderviewed = int(infolist[0][2])
    try: 
        browser.get(r"https://slayersclub.bethesda.net/en/events")
        eventlist = std_wait.until(EC.presence_of_all_elements_located((by.By.CLASS_NAME, "entry-card-listing__listing-item"))
                                   )
    except:
        # Exit code 1 is when the page takes too long to load
        exitScript(1, "Events page")
    mainwindow = browser.current_window_handle
    for item in reversed(eventlist):
        if i < eventsviewed and i < eventsshared and i < calenderviewed:
            i += 1
            continue
        if eventsviewed == len(eventlist) and calenderviewed == len(eventlist) and sharelimit:
            break
        # Each link is opened in a new window
        link = item.find_element_by_tag_name("a")
        openWindow(link, mainwindow)
        try:
            share_bar = std_wait.until(EC.presence_of_element_located((by.By.CLASS_NAME, "share-bar__title"))
                                       )
            # The scrolling down is just to register the page as read
            browser.execute_script("arguments[0].scrollIntoView();", share_bar)
            std_wait.until(EC.presence_of_element_located((by.By.XPATH, "//*[@class = 'check check--small']"))
                           )
            browser.find_elements_by_xpath("//*[@class = 'check check--small check--inline']")[1]
            shared += 1
        except IndexError:
            if not sharelimit:
                sharelimit = checkSharelimit()
            if not sharelimit:
                thisWindow = browser.current_window_handle
                sharebut = browser.find_element_by_xpath("//button[@class = 'button button--small button--outlined share-bar__button']")
                browser.execute_script("arguments[0].click();", sharebut)
                browser.switch_to.window(browser.window_handles[2])
                std_wait.until(EC.presence_of_element_located((by.By.TAG_NAME, "body"))
                                )
                closeWindow(thisWindow)
                shared += 1
            if len(eventlist) > calenderviewed:
                calender_but = browser.find_element_by_class_name("react-add-to-calendar__button")
                thisWindow = browser.current_window_handle
                browser.execute_script("arguments[0].click();", calender_but)
                link = std_wait.until(EC.presence_of_element_located((by.By.CLASS_NAME, "google-link"))
                               )
                browser.execute_script("arguments[0].click();", link)
                browser.switch_to.window(browser.window_handles[2])
                std_wait.until(EC.presence_of_element_located((by.By.TAG_NAME, "body"))
                               )
                closeWindow(thisWindow)
        except exceptions.TimeoutException: 
            # Exit code 1 is when the page takes too long to load
            exitScript(1, "Specific Event Page")
        closeWindow(mainwindow)

    """
    This part is for visitng the Giveaways page
    This is much the same as the events part, information
    about progress is extracted from User-Settings.txt
    This is always 0 on first startup, after first
    successfull completion of all tasks (except discord) it is 1
    giveaway_done == 1 means only the first giveaway page (newest) will be opened
    for viewing and then closed
    giveaway_done == 0 means all the giveaways have not yet been viewed and hence
    they will all be opened in much the same fashion as each event from events page
    
    Finally User-Settings.txt is updated with the progress made
    eventview and calenderview is always set to the amount of events available, because 
    the program is supposed to view every single event and add each of them to calender
    in it's first try
    eventshare is set to the previous amount of shares + this session's shares
    giveawayview is always set to 1, because the program is supposed to view every
    giveaway
    """

    print("Viewing Giveaways....")
    i = 0
    giveaway_done = extractInfo(2)
    try: 
        browser.get("https://slayersclub.bethesda.net/en/giveaways")
        giveawaylist = std_wait.until(EC.presence_of_all_elements_located((by.By.CLASS_NAME, "entry-card-listing__listing-item"))
                                      )
    except:
        # Exit code 1 is when the page takes too long to load
        exitScript(1)
    mainwindow = browser.current_window_handle
    for item in giveawaylist:
        if giveaway_done:
            break
        try: 
            link = item.find_element_by_tag_name("a")
            openWindow(link, mainwindow)
            listing_header = std_wait.until(EC.presence_of_element_located((by.By.CLASS_NAME, "entry-card-listing__header"))
                           )
            # The scrolling down is just to register the page as read
            browser.execute_script("arguments[0].scrollIntoView();", listing_header)
            std_wait.until(EC.presence_of_element_located((by.By.XPATH, "//*[@class = 'check check--small']"))
                           )
            closeWindow(mainwindow)
        except exceptions.NoSuchElementException: 
            # This exception will only occur when the link is not found
            # Which means, the Event is not actually clickable, so it is skipped
            continue
        except exceptions.TimeoutException:
            # Exit code 1 is when the page takes too long to load
            exitScript(1, "Giveaways page")

    # Wiping the file and updating it from scratch and then setting it back to hidden
    os.system("attrib -h User-Settings.txt")
    open("User-Settings.txt", 'w').close()
    with open("User-Settings.txt", 'w') as file:
        file.write(str("User=" + str(USER_NAME) + " Pass=" + str(PASSWORD) + "\neventview=" + str(len(eventlist)) + " eventshare=" + str(eventsshared + shared) + " calenderview=" + str(len(eventlist)) + " giveawayview=1 "))
    os.system("attrib +h User-Settings.txt")

    """
    This part is for visiting discord, I put it last because
    discord widget takes quite awhile to load and this is the
    most common thing that will cause errors
    But if it is successfully loaded in, it'll just click an element on it
    and close the program
    """

    print("Visiting Discord....")
    try: 
        browser.get(r"https://slayersclub.bethesda.net/en/#")
        leaderboard = std_wait.until(EC.presence_of_element_located((by.By.CSS_SELECTOR, "div[class = 'module top-contributors']"))
                       )
        browser.execute_script("arguments[0].scrollIntoView();", leaderboard)
        iframes = extended_wait.until(EC.presence_of_all_elements_located((by.By.CSS_SELECTOR, "div[class = 'frame frame--padding']"))
                                    )
        iframes[1].click()
        browser.switch_to.frame(browser.find_element_by_id("discordIframe"))
        extended_wait.until(EC.presence_of_element_located((by.By.CLASS_NAME, "widgetBtnConnect-2fvtGa"))
                      ).click()
    except:
        # Exit code 1 is when the page takes too long to load
        exitScript(1, "Discord Widget")

    exitScript(0)