# -*- coding: utf-8 -*-
"""
Creating a scraping bot that gets book data from https://books.toscrape.com/
Please refer to notebook for an even better breadown of the steps and process
for all questions answered.

ALGORITHM BEHIND THE CREATION OF THE BOT.
-----------------------------------------
We are given a webpage https://books.toscrape.com/ to scrape all books on 
the page.
A brief idea on the best solution. The page has different categories outlined 
on the left side of each page.

A good solution will be to assume we know the number of pages the webpage has
and then we iterate through each page and scrape all we see.

An excellent solution will be understanding we can't control changes to the 
website however, we can handle some possible issues. One such issue is not 
assuming the number of pages the webpage has. Instead, we find the categories
section of each book, and iterate through. This way, if new categories are 
added, we still scrape the data thats exists.

Steps:
    1) Create a function that scrapes and gets HTML tags as objects
    2) Create a function that stores book information. This function utilizes 
    the function that scrapes and gets HTML tags as objects
    3) Create a function that stores the dataset
    4) Create a function that iterates through pages and stores the data as a 
    dataframe. This function makes uses of all the other defined function, 
    combining all of them to create our scraping bot
"""

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Title
# 2. Rating
# 3. Price
# 4. Stock availability (Boolean)
# 5. UPC
# 6. Quantity available 
# 7. Category

def get_info_internal_links(address: str, tag: str, class_: str = None):
    """
    This function scrapes the html tags from the web address and creates an 
    instance of the beautiful soup library using the data scraped and the 
    'html.parser' to parse the data.

    Parameters
    ----------
    address : str
        The website to scrape the data.
    tag : str
        HTML tag for the container where the books are.
    class_ : str, optional
        The class associated with the HTML tag. The default is None.

    Returns
    -------
    info : Tag Object
        HTML tags associated with the request.

    """
    scraper = requests.get(address, timeout = 10)
    response = scraper.text
    
    soup = BeautifulSoup(response, "html.parser")
    info = soup.find(tag, class_ = class_)
    return info

def get_books_into_dataset(container_books, books) -> list:
    """
    Store all the data collected from each page into a list of lists. Uses the 
    get_info_internal_links function to scrape data for each category that has 
    extra pages with information we need.
    
    Parameters
    ----------
    container_books : Tag Object
        The HTML tag container where all the books on that page are stored.
    books : Tag Object
        The HTML tag container where all single book are stored.

    Returns
    -------
    store : list
        A list that lists the information of each book as a single row.

    """
    store = []
    for each_book in books:
        book_title = each_book.h3.a["title"]
        book_rating = each_book.p.attrs["class"][1]
        book_price = each_book.find("p", class_ ="price_color").text.replace("Â£", '')
        info_address = each_book.find("h3").a["href"].replace("../../../", "https://books.toscrape.com/catalogue/")
        
        get_upc = get_info_internal_links(address = info_address, 
                                          tag = "table", 
                                          class_ ="table table-striped")
        book_upc = get_upc.find("td").text
        
        book_in_stock = each_book.find("p", class_ ="instock availability").text.strip()
        
        get_quantity_available = get_info_internal_links(address = info_address, 
                                                         tag = "p", 
                                                         class_ ="instock availability")
        book_quantity_available = get_quantity_available.text.strip().replace("In stock (", "").split()[0]
        
        book_category = container_books.find("h1").text
        book_more_info = each_book.find("h3").a["href"].replace("../../../", "https://books.toscrape.com/catalogue/")
        store.append([book_title, 
                      book_rating, 
                      book_price, 
                      book_upc, 
                      book_in_stock,
                      book_quantity_available,
                      book_category, 
                      book_more_info])
    return store

def save_scraped_data(dataset: pd.DataFrame):
    """
    Save the data to the generated_data folder.

    Parameters
    ----------
    dataset : pd.DataFrame
        Dataset containing the scraped data.

    Returns
    -------
    None.

    """
    try:
        data_name = "scraped_books_data" 
        date = time.strftime("%Y-%m-%d")
        dataset.to_csv(f"../../generated_data/{data_name}_{date}.csv", index = False)
        print("\nSuccessfully saved file to the specified folder ---> generated_data folder.")
    except FileNotFoundError:
        print("\nFailed to save file to the specified folder ---> generated_data folder.")

