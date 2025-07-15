import praw
import os

# Create Reddit instance with your credentials
reddit = praw.Reddit(
    client_id="HudZSfjC8qOD9xL-FwdNjQ",
    client_secret="93H-73__fl4Hsd1ppOgj8IrBRcMY-g",
    user_agent="user_persona_script"
)

def scrape_user_data(username, limit=50):
    user = reddit.redditor(username)

    posts = []
    comments = []

    try:
        for submission in user.submissions.new(limit=limit):
            posts.append(f"Title: {submission.title}\nBody: {submission.selftext}")
        
        for comment in user.comments.new(limit=limit):
            comments.append(f"Comment: {comment.body}")
    except Exception as e:
        print(f"Error scraping user {username}: {e}")
    
    return posts, comments

def save_raw_data(username, posts, comments):
    folder = f"data/{username}"
    os.makedirs(folder, exist_ok=True)

    with open(f"{folder}/posts.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(posts))
    
    with open(f"{folder}/comments.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(comments))

if __name__ == "__main__":
    reddit_url = input("Enter Reddit profile URL: ").strip()
    username = reddit_url.rstrip("/").split("/")[-1]

    posts, comments = scrape_user_data(username)
    save_raw_data(username, posts, comments)

    print(f"Scraped and saved data for {username}.")
