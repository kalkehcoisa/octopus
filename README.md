# Octopus Challenge


## Requirements

1. Use docker-compose for the different parts of the application (web server, DB)
2. Create a Python web application using Tornado web server.
3. The project should have a single page with a form where I can enter a URL to any website (e.g. Wikipedia or BBCNews)
4. The application should fetch that url and:
    a. Build a dictionary that contains the frequency of use of each word on that page.
    b. Use wit.ai to perform sentiment analysis (positive, negative) on the text of the document. Feel free to train the system in the way you wish.
5. Use this dictionary to display, on the client’s browser, a “word cloud” of the top 100 words, where the font size is largest for the words used most frequently, and gets progressively smaller for words used less often.
6. Each time a URL is fetched, it should save the top 100 words to a MySQL DB, with the following three columns:
    a. The primary key for the word is a salted hash of the word.
    b. The word itself is saved in a column that has asymmetrical encryption, and you are saving the encrypted version of the word.
    c. The total frequency count of the word. Each time a new URL is fetched, you should INSERT or UPDATE the word rows.
7. Each time a URL is fetched, it should save the sentiment analysis to a MySQL DB, with the following columns:
    a. The primary key as salted hash of the url
    b. The primary key as the url
    c. The result of sentiment analysis (positive, negative)
8. An “admin” page, that will:
    a. List all words entered into the DB, ordered by frequency of usage, visible in decrypted form.
    b. List all the urls with their negative/positive qualification

9. Extra points for:
    a. Displaying just nouns and verbs (no prepositions or articles)
    b. In README, describe the best way to safely store and manage the keys.
    c. Elegant front end layout.
    d. Clean, well documented code.


## Introduction
This is a simple system based on docker-compose that gathers data from urls entered into a form, saves the word count for the top 100 words into mysql - only nouns and verbs - and shows to the user a word cloud made with them and presents a simple "admin" interface to see the data saved in the database.


## Install and Deploy
To install, it's necessary to have docker-compose and run in the root path (the path where *docker-compose.yml* is):
```
docker-compose rm -fv
docker-compose build
docker-compose up
```

## Usage
Just access http://localhost:5000, fill the input with a valid url and the system is going to gather the text from there, generate and show a word cloud from the top 100 words and show the top 100 words.
Also, there is an "admin" interface where it's possible to see all the words registered throughout all the requests to pages.
