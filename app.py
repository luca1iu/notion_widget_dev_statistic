from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)


def get_posts_response_data(api_key):
    # URL of the API endpoint
    url = "https://dev.to/api/articles/me/published?per_page=1000"

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
        'per_page': '1000'
    }

    # Send GET request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        response_data = response.json()
        return response_data
    else:
        # If request was unsuccessful, print error message
        print("Error:", response.text)


def get_followers(api_key):
    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    followers = 0
    page_number = 1

    # Loop until we reach the last page of followers
    while True:
        params = {
            "per_page": 1000,  # Number of followers per page (default is 80)
            "page": page_number
        }
        res = requests.get(url='https://dev.to/api/followers/users', headers=headers, params=params)
        response_data = res.json()
        current_page_followers = len(response_data)
        followers += current_page_followers

        # Check if the current page has no followers, indicating it's the last page
        if current_page_followers == 0:
            break

        # Move to the next page
        page_number += 1

    return followers


def get_articles(api_key):
    response = get_posts_response_data(api_key)
    articles = response

    # Calculate total counts
    total_articles = len(articles)
    total_comments = sum(article["comments_count"] for article in articles)
    total_public_reactions = sum(article["public_reactions_count"] for article in articles)
    total_page_views = sum(article["page_views_count"] for article in articles)

    return total_articles, total_comments, total_public_reactions, total_page_views


@app.route('/api/<api_key>', methods=['GET'])
def get_dev_info(api_key):
    followers = get_followers(api_key)
    total_articles, total_comments, total_public_reactions, total_page_views = get_articles(api_key)

    return render_template('home.html', followers=followers, total_articles=total_articles,
                           total_comments=total_comments, total_public_reactions=total_public_reactions,
                           total_page_views=total_page_views)


if __name__ == '__main__':
    app.run(port=5000)
