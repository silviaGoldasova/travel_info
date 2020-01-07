from model.models import db, Page, Category, load_db, Section, Section_form_obj
import wikipediaapi
import requests
import random

def add_place_to_db_new_page(title, category = "Other"):
    page = Page(title, category)
    db.session.add(page)

    categories = get_all_categories()
    if category not in categories:
        category_obj = Category(category)
        db.session.add(category_obj)

    db.session.commit()

def add_place_to_db(page):
    db.session.add(page)
    categories = get_all_categories()
    if page.category not in categories:
        category_obj = Category(page.category)
        db.session.add(category_obj)
    db.session.commit()

def get_all_categories():
    categories = Category.query.all()
    categories_list = []
    for category in categories:
        categories_list.append(category.name.strip())
    return categories_list

def get_all_places():
    places = Page.query.all()
    return places

def get_all_titles():
    titles = []
    places = get_all_places()
    for place in places:
        titles.append(place.title)
    return titles

def get_category(place_title):
    pages = get_all_places()
    for place in pages:
        if place.title.strip() == place_title.strip():
            return place.category

def add_category(category_name):
    categories = get_all_categories()
    if category_name not in categories:
        category_obj = Category(category_name)
        db.session.add(category_obj)

    """
    print(wikipedia.search("Bill", results=2))
    wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI )
    page_py = wiki.page('Italy')
    text = page_py.text

    #print("Page - Summary: %s" % page_py.summary[0:60])
    # Page - Summary: Python is a widely used high-level programming language for
    """


def get_sections(sections_wiki, section_list, level = 0):
    for section in sections_wiki:
        s = Section(section.title, section.text)
        section_list.append(s)
        get_sections(section.sections, section_list, level+1)
    return section_list


def get_sections_list(title):
    wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    page = wiki.page(title)
    page_sections = page.sections
    sections_list = []
    sections_list = get_sections(page_sections, sections_list)
    sections_obj_list = []
    index = 1
    for section in sections_list:
        sec_obj = Section_form_obj(section.name, section.text, index)
        sections_obj_list.append(sec_obj)
        index += 1
    return sections_obj_list

def get_image(query):
    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': 50,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'uiv': 4
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )
    response = r.json().get('data').get('result').get('items')
    print(response)
    urls = [r.get('media') for r in response]
    return random.choice(urls)