import json
import re
from bs4 import BeautifulSoup

# Open and read the HTML file
with open("index2.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Create a list to store all the extracted reviews
reviews = []

# Iterate over all review containers (assuming each review is within a <div> with specific classes)
review_divs = soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")

for review_div in review_divs:
    reviewbody = ""
    # Extract the review body from nested <span>
    reviewbody_span = review_div.find("span")
    if reviewbody_span:
        reviewbody = reviewbody_span.get_text(strip=True)

    # Find the review date (assuming it has class "review-date")
    review_date = ""
    review_date_span = review_div.find_next("span", class_="a-size-base a-color-secondary review-date")
    if review_date_span:
        # Extract the full review date text
        full_review_date = review_date_span.get_text(strip=True)
        
        # Use a regular expression to extract only the date part (e.g., "February 14, 2024")
        date_match = re.search(r"on (.*)", full_review_date)
        if date_match:
            review_date = date_match.group(1)  # This will be the date part
    
    # Find the customer name (assuming it is within a <span> inside a <div> with class "a-profile-content")
    customer_name = ""
    customer_name_div = review_div.find_next("div", class_="a-profile-content")
    if customer_name_div:
        customer_name_span = customer_name_div.find("span", class_="a-profile-name")
        if customer_name_span:
            customer_name = customer_name_span.get_text(strip=True)

    # Find the rating (assuming it has class "a-icon-alt")
    rating = None
    rating_span = review_div.find_next("span", class_="a-icon-alt")
    if rating_span:
        rating_text = rating_span.get_text(strip=True)
        # Use regex to find the numeric part of the rating and convert to an integer
        rating_match = re.search(r"(\d+)", rating_text)
        if rating_match:
            rating = int(rating_match.group(1))  # Convert rating to an integer
    
    # Store the extracted data for this review
    reviews.append({
        "customer_name": customer_name,
        "review_date": review_date,
        "reviewbody": reviewbody,
        "rating": rating
    })

# Write the extracted reviews data to a JSON file
with open("data2.json", "w", encoding="utf-8") as json_file:
    json.dump(reviews, json_file, ensure_ascii=False, indent=4)

print("Data has been successfully extracted and written to data2.json.")
