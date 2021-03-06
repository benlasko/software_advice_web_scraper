# A Beautiful Soup web scraper to scrape all product pages at softwareadvice.com.

![alice](images/alice_in_software_land.png)

<br>

## Technologies Used

* Python
* Beautiful Soup
* Pandas
* Jupyter Notebook
* MongoDB

<br>

## Overview

### This project was completed for a small IT business and my task was to scrape all product pages at softwareadvice.com.  The script I wrote uses Beautiful Soup to gather the data listed below from each product page. The script was written so the data would be saved in a csv file which can then be put into a MongoDB database.

* Product name
* Product overview
* Average score
* Total reviews
* Total recommendations
* If product was ever a "FrontRunner"
* List of guides product has been featured in


<br>

## Data

###  Softwareadvice.com has descriptions, reviews, and other data about software in over 40 categories like Accounting, Business Intelligence, Human Resources, Learning Management Systems, Medical, and Supply Chain Management.  In each category is a number of subcategories and in each subcategory is a number of software products.  There's over 900 subcategory links total and up to hundreds of product page links for each subcategory.

<br>

#### Categories/Subcategories page
![categories page](images/categories_page.png)


<br>

#### Subcategory page example (Big Data with 102 product pages)
![subcategory page](images/subcategory_page.png)



<br>

#### Product page example 1
![subcategory page](images/product_page_1.png)

<br>

#### Product page example 2 
![subcategory page](images/product_page_2.png)

<br>

## Next Steps

### Next steps for this project would include letting the script gather more data from the product pages (like pricing data although the site doesn't seem to include much pricing data right on the product pages), applying some text cleaning techniques to the product overviews, and writing functions to scrape specified pages by category, subcategory or individual product.

<br>
