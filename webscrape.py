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


# function to find image URL's on Google, arguments: webdriver, delay (seconds), maxImages: number of images to fetch, keyWord: search term
def getImagesFromGoogle(wd, delay, maxImages, keyWord):
    # Continue to scroll to bottom of chrome image search page
    def scrollDown(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    # The Chrome url of the image search (based on keyword)
    defaultGoogleImageSearchURL = "https://www.google.com/search?tbm=isch&q="
    url = defaultGoogleImageSearchURL + keyWord
    wd.get(url)

    # List to store image URL's
    imageUrls = set()
    # skip if duplicate | need to increase the maxImages if duplicate found to allow script to jump to next image
    skips = 0

    while len(imageUrls) + skips < maxImages:
        print("\nFetching image URL's...\n")
        scrollDown(wd)
        # classname for thumbnails in Google image search
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(imageUrls) + skips:maxImages]:
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
                    if image.get_attribute('src') in imageUrls:
                        maxImages += 1
                        skips += 1
                        break
                    else:
                        # Add the image to the list
                        imageUrls.add(image.get_attribute('src'))
                        print(f"Found {len(imageUrls)}")
    # return the list of image URL's
    return imageUrls


# Function to download images
def downloadImage(downloadPath, url, fileName):
    try:
        filePath = downloadPath + fileName
        #check if the download directory exists / create if it doesn't:
        if not os.path.exists(os.path.dirname(downloadPath)):
            try:
                os.makedirs(os.path.dirname(downloadPath))
                
            except Exception as e:
                print("The download directory cannot be created!  - ", e)

        #save the image
        with open(filePath, "wb") as f:
            try:
                imageContent = requests.get(url, stream=True).content
                imageFile = io.BytesIO(imageContent)
                image = Image.open(imageFile)
                #Save the image
                image.save(f, "JPEG")
                print("Download success...")
            except Exception as e:
                s = str(e)
                rgbString = "RGBA"
                pngString = "cannot write mode P as JPEG"
                if rgbString or pngString in s:
                    with open(filePath, "wb") as f:
                        imageContent = requests.get(url, stream=True).content
                        imageFile = io.BytesIO(imageContent)
                        image = Image.open(imageFile)
                        print("\nConverting RGBA image...\n")
                        
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


#downloadImage("", imageURL, "test.jpg")
searchTerm = input("What images would you like to download? \n")
downloadLimit = int(input("\nHow many images do you want to download? \n"))
urls = getImagesFromGoogle(wd, 0.5, downloadLimit, searchTerm)
print("\nBeginning download...")
for i, url in enumerate(urls):
    downloadImage(
        "imageFolder/", url, str(i) + ".jpg")
print("\nDownload complete!")

wd.quit()
