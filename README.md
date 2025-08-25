Small project I did for learning how to webscrape using python + mongodb. <br />
Mainly followed John Watson Rooney's tutorial on YouTube. Title: Try this Web Scraping Project with Mongodb (Code Along). <br />

## Website Used
- [Fully Booked](https://fullybookedonline.com)  
- Specific page: [Fave Reads under PHP 800](https://fullybookedonline.com/collections/featured-collections/fave-reads-under-php800.html)

## What the Program Does
- Sends requests to Fully Booked's GraphQL API  
- Extracts book details (title, author, price, description)  
- Handles pagination to collect all items  
- Saves the results in a MongoDB database

## Setup
1. In the web page of your choice inspect the website using devtools (Ctrl+Shift+I).  
2. Go to the "Network" tab and press the "Reload Page" button. 
3. Look for requests that populate the webpage with information (JSON or GraphQL). 
- In my case it was https://fullybookedonline.com/graphql?hash=1142935139&sort_1={%22bestseller_rank%22:%22ASC%22}&filter_1={%22price%22:{},%22category_id%22:{%22eq%22:27202},%22customer_group_id%22:{%22eq%22:%220%22}}&pageSize_1=24&currentPage_1=1&_currency=%22%22
4. Copy the link as cURL (bash)
5. Paste the copied link into curlconverter.com 

