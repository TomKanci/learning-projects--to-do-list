import requests
from bs4 import BeautifulSoup

# Replace the URL with the webpage you want to extract the IDs from
url = "http://127.0.0.1:5000"

# Send a GET request to the URL and store the response
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all elements with the class "draggable" and extract their IDs
myarray = [element["id"] for element in soup.find_all(class_="draggable")]

print(myarray)