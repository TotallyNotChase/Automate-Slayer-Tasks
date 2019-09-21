# A Slayer's Club browser for the lazy (or the busy)
This is a fairly simple script written in python, using selenium, to automate *daily tasks* on the **Slayer's Club** for **DOOM** by *iD software*.
The *source code* is included with a fair bit of *comments and documentation* right here, for everyone to see, as well!

## Features
The script does the following things upon launch, in this order.
  1. Visits **forum**
  2. Visits **Events** page, where it *views*, *shares* and *adds the events to calender*
  3. Visits **Giveaways** page, where it *views* the giveaways.
  4. Visits **Discord** through the widget.

## Installation
This should work on **Windows**, that is confirmed, it should also work in **Linux**, though I'm not entirely sure and would appreciate if someone could confirm.

All you need to do is
  1. Download this *repo*
  2. Download **chromedriver.exe** through [this link](https://chromedriver.chromium.org/) and put it in the same directory
  3. Run either the .exe or the .py file

## Usage
The script should ask you to provide your SC **Username** and **Password** at your first startup.
Don't worry, this is locally stored (in a hidden file, you can see the file by having privileges though). It's intention is to avoid providing the details every time you wanna run the program.

Now I *really* don't want the file to be messed up with, but for the sake of full disclosure, the file your information, along with information about the amount of events/ giveaways viewed is stored in a file called **User-Settings.txt**, in *plain text format*, in your own system, in the *same* directory, with a *hidden* attribute.

If you tamper with the file and the information fails sanity check, the file will be **instantly deleted** and the program will start from *scratch*. It's pretty unforgiving about this...

On the bright side, you can use this on your advantage if you wanna *switch accounts*, just **delete** this file and you can enter your Username and Password again!

Afterwards, the script will do all the tasks one by one, give it time if it's the first startup, it'll let you know when it's finished.

## Optimization Concerns
For **General webpage** visits:

Generally, every crucial webpage is opened in a new window with the root list/homepage as the mainwindow. For stuff like **Forum pages**, where you really just need to *visit it* and not much else, the script will wait until the page is loaded and then it'll immediately close the window.

For **Events** and **Giveaways**:

The script starts of from scratch as having no **Events** or **Giveaways** viewed at all.

From where, it starts viewing the **Events**, it will always view every single event in the first go, if ran without *errors*. It'll try to *share* as long as the sharelimit has not been reached (3 each day). It'll also *add every single event to the calender* at the first go.

This is the same for **Giveaways** too, except since the script only has to *view* the giveaways, it will never have to *visit the specific Giveaway pages* after the first go (unless a new one is added). So, all the work is done in the first go.

What all of this means that, after the *first go*, the script will only enter the **Event pages** that have not yet been *shared* (according to the program) and try to share them. For giveaways, it won't even enter the **specific Giveaway pages** after the first go. So most of the heavy lifting is done in the first go, and unless *new events/giveaways* are added, there's barely any work the script will have to do in these sections.

For **Discord Widget**:

This is probably the one most of the problems *might* arise from. The **discord widget loading** is *weird, unpredictable and slow*. So it really depends on the internet connection of the user. Now I'll address these concerns on the **Error Guide** of this README but I'll briefly mention that the **wait** set for the discord widget in the script is *quite long* already. So it should *mostly* be fine for good internet connections.

# Troubleshooting
Please make sure you have chromedriver in the same directory along with chromium (chrome) installed on your computer. Also make sure to allow the program through firewall for it to access the internet.
  * *The program is stuck at "Visting X" and won't continue*:-

      The console might just have lost focus, press enter on it and see if it works, there really aren't any loops that can possibly go infinitely long so if the program encounters something wrong, it'll just throw an exception and exit, not run for eternity.
  * *I get weird errors but the program doesn't close*:-

    You might encounter some common error codes that have to do with selenium and how the underlying chromium source code works, don't worry, it's nothing serious until the program itself throws any of the Error codes mentioned in the **Error Guide** section.
  * *I get error X*:-

    Refer to the **Error Guide** section.
