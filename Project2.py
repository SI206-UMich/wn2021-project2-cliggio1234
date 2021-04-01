#Your Name: Christina Liggio
#Your student id: 33453386
#Your Email: cliggio@umich.edu
#List who you worked with on this homework: Amanda Rudolph 
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    
    soup = BeautifulSoup(open('search_results.htm'), 'html.parser')
    books = []
    for b in soup.findAll('tr', itemtype = "http://schema.org/Book"):
        items = b.findAll('span', itemprop = 'name')
        t = items[0].string.strip()
        a = items[1].string.strip()
        books.append((t, a))
    return books

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    list_of_urls = []
    urls = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    resp = requests.get(urls)
    soup1 = BeautifulSoup(resp.text, 'html.parser')
    books = soup1.find_all('a', class_ = 'bookTitle', itemprop = 'url')
    for book in books:
        bk = book['href']
        if bk.startswith('/book/show/'):
            sites = 'https://www.goodreads.com' + str(bk)
            list_of_urls.append(sites)
    return list_of_urls[:10]




def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    t = soup2.find('h1', id = "bookTitle").string.strip()
    a = soup2.find('a', {'class': 'authorName'}).string.strip()
    pages = int(soup2.find('span', itemprop = "numberOfPages").string.strip(" pages"))
    return(t, a, pages)


    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    bestBooks = []
    with open(os.path.join(filepath, "best_books_2020.htm")) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        data = soup.find_all('div', class_ = 'category clearFix')
        for item in data:
            category = item.h4.text
            category = category.strip()
            title_a = item.find('div', class_ = "category__winnerImageContainer")
            title_b = title_a.find("img", alt = True)
            title_c = title_b['alt']
            url = item.find("a").get("href")
            tuplee = (category, title_c, url)
            bestBooks.append(tuplee)
    return bestBooks

    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w') as file:
        file.write('Book Title,Author Name\n')
        for l in data:
            file.write(','.join(l) + '\n')



def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        lst_of_title = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(lst_of_title), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(lst_of_title, list)
        # check that each item in the list is a tuple
        for title in lst_of_title:
            self.assertIsInstance(title,tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(lst_of_title[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)','J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(lst_of_title[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))
    
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)
    
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for sl in TestCases.search_urls:
            self.assertIsInstance(sl, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue(sl.startswith('https://www.goodreads.com/book/show/'))

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summary = get_book_summary(url)
            self.assertEqual(type(summary), tuple)
            summaries.append(summary)
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for item in summaries:
            self.assertEqual(type(item), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(item), 3)
            # check that the first two elements in the tuple are string
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(item[2], int)
            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2], 337)
     


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        dir = os.path.dirname(__file__)
        best_books = summarize_best_books(dir)
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)
            # assert each item in the list of best books is a tuple
        for book in best_books:
            self.assertIsInstance(book, tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(book), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0][0], 'Fiction')
        self.assertEqual(best_books[0][1], 'The Midnight Library')
        self.assertEqual(best_books[0][2], 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1][0], 'Picture Books')
        self.assertEqual(best_books[-1][1], 'Antiracist Baby')
        self.assertEqual(best_books[-1][2], 'https://www.goodreads.com/choiceawards/best-picture-books-2020')


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        dir = os.path.dirname(__file__)
        searchr = get_titles_from_search_results(dir)
        # call write csv on the variable you saved and 'test.csv'
        write_csv(searchr, "search_results.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        inFile = open(os.path.join(dir, "search_results.csv"), "r")
        liness = inFile.readlines()

        # check that there are 21 lines in the csv
        self.assertEqual(len(liness), 21)
        # check that the header row is correct
        self.assertEqual(liness[0].strip(), "Book Title,Author Name")
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(liness[1].strip(),'Harry Potter and the Deathly Hallows (Harry Potter, #7),J.K. Rowling')
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(liness[-1].strip(),'Harry Potter: The Prequel (Harry Potter, #0.5),J.K. Rowling' )


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



