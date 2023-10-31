import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import argparse
import base64
from selenium.webdriver.common.by import By
import math
from pathlib import Path

def main(search, amount):
    amount = int(amount)*2 #to deal with lil image searching optimization problems
    # Set up the download folder
    download_folder = "GetImages/"+search.replace(' ', '_')

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Function to download an image

    def download_image(url, folder):
        if url.startswith('data:image/jpeg'):
            try:
                # Extract the base64 data part of the URL
                data = url.split(',')[-1]
                img_data = base64.b64decode(data)

                # Convert the binary data to an image
                image = Image.open(BytesIO(img_data))

                #Changing from pallete mode to RGB if needed
                if image.mode == 'P':
                    image = image.convert('RGB')

                # Save the image to the specified folder
                file_path = os.path.join(folder, f"image_{math.ceil((i + 1)/2)}.jpg")
                image.save(file_path, "JPEG")

            except Exception as e:
                print(f"Error while downloading image {i + 1}: {e}")
        else:
            print(f"Skipping non-jpeg IMG")

    # Set up Selenium
    url = "https://www.google.com/imghp"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.get(url)

    # Locate the search bar and enter your search query
    search_box = driver.find_element( By.NAME, "q")
    search_box.send_keys(search)  # Replace with your search query
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Let the page load

    # Scroll down to load more images
    scroll_pause_time = 1
    scrolls = math.ceil(amount/10)
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find and download the first 10 images
    image_tags = soup.find(class_="islrc").find_all("img")
    for i, img in enumerate(image_tags[:amount]):
        img_url = img.get("src")
        if img_url:
            download_image(img_url, download_folder)
            print(f"Downloaded image {math.ceil((i + 1)/2)}")

    # Close the browser
    driver.quit()
    os.startfile(os.path.realpath(download_folder))

if __name__ == '__main__':
    try:
        # # Create an argument parser
        # parser = argparse.ArgumentParser(description="Google Images Scraper")
        # parser.add_argument("search_query", type=str, help="Type the image you want to search on Google Images")
        # parser.add_argument("amount", default=10, type=int, help='Type the amount of images you want to download')
        # # Parse the command-line arguments
        # args = parser.parse_args()

        search_query = input("Search the images you want to download: ")
        amount = int(input("Amount of images (default: 10): ") or 10)
        
        main(search_query, amount)
    except Exception as e:
        print(f"An error occurred: {e}")
