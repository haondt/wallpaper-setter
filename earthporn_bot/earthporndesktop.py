import praw, urllib.request, os, ctypes


def main():


    subreddit = "wallpapers" # sub to get images from
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(subreddit)

    # scrape the top post from the last 24 hrs
    for submission in subreddit.top(time_filter="day", limit=5): # check the top 5 incase top post isn't an image
        url = submission.url
        if is_image(url):
            path = download_image(url)
            set_wallpaper(path)
            break


# given a link to an image, downloads the image to the given directory
def download_image(link):

    working_directory = "C:/~PATH~/earthporn_bot/wallpapers/" # Edit this to the location of the bot file
    found = False
    i = 0
    while not found:
        if os.path.isfile(working_directory + "image_" + str(i) + ".jpg"):
            i += 1
        else:
            found = True

    image_location = working_directory + "image_" + str(i) + ".jpg"
    urllib.request.urlretrieve(link, image_location)
    return image_location

# checks a url to see if it links to an image
def is_image(url):
    image_suffixes = [
        ".jpg",
        ".png"
    ]
    image_prefixes = [
        "i.imgur",
        "i.redd.it",
        "imgur.com"
    ]
    image_suffixes = "\t".join(image_suffixes)
    image_prefixes = "\t".join(image_prefixes)

    return url[len(url) - 4:] in image_suffixes or url.split("/")[2] in image_prefixes


def set_wallpaper(image_path):

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


main()