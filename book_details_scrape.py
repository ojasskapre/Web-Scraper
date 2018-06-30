from bs4 import BeautifulSoup
import requests as rq

search_book = str(input('Enter the book to be searched:\n'))
url = 'https://www.bookdepository.com/search?searchTerm='+search_book+'&search=Find+book'
books = str(input('Enter the file to save the data:\n'))
file = open(books+".txt",'w+')
response = rq.get(url)

book_list = []
book = []
soup = BeautifulSoup(response.content, 'html.parser')

for items in soup.findAll('',{'class':'content'}):
    if items.string==None:
        file.write("No book found!!!!\n")
        print("No book found!!!!\n")
        exit(1)

for item in soup.findAll('',{'itemprop':'name'}):
    if item.get('content')!=None:
        book.append(str(item.get('content'))[0:49])
book_list.append(book)

book=[]

for item in soup.findAll('',{'itemprop':'name'}):
    if item.string!=None:
        book.append(item.string[0:19])
book_list.append(book)

book = []

for item in soup.findAll('',{'itemprop':'datePublished'}):
    book.append(item.string.strip())
book_list.append(book)

book = []

og_price = []
discount = []
final_price = []
i = 0

for price in soup.findAll('span', {'class': 'rrp'}):
    og_price.append(str(price.string)[3:])

for price in soup.findAll('p', {'class': 'price-save'}):
    discount.append(str(price.string.strip())[8:])

for item in soup.findAll('p',{'class':'price'}):
    if(item.string == None):
        for itr in range(0,len(og_price)-1):
            final_price.append('US$'+str(round(float(og_price[itr])-float(discount[itr]),2)))
        book.append(final_price[i])
        i=i+1
    else:
        book.append(item.string.strip())
book_list.append(book)

file.write('{0:50} {1:20} {2:15} {3:15}\n\n'.format("Book name","Author","Publication-Date","Price"))
for i in range(len(book_list[0])):
    file.write('{0:50} {1:20} {2:15} {3}\n'.format(book_list[0][i],book_list[1][i],book_list[2][i],book_list[3][i]))

