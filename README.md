# Welcome to App Stroe Crawler!

This code is python based for i-Tunes crawler to scrape all webpages with the following base url: https://itunes.apple.com/us/genre/ios/ and get the list of all app store applications along with their category, size, rating, reviews, price, languages, compatibility, developer, iTunes url and image url.

The basic aim is to gather/mine data about the apps of App Store and build a rich database so that developers, apple fans and anyone else can use to generate statistics about the current app store situation



# Usage:
```
python itunes_crawler.py
```
Directly run the script itunes_crawler.py to get all apps data as a csv file. By default it will automatically crawl App Store home page!

# Example of Scraped Data:
```
app_id: 422689480
app_name: Gmail - Email by Google
developer: Google LLC
price: Free
rating: 4.5
reviews: 100.9K
size: 169.7 MB
category: Productivity
age: Rated 4+
language: "English, Afrikaans, Arabic, Basque, Bengali, Bulgarian, Catalan, Chinese (Hong Kong), Croatian, Czech, Danish, Dutch, Estonian, Filipino, Finnish, French, Galician, German, Greek, Gujarati, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Korean, Latvian, Lithuanian, Malay, Malayalam, Marathi, Norwegian, Norwegian Bokmål, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Simplified Chinese, Slovak, Slovenian, Spanish, Swahili, Swedish, Tamil, Telugu, Thai, Traditional Chinese, Turkish, Ukrainian, Urdu, Vietnamese, Zulu"
compatibility: Requires iOS 10.0 or later. Compatible with iPhone, iPad, and iPod touch.
seller: Google LLC
seller_website: https://mail.google.com
img_src: https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/d2/53/c0d25328-24eb-fd1d-b3ba-f9c6f761c420/logo_gmail_color-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/230x0w.jpg
```
