# pymage_downloader
Pymage_downloader is a cross-platform Python3 extensible tool that helps to download images and files from reddit posts.

Currently supports Deviantart, Imgur, Gfycat, Instagram, i.redd.it and directly linked files. Support for additional
sites can be easily added with plugins.

The script detects by default if a file has already been downloaded, and if so, skips it. (Although this can be overwritten.)

## Dependencies

*Only Python 3 is supported*
- PRAW 5.0.1
- Requests
- Re
- lxml
- BeautifulSoup4

All of which can be installed through `pip3 install praw requests re lxml beautifulsoup4`

## Prerequisites
In order to use it, the reddit API requires that you get a reddit client ID and a client secret, refer to
`https://github.com/reddit/reddit/wiki/OAuth2` for instructions on how to get authorization.

Once done, fill out the information in `src/praw.ini`. You also need to define a user-agent with your reddit username,
as indicated in the reddit API documentation.

## Usage

`pymage_downloader.py [options]`

### Options

> `-h, --help`

show this help message and exit

> `--subreddit, -s <subreddit>`

Specify the name of the subreddit. By default: *pics*

> `--period , -p <hour,day,week,month,year,all>`

  Period of time from which you want images. Only works
  for top and controversial listing. By default: *week*

> `--type, -t {hot,top,new,controversial}`

Type of listing of posts in a subreddit. By default fetches: *hot*

> `--limit, -l <N>`

Limits the number of reddit posts per query to the API. By default: *25*

> `--destination, -d FOLDER`

Defines a download folder. By default it creates a folder called: *reddit_pics*

> `--overwrite, -o`

Specifies if files should be overwritten if they were already downloaded. By default this is False.

> `--debug`

Activates debug mode.

### Examples

> `pymage_downloader.py -t top -p month -l 15 -s pics`

Downloads all of the images found in the top 15 posts of the month in the *pics* subreddit

> `pymage_downloader.py -t hot -p month -s aww --debug`

Downloads all of the images found in the hot posts in the *aww* subreddit. The period is ignored because it only works
for top and controversial posts.

