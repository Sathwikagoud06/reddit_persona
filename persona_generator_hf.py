import os
from transformers import pipeline, set_seed

# Load lightweight LLM from Hugging Face
generator = pipeline("text-generation", model="distilgpt2")
set_seed(42)

def read_user_data(username):
    post_path = f"data/{username}/posts.txt"
    comment_path = f"data/{username}/comments.txt"

    if not os.path.exists(post_path) or not os.path.exists(comment_path):
        print(f"❌ Missing files for {username}")
        return None

    with open(post_path, "r", encoding="utf-8") as f:
        posts = f.read()
    with open(comment_path, "r", encoding="utf-8") as f:
        comments = f.read()

    return posts, comments

def generate_persona(posts, comments):
    prompt = f"""
Based on the following Reddit posts and comments, describe a user persona including traits like interests, tone, habits, profession (if any), and any personality insights. Cite quotes from the content to support the analysis.

--- POSTS ---
{posts[:2000]}

--- COMMENTS ---
{comments[:2000]}

Persona Summary:
"""
    output = generator(
        prompt,
        max_new_tokens=150,
        num_return_sequences=1,
        truncation=True,
        pad_token_id=50256  # Prevents warning for GPT2 model
    )[0]['generated_text']
    return output

def save_persona(username, persona_text):
    os.makedirs("output", exist_ok=True)
    output_path = f"output/{username}_persona.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona saved: {output_path}")

if __name__ == "__main__":
    reddit_url = input("Enter Reddit profile URL: ").strip()
    username = reddit_url.rstrip("/").split("/")[-1]

    result = read_user_data(username)
    if result:
        posts, comments = result
        print(f"Generating persona for {username}...")
        persona = generate_persona(posts, comments)
        save_persona(username, persona)
