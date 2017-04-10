import praw, urllib.request, os, ctypes, sys


def main():


    subreddit = "earthporn" # sub to get images from

    if len(sys.argv) > 1:
        subreddit = sys.argv[1]

    print("Fetching wallpaper from r/" + subreddit + "...")

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(subreddit)

    # scrape the top post from the last 24 hrs
    print("Searching sub...")
    found_image = False
    for submission in subreddit.top(time_filter="day", limit=10): # check the top 10 incase top post isn't an image
        url = submission.url
        if is_image(url):
            print("Downloading image...")
            path = download_image(url)
            set_wallpaper(path)
            found_image = True
            break

    if not found_image:
        print("Couldn't find any images in the top 10 posts.")

# given a link to an image, downloads the image to the given directory
def download_image(link):

    working_directory = "C:/Users/noahb/OneDrive/Documents/Projects/earthporn_bot/wallpapers/"
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
    print("Setting Wallpaper...")
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


main()
