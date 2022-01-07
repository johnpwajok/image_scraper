# Library imports
from selenium import webdriver
# By allows search by HTML property
from selenium.webdriver.common.by import By
import requests
import io
import os
import time
from PIL import Image

###############################################
###############################################
# path to chromedriver executable, different driver needed for each browser
PATH = "/Users/johnpwajok/Downloads/chromedriver"

# set webdriver to use Chromedriver
wd = webdriver.Chrome(PATH)


# function to find image URL's on Google, arguments: webdriver, delay (seconds), max_images: number of images to fetch, key_word: search term
def get_images_from_google(wd, delay, max_images, key_word):
    # Continue to scroll to bottom of chrome image search page
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    # The Chrome url of the image search (based on key_word)
    default_google_image_search_URL = "https://www.google.com/search?tbm=isch&q="
    url = default_google_image_search_URL + key_word
    wd.get(url)

    # List to store image URL's
    image_URLS = set()
    # hops if duplicate | need to increase the max_images if duplicate found to allow script to go to next image
    hops = 0

    while len(image_URLS) + hops < max_images:
        print("\nFetching image URL's...\n")
        scroll_down(wd)
        # classname for thumbnails in Google image search
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_URLS) + hops:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            # n3VNCb = classname of actual image, rather than the thumbnail
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                # if the image is valid | has a source tag and has http contained in the source tag
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    # skip to next image if the current image is already in the list
                    if image.get_attribute('src') in image_URLS:
                        max_images += 1
                        hops += 1
                        break
                    else:
                        # Add the image to the list
                        image_URLS.add(image.get_attribute('src'))
                        print(f"Found {len(image_URLS)}")
    # return the list of image URL's
    return image_URLS


# Function to download images
def download_image(download_path, url, file_name):
    try:
        file_path = download_path + file_name
        #check if the download directory exists / create if it doesn't:
        if not os.path.exists(os.path.dirname(download_path)):
            try:
                os.makedirs(os.path.dirname(download_path))
                
            except Exception as e:
                print("The download directory cannot be created!  - ", e)

        #save the image
        with open(file_path, "wb") as f:
            try:
                image_content = requests.get(url, stream=True).content
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file)
                #Save the image
                image.save(f, "JPEG")
                print("Download success...")
            except Exception as e:
                #if the image is RGBA or PNG, need to convert it to RGB to be able to save as jpg
                s = str(e)
                rgb_string = "RGBA"
                png_string = "cannot write mode P as JPEG"
                if rgb_string or png_string in s:
                    with open(file_path, "wb") as f:
                        image_content = requests.get(url, stream=True).content
                        image_file = io.BytesIO(image_content)
                        image = Image.open(image_file)
                        print("\nConverting RGBA image...\n")
                        #convert to 'RGB'
                        image = image.convert('RGB')
                        image.save(f, "JPEG")
                        print("\nRGBA Image Conversion complete!\n")
                        print("Download success...")
                        #image.save(f, "JPEG")
                        #print("Download success...")
                        #im = Image.open("audacious.png")
                        #rgb_im = im.convert('RGB')
                        #rgb_im.save('audacious.jpg')
                else:
                    print("Download Failed!!  - ", e)
    except Exception as e:
        print("Download Failed!!  - ", e)


#download_image("", imageURL, "test.jpg")
search_term = input("What images would you like to download? \n")
download_limit = int(input("\nHow many images do you want to download? \n"))
#get list of image url's 
urls = get_images_from_google(wd, 0.5, download_limit, search_term)
print("\nBeginning download...")
#download the images from the urls list to a new directory called 'imageFolder'
for i, url in enumerate(urls):
    download_image(
        "imageFolder/", url, str(i) + ".jpg")
print("\nDownload complete!")

wd.quit()
