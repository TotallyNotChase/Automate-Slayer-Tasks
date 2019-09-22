# A Slayer's Club browser for the lazy (or the busy)
This is a fairly simple script written in python, using selenium, to automate *daily tasks* on the **Slayer's Club** for **DOOM** by *iD software*.

The **source code** is included with a fair bit of *comments and documentation* right here, for everyone to see, as well!

![](https://i.imgur.com/guE8otf.png)

## Features
The script does the following things upon launch, in this order.
  1. Visits **forum**
  2. Visits **Events** page, where it *views*, *shares* and *adds the events to calender*
  3. Visits **Giveaways** page, where it *views* the giveaways.
  4. Visits **Discord** through the widget.

I didn't add any **News Article** automation because I want people to actually read them as they're really interesting. But if people *really* want it, I can add at most 5 most recent news article view/share task.

## Installation
This should work on **Windows**, that is confirmed, it should also work in **Linux**, though I'm not entirely sure and would appreciate if someone could confirm.

All you need to do is
  1. Download this *repo*

  ![](https://i.imgur.com/nuXjOwA.gif)

  2. Download **chromedriver.exe** through [this link](https://chromedriver.chromium.org/) and put it in the same directory. Make sure to download the version corresponding to your **Chrome browser version**.

  ![](https://i.imgur.com/UJbbVLi.gif)

   Alternatively, if you prefer **Firefox**, download **firefoxdriver.exe** through [this link](https://github.com/mozilla/geckodriver/releases)

  ![](https://i.imgur.com/8pQDfd6.gif)

  3. Run either the .exe or the .py file. Allow it through the *firewall* if needed.

  ![](https://i.imgur.com/gkfMz4x.gif)

## Usage
The script should ask you to provide your SC **Username** and **Password** at your first startup.
Don't worry, this is locally stored (in a hidden file, you can see the file by having privileges though). It's intention is to avoid providing the details every time you wanna run the program.

![](https://i.imgur.com/PqwCXVq.gif)

Now I *really* don't want the file to be messed up with, but for the sake of full disclosure, your information, along with information about the amount of events/ giveaways viewed is stored in a file called **User-Settings.txt**, in *plain text format*, in your own system, in the *same* directory, with a *hidden* attribute.

If you tamper with the file and the information fails sanity check, the file will be **instantly deleted** and the program will start from *scratch*. It's pretty unforgiving about this...

On the bright side, you can use this on your advantage if you wanna *switch accounts*, just **delete** this file and you can enter your Username and Password again!

![](https://i.imgur.com/G8fKKvO.gif)

After the initial setup, the script will do all the tasks one by one, give it time if it's the first startup, it'll let you know when it's finished.

![]()

## Optimization Concerns
For **General webpage** visits:

The *speed* of script is heavily tied with the **user's internet speed**. The script doesn't use any loops that can go indefinitely and all of these loops have a complexity of O(n), so really, the script is only gonna take time on the *wait intervals* (Waiting for the page to load).

These wait intervals are set *manually* by me, and their upper limit is **10 (seconds) for standard wait** and **30 (seconds) for extended wait**. If the page takes longer than this to load any required element, the script will throw a **request timed out** and exit. This *should* be no problem for most people because I, myself, have third world cheap internet speeds and it works fine for me.

For **Events** and **Giveaways**:

The script starts of from scratch as having no **Events** or **Giveaways** viewed at all.

From where, it starts viewing the **Events**, it will always view every single event in the first go, if ran without *errors*. It'll try to *share* as long as the sharelimit has not been reached (3 each day). It'll also *add every single event to the calender* at the first go.

This is the same for **Giveaways** too, except since the script only has to *view* the giveaways, it will never have to *visit the specific Giveaway pages* after the first go (unless a new one is added). So, all the work is done in the first go.

What all of this means that, after the *first go*, the script will only enter the **Event pages** that have not yet been *shared* (according to the program) and try to share them. For giveaways, it won't even enter the **specific Giveaway pages** after the first go. So most of the heavy lifting is done in the first go, and unless *new events/giveaways* are added, there's barely any work the script will have to do in these sections.

For **Discord Widget**:

This is probably the one most of the problems *might* arise from. The **discord widget loading** is *weird, unpredictable and slow*. So it really depends on the internet connection of the user. Now I'll address these concerns on the **Error Guide** of this README but I'll briefly mention that the **wait** set for the discord widget in the script is *quite long* already. So it should *mostly* be fine for good internet connections.

## Error Guide
The program has a built in **error handler**, I'd like to think that it'll cover all the exceptions but I can't really be sure without people actually testing it out. Here's the list of their **codes**, along with what *you should do* about them!

The errors contain a *code* and an *optional message*, here's a picture to help you find both of them!

![](https://i.imgur.com/sjHD4Dk.png)

  1. **Code 1**: *Request Timed Out*. This means the page or an element on it took too long to load, the accompanying message should tell you which task the script was performing when this happened. All you can do about this is wait and try again later.

  2. **Code 2**: *Invalid Credentials*. This means your the sign in attempt failed. So either your **internet connection** heavily slowed down or your *Username and Password* was incorrect.

  3. **Code 3**: *Discord widget took too long to respond*. This is a weird issue, the discord widget takes a while to load and the program just won't wait that long, I could make it wait that long, but that's counterproductive.
  If you get this issue, give it at least one more try, sometimes this error can be thrown only on the first startup but not the consequent one.

  4. **Code 4**: *An unexpected error occurred, make sure that **chromedriver**/**geckodriver** is present in the same directory*. This happens when the *initial browser creation* fails. This happens most often when chromedriver.exe/geckodriver.exe is NOT present in the *same directory as the script* and/or **chromium (chrome)**/**Firefox** is not installed on your PC. You should also check whether your **chromedriver version**/**geckodriver version** is the same as your **Chrome version**/**Firefox Version**.

  5. **Code 5**: *User-Settings.txt Sanity check failed, please try again later*. This happens when the information about events present in **User-Settings.txt** is either *incorrect* (i.e not numbers) or *not present*. This will instantly delete the file and ask you for your **Username and Password** again. This is why I advice not to tamper with the file itself. *(Unless you just wanna straight up delete it)*

# Troubleshooting
Please make sure you have chromedriver/geckodriver in the same directory along with chromium (chrome)/Firefox installed on your computer. Also make sure to allow the program through firewall for it to access the internet.

  * *The program is stuck at "Visting X" and won't continue*:-

      The console might just have lost focus, press enter on it and see if it works, there really aren't any loops that can possibly go infinitely long so if the program encounters something wrong, it'll just throw an exception and exit, not run for eternity.
  * *I get weird ERROR(#numbers)/INFO(#numbers) but the program doesn't close*:-

  ![](https://i.imgur.com/eccT32K.png)

   You might encounter some common error codes that have to do with selenium and how the underlying chromium source code works. Some info will also pop up when the script clicks on share and when the script opens the javascript heavy discord widget. Don't worry, it's nothing serious until the program itself throws any of the Error codes mentioned in the **Error Guide** section.
  * *I get error X*:-

    Refer to the **Error Guide** section.
  * *The program says my credentials are wrong even though I'm sure they are right*:-

    This either means your **connection timed out** or your password contains *special* special characters. (yeah)

    Make sure your password doesn't contain escapable characters like `/`, `\`, `"`, `'`. It's fine if it has `@`, `_` or `-` but if it has any escapable characters, I'm sorry to say, this script won't support that, yet.

    If you do use such a password, let me know, I might try to implement something. *(no it doesn't include you telling me your password)*
