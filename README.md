# Aqira 
Scholarvox Scraper in Python3, written in roughly 2 days.

## Drawbacks and important notes

* The process is damn slow, it tooks roughly 1.45 hours to scrape 400 pages of a book, if you can wait this tool is for you .
* This works only on windows, however if i have the time for it, **MacOS and Linux support** will be comming soon.
* You may need to edit some parameters yourself, this is not a fully fledged scraper for the time being.

## Installation

Easy Steps:

```
git clone <this-repo>
pip install -r requirements.txt
python main.py
```

## Getting Started

* Open CMD or Powersheel in aqira's directory.
* Open `main.py` and add your Username and Password for Scholarvox Login.
* Type: `python main.py --help` to learn how to use the flags.
* Scrape and Enjoy!!

## Logs 

* This Script is only compatible with *Google Chrome*, maybe adding support for Firefox and other browsers. 
* ~~Setting your Parameters (Changing document link, MAX\_PAGES) is done for now in the source code `main.py`~~.
* Added parsing CLI flags, no need for source code modification (except for site credentials).
* Scholarvox is a trashy website, don't try to select by ids or classes, use XPATH to locate elements on the page.
* Chrome Options extensive list (Chromium C++ source code)
  - [List of common switches](/master/chrome/common/chrome_switches.cc)
  - [List of headless switches](/master/headless/app/headless_shell_switches.cc)
  - [To search other switches](https://source.chromium.org/search?q=file:switches.cc&ss=chromium%2Fchromium%2Fs)
  - [List of preferences](/master/chrome/common/pref_names.c)
