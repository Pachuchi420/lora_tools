import praw
import requests
import os

# Create a Reddit instance
reddit = praw.Reddit(
    client_id='LHQMBQpEXykhqeXUoUOliA',
    client_secret='zz34UEErEEvs_X4zjl6yb5rEMxXXvw',
    user_agent='/u/RyuNeko932000'
)


# Prompt user to choose subreddit
subreddit_name = input("Enter subreddit to download images from: ")

# Retrieve the top posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
top_posts = subreddit.top(limit=None)

# Prompt the user to select a destination folder
destination_folder = input("Enter the destination folder path: ")
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)


# Download the images
for post in top_posts:
    if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        image_url = post.url
        image_data = requests.get(image_url, stream=True).content
        file_name = f'{post.id}.jpg'  # You can modify the file name as needed
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        print(f'Downloaded: {file_name} -> {file_path}')
