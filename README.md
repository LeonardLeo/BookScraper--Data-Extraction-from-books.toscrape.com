# Book Data Scraper Bot

## Overview

The Book Data Scraper Bot is a Python-based web scraping tool designed to extract book data from the [Books to Scrape](https://books.toscrape.com/) website. It automates the process of gathering book information, including title, rating, price, UPC, availability, quantity available, category, and more, and organizes the data into a structured format for further analysis and use.


## Features

- **Web Scraping:** Utilizes web scraping techniques with BeautifulSoup and requests modules to extract book data from the Books to Scrape website.
- **Data Organization:** Structures the scraped book data into a pandas DataFrame, facilitating easy manipulation, analysis, and exportation to various formats such as CSV files.
- **Category Flexibility:** Dynamically iterates through different book categories and handles multi-page categories, ensuring comprehensive data collection even with website updates.
- **Automation:** Automates the data collection process, allowing for scheduled scraping at predefined intervals, reducing manual effort and ensuring up-to-date datasets.


## Installation

1. Clone the repository to your local machine:
git clone [repository-url](https://github.com/LeonardLeo/BookScraper--Data-Extraction-from-books.toscrape.com)
2. Run the main script to start scraping book data:
`python scraper_bot.py`


## Usage

1. Upon running the script, the Book Data Scraper Bot will begin scraping book data from the Books to Scrape website.
2. The bot will iterate through different book categories and pages, collecting information for each book.
3. Once scraping is complete, the bot will save the data as a CSV file in the `generated_data` folder.


## Documentation

For a detailed breakdown of the project's algorithm, functions, and usage, refer to the provided Jupyter Notebook (`scraping_books_from_books.toscrape.com_notebook.ipynb`). The notebook provides comprehensive documentation and insights into the scraping process and code implementation.


## Contributions

Contributions to the project are welcome! If you encounter any issues, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.


## License

This project is licensed under the MIT license.
