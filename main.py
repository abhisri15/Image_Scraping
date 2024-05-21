import os
import requests
from bs4 import BeautifulSoup
import pymongo

# Directory to save images
save_dir = "images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Fake user agent to avoid getting blocked by Google
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Fetch the search results page
query = "bill gates"
response = requests.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch", headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
images_tags = soup.find_all('img')

# Remove the first image tag as it's usually not relevant
if images_tags:
    del images_tags[0]

img_data_mongo = []
for idx, img_tag in enumerate(images_tags):
    image_url = img_tag.get('src')

    # Skip if the image URL is not valid
    if not image_url or image_url.startswith('data:image'):
        continue

    try:
        image_data = requests.get(image_url).content
        myDict = {"index": image_url, "image": image_data}
        img_data_mongo.append(myDict)

        file_path = os.path.join(save_dir, f"{query}_{idx}.jpg")
        with open(file_path, "wb") as f:
            f.write(image_data)

    except Exception as e:
        print(f"Failed to process image {idx}: {e}")



