from bs4 import BeautifulSoup
import requests

book_list = []


def no_book_found(soup: BeautifulSoup) -> None:
    for items in soup.findAll('', {'class': 'content'}):
        if items.string is None:
            print("No book found!!!!\n")
            exit(1)


def get_book_name(soup: BeautifulSoup) -> None:
    book = []
    gen = (item for item in soup.findAll('', {'itemprop': 'name'}) if item.get('content') is not None)
    for name in gen:
        book.append(str(name.get('content')))
    book_list.append(book)


def get_book_author(soup: BeautifulSoup) -> None:
    book = []
    gen = (item for item in soup.findAll('', {'itemprop': 'name'}) if item.string is not None)
    for author in gen:
        book.append(author.string)
    book_list.append(book)


def get_publication_date(soup: BeautifulSoup) -> None:
    book = []
    gen = (item for item in soup.findAll('', {'itemprop': 'datePublished'}))
    for publication_date in gen:
        book.append(publication_date.string.strip())
    book_list.append(book)


def get_book_price(soup: BeautifulSoup) -> None:
    original_price = []
    discount_price = []
    final_price = []
    book = []
    itr = 0
    gen = (item for item in soup.findAll('span', {'class': 'rrp'}))
    for price in gen:
        original_price.append(str(price.string)[3:])

    gen = (item for item in soup.findAll('p', {'class': 'price-save'}))
    for price in gen:
        discount_price.append(str(price.string.strip())[8:])

    for item in soup.findAll('p', {'class': 'price'}):
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
    no_book_found(soup)
    get_book_name(soup)
    get_book_author(soup)
    get_publication_date(soup)
    get_book_price(soup)
    return list(zip(book_list[0], book_list[1], book_list[2], book_list[3]))
