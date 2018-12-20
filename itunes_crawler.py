import io
import re
import csv
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup

session = requests.Session()


def category_urls(url):
	codes = []
	genres = []
	category_urls = []
	source = session.get(url).text
	soup = BeautifulSoup(source, 'html.parser')
	content = soup.find(class_ = 'grid3-column')
	for a in content.find_all('a', {'class' : 'top-level-genre'}):
		code = a['href'].rsplit('/', 1)[1]
		codes.append(code)
		genre = a.text
		genres.append(genre)
		category_urls.append(a['href'])
	return (category_urls, codes, genres)


def urls_of_single_page(url):
	source = session.get(url).text
	soup = BeautifulSoup(source, 'html.parser')
	content = soup.find(class_ = 'grid3-column')
	target_urls = []
	for a in content.find_all('a'):
		app_url = a['href']
		target_urls.append(app_url)
	return target_urls


num_of_pages = []
def pagination(url):
	source = session.get(url).text
	soup = BeautifulSoup(source, 'html.parser')
	content = soup.find('div', {'id' : 'selectedgenre'})
	ul = content.find(class_ = 'list paginate')
	if not ul:
		return 1
	for li in ul.find_all('li'):
		num_of_pages.append(li.text)

	if 'Next' in num_of_pages:
		new_url = url.split('&page=')[0] + '&page=' + num_of_pages[-2] + '#page'
		if new_url == url:
			return int(num_of_pages[-2])
		if int(num_of_pages[-2]) < 18:
			return int(num_of_pages[-2])
		pagination(new_url)
		return int(num_of_pages[-2]) + 1
	else:
		return (num_of_pages[-1])


def get_data(url):
	source = session.get(url).text
	soup = BeautifulSoup(source, 'html.parser')
	for meta in soup.find_all('meta'):
	      if ('name' in meta.attrs and meta.attrs['name'] == 'apple:content_id'):
	        app_id = meta.get('content')

	# check whether the page exists or not
	try:
	    app_id
	except NameError:
		return 0

	data = soup.find_all('dd', class_ = 'information-list__item__definition l-column medium-9 large-6')
	if data:
		seller = data[0].text.strip()
		size = data[1].text.strip()
		category = data[2].text.strip()
		age = data[3].text.strip()
	else:
		seller = size = category = age = ''

	if soup.find(class_ = 'product-header__title app-header__title'):
		app_name = soup.find(class_ = 'product-header__title app-header__title').text.strip().split('\n')[:-1][0]
	else:
		app_name = 'null'
	if soup.find(class_ = 'link'):
		developer = soup.find(class_ = 'link').text.strip()
	else:
		developer = ''
	if soup.find(class_ = 'inline-list__item inline-list__item--bulleted'):
		price = soup.find(class_ = 'inline-list__item inline-list__item--bulleted').text.strip()
	else:
		price = ''
	if soup.find('span', class_ = 'we-customer-ratings__averages__display'):
		rating = soup.find('span', class_ = 'we-customer-ratings__averages__display').text.strip()
	else:
		rating = ''
	if soup.find('h5', class_ = 'we-customer-ratings__count medium-hide'):
		reviews = soup.find('h5', class_ = 'we-customer-ratings__count medium-hide').text.strip().replace(' Ratings','')
	else:
		reviews = ''
	if soup.find('dd', class_ = 'information-list__item__definition l-column medium-9 large-6 we-truncate we-truncate--multi-line we-truncate--interactive ember-view'):
		language = soup.find('dd', class_ = 'information-list__item__definition l-column medium-9 large-6 we-truncate we-truncate--multi-line we-truncate--interactive ember-view').text.strip()
	else:
		language = ''
	if soup.find('dd', class_ = 'we-truncate we-truncate--multi-line we-truncate--interactive ember-view information-list__item__definition l-column medium-9 large-6'):
		compatibility = soup.find('dd', class_ = 'we-truncate we-truncate--multi-line we-truncate--interactive ember-view information-list__item__definition l-column medium-9 large-6').text.strip()
	else:
		compatibility = ''
	if soup.find('a', class_ = 'link icon icon-after icon-external'):
		seller_website = soup.find('a', class_ = 'link icon icon-after icon-external')['href']
	else:
		seller_website = ''
	if soup.find(class_ = 'we-artwork__source'):
		img_src = soup.find(class_ = 'we-artwork__source')['srcset'].split(',')[0].replace(' 1x', '')
	else:
		img_src = ''
	
	header = [[app_id, app_name, developer, price, rating, reviews, size, category, age, language, compatibility, seller, seller_website, img_src]]
	if not header:
		return 0

	df = pd.DataFrame(header, columns=['app_id', 'app_name', 'developer', 'price', 'rating', 'reviews', 'size', 'category', 'age', 'language', 'compatibility', 'seller', 'seller_website', 'img_src'])
	if df.empty:
		return 0

	if counter == 1:
		df.to_csv('data.csv', sep=',', encoding='utf-8', index=False)
	else:
		with open('data.csv', 'a') as file:
			df.to_csv(file, index=False, encoding='utf-8', header=False)
	return 1



