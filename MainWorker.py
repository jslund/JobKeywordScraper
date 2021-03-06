import requests
import bs4 as beautifulSoup
from multiprocessing.dummy import Pool

def ResultsFinder(search_string):
    search = requests.get(search_string)
    search_soup = beautifulSoup.BeautifulSoup(search.content, "lxml")
    soup_urls = search_soup.find_all(attrs={'data-tn-element': 'jobTitle'})

    return soup_urls


def TextScraper(url):
    page = requests.get(url)
    job_soup = beautifulSoup.BeautifulSoup(page.content, "lxml")
    job_description = job_soup.find(attrs={'class': 'jobsearch-JobComponent-description'})
    job_description = job_description.get_text()

    return job_description

def Scraper(search_term, search_location):
    #Loads the search page into a soup object and creates a list of all links




    search_string = "https://www.indeed.co.uk/jobs?q={0}&l={1}".format(search_term, search_location)
    search_string_list = [search_string]
    search_string_list.append(search_string + "&start=10")
    search_string_list.append(search_string + "&start=20")

    job_pages = ""


    with Pool(3) as threads: soup_urls = threads.map(ResultsFinder, search_string_list)




    #Get the links to next pages from the bottom. TODO//Make compatible for many searches. Cross check the links on each page
    # page_urls_soup = search_soup.find(attrs={'class': 'pagination'})
    # page_urls = page_urls_soup.find_all('a')
    # href_list = []
    # for url in page_urls:
    #     href = "https://www.indeed.co.uk" + url['href']
    #     href_list.append(href)
    #
    # href_list = list(set(href_list))



    url_string_list = []

    n = 0

    for url_set in soup_urls:
        for url in url_set:
            url_string = "https://www.indeed.co.uk" + url['href']
            url_string_list.append(url_string)
            n += 1


    with Pool(n) as threads: job_description_list = threads.map(TextScraper, url_string_list)



    job_description = " "
    job_pages = job_description.join(job_description_list)

    return job_pages

def LanguageProcessor(job_pages):
    import nltk

    default_stopwords = set(nltk.corpus.stopwords.words('english'))

    words = nltk.word_tokenize(job_pages)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # Remove stopwords
    words = [word for word in words if word not in default_stopwords]

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 50 words
    frequency_list = {}

    for word, frequency in fdist.most_common(25):
        frequency_list[word] = frequency
        print(u'{};{}'.format(word, frequency))

    return frequency_list

if __name__ == '__main__':
    #search_term = input("Type Search Term ")
    #search_location = input("In which location? ")
    search_term = "python"
    search_location = "remote"
    job_pages = Scraper(search_term, search_location)
    frequency_list = LanguageProcessor(job_pages)

