import re
import subprocess
import unicodedata
from typing import List, Optional

import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer


# Download the models used
nltk.download("stopwords")
nltk.download("punkt")
subprocess.run(["spacy", "download", "en_core_web_sm"])
stopword_list = nltk.corpus.stopwords.words("english")


def remove_html_tags(text: str) -> str:
    """
    Remove html tags from text like <br/> , etc. You can use BeautifulSoup for this.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    
    # Parse the html in the 'text' variable, and store it in Beautiful Soup format  
    soup = BeautifulSoup(text, "html.parser")
    # get text
    doc = soup.get_text()
    # return data by retrieving the text content
    return doc



def stem_text(text: str) -> str:
    """
    Stem input string.
    (*) Hint:
        - Use `nltk.porter.PorterStemmer` to pass this test.
        - Use `nltk.tokenize.word_tokenize` for tokenizing the sentence.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    
    # tokenize the sentence
    tokens = word_tokenize(text)
    porter = nltk.stem.PorterStemmer()
    # stem the tokens
    # create an empty list to store the stems
    stems = [porter.stem(word) for word in tokens]
    # join the stems
    doc = " ".join(stems) 
    return doc



def lemmatize_text(text: str) -> str:
    """
    Lemmatize input string, tokenizing first and extracting lemma from each text after.
    (*) Hint: Use `nlp` (spacy model) defined in the beginning for tokenizing
    and getting lemmas.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    empty_list = [token.lemma_ for token in doc]
    final_string = " ".join(map(str,empty_list))
    return final_string

def remove_accented_chars(text: str) -> str:
    """
    Remove accents from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    doc = ''.join(c for c in unicodedata.normalize('NFKD', text)
                  if unicodedata.category(c) != 'Mn'
                  )
    return doc


def remove_special_chars(text: str, remove_digits: Optional[bool] = False) -> str:
    """
    Remove non-alphanumeric characters from input string.

    Args:
        text : str
            Input string.
        remove_digits : bool
            Remove digits.

    Return:
        str
            Output string.
    """
    if remove_digits:
        pattern = "[^a-zA-z\s]+"
    else:
        pattern = "[^a-zA-Z0-9\s]+"
    filtered_doc = re.sub(pattern, '',text)   
    return filtered_doc


def remove_stopwords(
    text: str,
    is_lower_case: Optional[bool] = False,
    stopwords: Optional[List[str]] = stopword_list,
) -> str:
    """
    Remove stop words using list from input string.
    (*) Hint: Use tokenizer (ToktokTokenizer) defined in the beginning for
    tokenization.

    Args:
        text : str
            Input string.
        is_lower_case : bool
            Flag for lowercase.
        stopwords : List[str]
            Stopword list.

    Return:
        str
            Output string.
    """
    toktok = ToktokTokenizer()

    tokens = toktok.tokenize(text)
    
    if not is_lower_case:
        tokens = [token.lower() for token in tokens]
    
    tokens_cleaned = [token for token in tokens if token not in stopwords]
    

    doc = " ".join(map(str,tokens_cleaned))
    return doc

def remove_extra_new_lines(text: str) -> str:
    """
    Remove extra new lines or tab from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    # Remove extra tabs and lines
    processed_string = re.sub(r'\n+|\t+', ' ', text)
    
    return processed_string


def remove_extra_whitespace(text: str) -> str:
    """
    Remove any whitespace from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    processed_string = re.sub(r'\s+', ' ', text)
    return processed_string



def normalize_corpus(
    corpus: List[str],
    html_stripping: Optional[bool] = True,
    accented_char_removal: Optional[bool] = True,
    text_lower_case: Optional[bool] = True,
    text_stemming: Optional[bool] = False,
    text_lemmatization: Optional[bool] = False,
    special_char_removal: Optional[bool] = True,
    remove_digits: Optional[bool] = True,
    stopword_removal: Optional[bool] = True,
    stopwords: Optional[List[str]] = stopword_list,
) -> List[str]:
    """
    Normalize list of strings (corpus)

    Args:
        corpus : List[str]
            Text corpus.
        html_stripping : bool
            Html stripping,
        contraction_expansion : bool
            Contraction expansion,
        accented_char_removal : bool
            accented char removal,
        text_lower_case : bool
            Text lower case,
        text_stemming : bool
            Text stemming,
        text_lemmatization : bool
            Text lemmatization,
        special_char_removal : bool
            Special char removal,
        remove_digits : bool
            Remove digits,
        stopword_removal : bool
            Stopword removal,
        stopwords : List[str]
            Stopword list.

    Return:
        List[str]
            Normalized corpus.
    """

    normalized_corpus = []

    # Normalize each doc in the corpus
    for doc in corpus:
        # Remove HTML
        if html_stripping:
            doc = remove_html_tags(doc)

        # Remove extra newlines
        # doc = remove_extra_new_lines(doc)

        # Remove accented chars
        if accented_char_removal:
            doc = remove_accented_chars(doc)

        # Lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)

        # Stemming text
        if text_stemming and not text_lemmatization:
            doc = stem_text(doc)

        # Remove special chars and\or digits
        if special_char_removal:
            doc = remove_special_chars(doc, remove_digits=remove_digits)

        # Remove extra whitespace
        # doc = remove_extra_whitespace(doc)

        # Lowercase the text
        if text_lower_case:
            doc = doc.lower()

        # Remove stopwords
        if stopword_removal:
            doc = remove_stopwords(
                doc, is_lower_case=text_lower_case, stopwords=stopwords
            )

        # # Remove extra whitespace
        # doc = remove_extra_whitespace(doc)
        doc = doc.strip()

        normalized_corpus.append(doc)

    return normalized_corpus