def iterate_through_pages() -> pd.DataFrame:
    """
    Scrape the data from https://books.toscrape.com/ by combining all the 
    functions created:
        a) get_info_internal_links -> To get the webpage and parse it.
        b) get_books_into_dataset -> Gets the book data from the parsed data 
    and stores it.
        c) save_scraped_data -> Save the data to the generated_data folder.

    Returns
    -------
    dataset : pd.DataFrame
        A dataframe containing the scraped books data from all pages on the 
        https://books.toscrape.com/ web page.

    """
    # Get the dataset
    dataset = pd.DataFrame(columns = ["Title", 
                                      "Rating", 
                                      "Price", 
                                      "UPC", 
                                      "Availability", 
                                      "Quantity_Available", 
                                      "Category", 
                                      "More_Info"])
    
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    # Get all categories
    box = get_info_internal_links(address = url, 
                                  tag = "ul", 
                                  class_ = "nav nav-list").li
    column_box = box.find_all("li")
    # Categories and their index
    columns = [column.text.lower().strip().replace(" ", '-') for column in column_box]
    index = list(range(2, len(columns) + 2))
    
    print("""Now iterating through pages to scrape data...
          \n    TRUE: Categories with next page.
          \n    FALSE: Categories with one page.\n""")
    
    # Looping through each category and index to open up each webpage to be scraped
    for category, index in zip(columns, index):
        url1 = f"https://books.toscrape.com/catalogue/category/books/{category}_{index}/index.html"
        
        container_books = get_info_internal_links(address = url1, tag = "div", class_ = "col-sm-8 col-md-9")
        books = container_books.find_all("li", class_ ="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        print(f"{category}{index} -->", container_books.find("li", class_ = "current") is None)
        
        # Condition for how to iterate through categories with multi-pages and store the scraped book data
        # All categories with multiple pages have a class called "current"
        # In our condition, we check that that class exist and specify how to proceed if so
        if container_books.find("li", class_ = "current") is None:
            store = get_books_into_dataset(container_books, books)
            data = pd.DataFrame(store, columns = ["Title", 
                                                  "Rating",
                                                  "Price", 
                                                  "UPC", 
                                                  "Availability", 
                                                  "Quantity_Available", 
                                                  "Category", 
                                                  "More_Info"])
            dataset = pd.concat([dataset, data])
            
        elif container_books.find("li", class_ = "current") is not None:
            page_number = container_books.find("li", class_ = "current").text.split()[-1]
            page_number = int(page_number)
            for page in range(1, (page_number + 1)):
                url2 = f"https://books.toscrape.com/catalogue/category/books/{category}_{index}/page-{page}.html"
                container_books = get_info_internal_links(address = url2, tag = "div", class_ = "col-sm-8 col-md-9")
                books = container_books.find_all("li", class_ ="col-xs-6 col-sm-4 col-md-3 col-lg-3")
                
                store = get_books_into_dataset(container_books, books)
                data = pd.DataFrame(store, 
                                    columns = ["Title", 
                                               "Rating",
                                               "Price", 
                                               "UPC", 
                                               "Availability", 
                                               "Quantity_Available", 
                                               "Category", 
                                               "More_Info"])
                dataset = pd.concat([dataset, data])
        
        else:
            print("No class called 'current'.")
            break
    
    # Save dataset to folder
    save_scraped_data(dataset)
    
    return dataset

# Program Starts
if __name__ == "__main__":
    while True:
        dataframe = iterate_through_pages()
        print("\n\nNext scraping will be done in 2 hours.\nPlease wait...")
        # Time initialized in our program to solve some of the problems with web scraping
        # We don't want to be detected as a bot so specifying a delay helps our activity seem normal on the webpage
        time.sleep(7200)
        