base_url = 'https://itunes.apple.com/us/genre/ios/id36?mt=8'
category_url = 'https://itunes.apple.com/us/genre/ios-'

(category_urls, codes, genres) = category_urls(base_url)
alphabets = list(string.ascii_uppercase)

print 'The first step is to parse the pagination structure of each letter to get the total number of category pages, and this can be done by navigating through all categories available on iTunes home page.'

category_list = []
for i, url in enumerate(category_urls):
	print '\n{} category is being prepared...'.format(genres[i])
	letter_index = []
	for index, letter in enumerate(alphabets):
		letter_url = url + '&letter=' + letter
		page_num = pagination(letter_url)
		letter_index.append((letter, page_num))
		print 'letter {} is done, and it has {} pages!'.format(letter, page_num)
	letter_index.insert(0, genres[i])
	print '{} genre is successfully completed!'.format(genres[i])
	category_list.insert(len(letter_index), letter_index)
print category_list



# retrieving and scraping all pages from each category through alphabetical and numeric pagination respectively..
target_pages = []
for i in range(0, len(genres)):
	for j in range(0, len(alphabets)):
		for k in range(1, category_list[i][j+1][1] + 1):
			target_url = category_url + str(genres[i].replace(' & ','-').replace(' ', '-').lower()) + '/' + codes[i] + '&letter=' + str(alphabets[j]) + '&page=' + str(k) + '#page'
			target_pages.append(target_url)


print '\nThe next step is to grap every application info based on the urls that are just retrieved from categories pages. \n'
print 'Total pages to be scrapped are about {} pages!'.format(len(target_pages))
print 'Each page has around 90 urls/applications... \n'
app_urls = []
finished_urls = 0
for index, url in enumerate(target_pages):
	target_urls = urls_of_single_page(url)
	finished_urls += len(target_urls)
	print '{} urls were successfully retrieved..'.format(finished_urls)
	if (index % 150 == 0):
		print '\n{} pages out of {} pages are finished so far... \n'.format(index + 1, len(target_pages))
	app_urls.extend(target_urls)


print '{} urls on the iTunes were grabed successfully... \n'.format(finished_urls)
print 'The next step is to access each single application in order to extract its data. \n'


# extracting the data for each single application
counter = 1
results = []
for app_url in app_urls:
	app_url = app_url.decode('utf-8')
	data = get_data(app_url)
	results.append(data)
	counter += 1
	print '{} urls out of {} urls were scraped...'.format(counter - 1, len(app_urls))
	

print '\nFinished scraping all iTunes applications!'
print 'Only {} application(s) out of {} were not scraping correctly!'.format(results.count(0), len(results))


