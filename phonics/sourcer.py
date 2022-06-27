import requests
from collections import Counter
from bs4 import BeautifulSoup
import app


url = 'https://www.bbc.co.uk/news/uk-61852286'
req = requests.get(url).content
soup = BeautifulSoup(req, 'html.parser')

def set_url(url):
    global soup
    req = requests.get(url).content
    soup = BeautifulSoup(req, 'html.parser')
    find_main_article()

def analyse_article(data):
    print('\nAnalysis:')
    paragraph_number = 1
    article_ratios = {

    }
    for paragraph in data:
        print('\n')
        words = paragraph.split(' ')
        paragraph_size = len(words)
        paragraph_ratios = {

        }
        for word in words:
            app.prepare_words(word.lower())
        if app.stage_one_words:
            stage_one_ratio = f'{len(app.stage_one_words)}/{paragraph_size}'
        else:
            stage_one_ratio = 0
        if app.stage_two_words:
            stage_two_ratio = f'{len(app.stage_two_words)}/{paragraph_size}'
        else:
            stage_two_ratio = 0                
        if app.stage_three_words:
            stage_three_ratio = f'{len(app.stage_three_words)}/{paragraph_size}'
        else:
            stage_three_ratio = 0                
        if app.stage_four_words:
            stage_four_ratio = f'{len(app.stage_four_words)}/{paragraph_size}'
        else:
            stage_four_ratio = 0
        if app.learned_words_present:
            learned_ratio = f'{len(app.learned_words_present)}/{paragraph_size}'
        else:
            learned_ratio = 0
        if app.challenging_words:
            challenging_ratio = f'{len(app.challenging_words)}/{paragraph_size}'
        else:
            challenging_ratio = 0
        if app.unknown_words:
            unknown_ratio = f'{len(app.unknown_words)}/{paragraph_size}'
        else:
            unknown_ratio = 0
        
        paragraph_ratios['length'] = paragraph_size
        paragraph_ratios['s1'] = len(app.stage_one_words)
        paragraph_ratios['s2'] = len(app.stage_two_words)
        paragraph_ratios['s3'] = len(app.stage_three_words)
        paragraph_ratios['s4'] = len(app.stage_four_words)
        paragraph_ratios['learned'] = len(app.learned_words_present)
        paragraph_ratios['challenging'] = len(app.challenging_words)
        paragraph_ratios['unknown'] = len(app.unknown_words)
        paragraph_ratios['missing'] = paragraph_size - len(app.stage_one_words) - len(app.stage_two_words) - len(app.stage_three_words) - len(app.stage_four_words) - len(app.challenging_words) - len(app.learned_words_present) - len(app.unknown_words)


        article_ratios[paragraph_number] = paragraph_ratios

        length_check = paragraph_size - len(app.stage_one_words) - len(app.stage_two_words) - len(app.stage_three_words) - len(app.stage_four_words) - len(app.learned_words_present)
        print(f'paragraph {paragraph_number}: {paragraph}')
        print(f'stage 1: {list(dict.fromkeys(app.stage_one_words))}')
        print(f'stage 2: {list(dict.fromkeys(app.stage_two_words))}')
        print(f'stage 3: {list(dict.fromkeys(app.stage_three_words))}')
        print(f'stage 4: {list(dict.fromkeys(app.stage_four_words))}')
        print(f'\nlearned_words: {list(dict.fromkeys(app.learned_words_present))}')
        print(f'\nchallenging words: {len(list(dict.fromkeys(app.challenging_words)))} ({length_check})')
        print(list(dict.fromkeys(app.challenging_words)))
        print(f'\nunknown: {list(dict.fromkeys(app.unknown_words))}')
        print(f'\ns1({stage_one_ratio}) s2({stage_two_ratio}) s3({stage_three_ratio}) s4({stage_four_ratio}) learned({learned_ratio}) challenging({challenging_ratio}) unknown({unknown_ratio})')

        paragraph_number+=1

        app.clear_lists()
    print('Summary:')
    for k in article_ratios.keys():
        print('\n')
        print(f'{k}: {article_ratios[k]}')
        summary = {}
        summary['s1'] = round(article_ratios[k]['s1'] / article_ratios[k]['length'] * 100)
        summary['s2'] = round(article_ratios[k]['s2'] / article_ratios[k]['length'] * 100)
        summary['s3'] = round(article_ratios[k]['s3'] / article_ratios[k]['length'] * 100)
        summary['s4'] = round(article_ratios[k]['s4'] / article_ratios[k]['length'] * 100)
        summary['learned'] = round(article_ratios[k]['learned'] / article_ratios[k]['length'] * 100)   
        summary['challenging'] = round(article_ratios[k]['challenging'] / article_ratios[k]['length'] * 100)
        summary['unknown'] = round(article_ratios[k]['unknown'] / article_ratios[k]['length'] * 100)
        print(summary)


        




def print_article(main_class):
    global soup
    paragraphs = []
    for data in soup.find_all('h1'):
        print(data.get_text())
    for data in soup.find_all('p'):
        try:
            clas = data.parent['class'][1]
        except (KeyError, IndexError):
            continue
        if clas == main_class[0][0]:
            print(data.get_text())
            paragraphs.append(data.get_text())
    analyse_article(paragraphs)

def find_main_article():
    global soup
    classes = []
    for data in soup.find_all('p'):
        try:
            clas = data.parent['class'][1]
        except (KeyError, IndexError):
            continue
        classes.append(clas)
    main_class = Counter(classes).most_common(1)
    print_article(main_class)




# find_main_article()
