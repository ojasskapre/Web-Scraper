from book_details_scraper import get_book_details
from book_details_elasticsearch import store_book_details

search_book = str(input('Enter the book to be searched:\n'))  # type: str
book_lists = get_book_details(search_book)  # type: list
book_dict = {}

for items in book_lists:
    book_dict.update({items[0]: {'author': items[1], 'publication_date': items[2], 'price': items[3]}})
print(book_dict)

store_book_details(search_book, book_dict)