from collections import Counter
import hashlib
import os
import re

from bs4 import BeautifulSoup, Comment
import nltk
from wordcloud import WordCloud
from settings import WCLOUD_PATH


def make_word_cloud(words):
    filename = hashlib.md5()
    filename.update(bytes(' '.join(words), 'utf-8'))
    filename = filename.hexdigest() + '.png'
    fpath = os.path.join(WCLOUD_PATH, filename)
    most_common = Counter(words).most_common(100)
    if not os.path.exists(fpath):
        wc = WordCloud(
            width=800, height=400
        ).generate_from_frequencies(
            frequencies=dict(most_common)
        )
        image = wc.to_image()
        image.save(fpath)
    url = '/word_cloud/' + filename
    return most_common, url


def remove_tags(dirty_html):
    """
    Extracts the text from an html page.
    Cleans all scripts, comments, linebreaks, etc.
    """
    soup = BeautifulSoup(dirty_html, "lxml").body

    # remove comments
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    [c.extract() for c in comments]

    # remove scripts
    [s.extract() for s in soup.find_all('script')]
    [s.extract() for s in soup.find_all('noscript')]

    # get rid of multiple spaces and line breaks
    soup = soup.get_text(' ')
    soup = re.sub('[ \n]+', ' ', soup)
    return soup.lower()


def clear_word(word):
    return re.sub('^[\']', '', word)


def nltk_text(dirty_text):
    """
    Removes everything from `dirty_text`
    that aren't nouns or verbs.
    """

    # breaks the text into a list of tokens (words, punctuation...)
    tokens = nltk.word_tokenize(dirty_text)
    # part-of-speech tagger: tags grammar classes
    tags = nltk.pos_tag(tokens)
    nouns = [
        clear_word(word) for word, pos in tags if (
            (  # ignore single char/blanks
                len(word) > 1
            ) and (  # keeps only the nouns, composed nouns, etc
                pos == 'NN' or pos == 'NNP' or
                pos == 'NNS' or pos == 'NNPS'
            )
        )
    ]
    return nouns
