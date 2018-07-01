from bs4 import BeautifulSoup
import requests
import logging

book_list = []
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookFinder:
    def __init__(self, soup):
        self.soup = soup

    def no_book_found(self) -> None:
        for items in self.soup.findAll('', {'class': 'content'}):
            if items.string is None:
                print("No book found!!!!\n")
                exit(1)

    def get_book_name(self) -> None:
        book = []
        book_generator = (item for item in self.soup.findAll('', {'itemprop': 'name'})
                          if item.get('content') is not None)
        for name in book_generator:
            book.append(str(name.get('content')))
        book_list.append(book)

    def get_book_author(self) -> None:
        book = []
        book_generator = (item for item in self.soup.findAll('', {'itemprop': 'name'}) if item.string is not None)
        for author in book_generator:
            book.append(author.string)
        book_list.append(book)

    def get_publication_date(self) -> None:
        book = []
        book_generator = (item for item in self.soup.findAll('', {'itemprop': 'datePublished'}))
        for publication_date in book_generator:
            book.append(publication_date.string.strip())
        book_list.append(book)

    def get_book_price(self) -> None:
        original_price = []
        discount_price = []
        final_price = []
        book = []
        itr = 0
        book_generator = (item for item in self.soup.findAll('span', {'class': 'rrp'}))
        for price in book_generator:
            original_price.append(str(price.string)[3:])

        book_generator = (item for item in self.soup.findAll('p', {'class': 'price-save'}))
        for price in book_generator:
            discount_price.append(str(price.string.strip())[8:])

        for item in self.soup.findAll('p', {'class': 'price'}):
            if item.string is None:
                for iterator in range(0, len(original_price) - 1):
                    final_price.append(
                        'US$' + str(round(float(original_price[iterator]) - float(discount_price[iterator]), 2)))
                book.append(final_price[itr])
                itr = itr + 1
            else:
                book.append(item.string.strip())
        book_list.append(book)


def get_book_details(search_book: str) -> list:
        url = 'https://www.bookdepository.com/search?searchTerm={} &search=Find+book'.format(search_book)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        book_finder = BookFinder(soup)
        book_finder.no_book_found()
        book_finder.get_book_name()
        logging.info('book name')
        book_finder.get_book_author()
        logging.info('author name')
        book_finder.get_publication_date()
        logging.info('publication date')
        book_finder.get_book_price()
        logging.info('Price')
        return list(zip(book_list[0], book_list[1], book_list[2], book_list[3]))
