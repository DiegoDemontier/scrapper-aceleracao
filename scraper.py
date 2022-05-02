from bs4 import BeautifulSoup, SoupStrainer
import login
from handle_json import read, write


def next_page(url):
    page = login.browser.open(url)
    soup = BeautifulSoup(page, 'html.parser')
    next_page = soup.select("div.pagination a.next_page")
    return len(next_page)


def get_soup(url, select_class):
    page = login.browser.open(url)
    only_tags = SoupStrainer(class_=select_class)
    return BeautifulSoup(page, 'html.parser', parse_only=only_tags)


def get_percentage(url):
    soup = get_soup(url, 'd-block comment-body markdown-body  js-comment-body')
    percentages = soup.select("tbody tr > td:nth-child(2)")
    max_percentage = 0
    for percentage in percentages:
        if percentage.text.find("%") != -1:
            percentage = float(percentage.text[:-1])
            if percentage > max_percentage:
                max_percentage = percentage
    return max_percentage


def get_student_info(students, pull_url):
    url_base = 'https://github.com'
    data = []
    for index in range(len(students)):
        print(pull_url[index].get('href'))
        name = students[index].text
        url = url_base + pull_url[index].get('href')
        percentage = get_percentage(url)
        data.append({'nome': name, 'pull_url': url, 'porcent': percentage})
    return data


def get_inf(url):
    soup = get_soup(url, 'flex-auto min-width-0 p-2 pr-3 pr-md-2')
    name = soup.select('span.opened-by a.Link--muted')
    links = soup.select('a.Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
    return (name, links)


def get_student_data(pull_url):
    data = []
    for url in pull_url:
        print(url)
        name, links = get_inf(url)
        data += get_student_info(name, links)
        if(next_page(url) > 0):
            url = url + '?page=2'
            name, links = get_inf(url)
            data += get_student_info(name, links)
    return data


def get_api_data():
    data_dict = read('challenge_data.json')
    api_data = []
    for dict in data_dict:
        print(dict['desafio'])
        exercises = get_student_data(dict['url'])
        api_data.append(
          {
            'desafio': dict['desafio'],
            'total': dict['total'],
            'url': dict['slack'],
            'tipo': dict['tipo'],
            'exercicios': exercises
          }
        )
    return api_data


if __name__ == '__main__':
    write(get_api_data())
