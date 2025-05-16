

![image](https://github.com/user-attachments/assets/35d9aadc-3df5-4a4e-94cd-a3e4a000cdf6)





💬 Quotes to Scrape - Web Scraping Project with Scrapy and MongoDB <br />
This project uses Scrapy to collect quotes from the website Quotes to Scrape. After the data is extracted, it goes through a basic processing stage and is then saved into a MongoDB database for storage and further use.

🔧 Technologies Used:
Python

Scrapy

MongoDB


📌 Features:
Extracts phrases, quotes, authors,urls, biography and associated tags.

Handles pagination to collect all available data.

Cleans and structures the data before saving.

Stores the data in a MongoDB collection.

📁 Project Structure:
scrapy_project/: Contains the Scrapy spider and configuration.

items.py: Defines the data fields for quotes.

pipelines.py: Processes and inserts the data into MongoDB.

settings.py: Configures Scrapy behavior and MongoDB connection.

🚀 How to Run:
Clone the repository.

Make sure you have MongoDB running locally or provide the connection URI.

Install the required dependencies: pip install -r requirements.txt

Run the spider: scrapy crawl quotes
