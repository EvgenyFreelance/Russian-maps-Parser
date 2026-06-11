import playwright
from playwright.sync_api import sync_playwright
import time
import random
import re


class Parser():
    def __init__(self,url,place,institution,proxies=None):
        # --- Создание аттрибутов класса для более гибкого создания парсеров ---
        self.url = url
        self.place = place
        self.institution = institution

        # --- Создание макета данных которые будет парсит парсер ---
        self.data = {'Название': [],
                     'Ссылка': [],
                     'Адрес': [],
                     'Сайт': [],
                     'Телефон(ы)': [],
                     'Типы учреждений': [],}

    # --- Создаем функции, которя скроллит вниз на определённой странице, до определённого элемента
    def scrolling_down(self,page,selector):
        try:
            page.locator('.search-list-view__list').hover()

            while True:
                page.mouse.wheel(delta_x=0, delta_y=random.randint(300,500))
                time.sleep(random.uniform(0.15,0.3))

                if page.locator(selector).is_visible():
                    break

        except Exception as er:
            print(er)

    # --- Основа работы парсера ---
    def parse(self):
        with sync_playwright() as pl:
            # --- Создаем контекст(постоянного пользователя для парсера)
            browser = pl.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()

            # --- Переходим по начальной ссылке и ищем по заданному городу
            self.page.goto(self.url)

            self.page.get_by_placeholder('Поиск и выбор мест').type(text=self.place + ' ' + self.institution,delay=1)
            self.page.get_by_placeholder('Поиск и выбор мест').press(key='Enter')

            # --- Собираем все нужные элементы ---
            self.scrolling_down(self.page,'.add-business-view')
            self.elements = self.page.query_selector_all('li.search-snippet-view')

            print(len(self.elements))

            # Перебираем их
            for element in self.elements:
                link_and_name = element.query_selector('a.link-overlay')
                address = element.query_selector('a.search-business-snippet-view__address').inner_text() if element.query_selector('a.search-business-snippet-view__address') else 'Аддрес отсутсвует'
                self.data['Адрес'].append(address)

                if link_and_name:
                    self.data['Название'].append(
                        link_and_name.inner_text()
                    )

                    link = 'https://yandex.ru' + link_and_name.get_attribute('href')
                    self.data['Ссылка'].append(link)

            # --- Переходим по списку полученных ссылок в предыдущем цикле и дальше парсим информацию ---
            for link in self.data['Ссылка']:

                    self.page.goto(link)
                    self.page.mouse.wheel(delta_x=0, delta_y=random.randint(300, 1000))

                    site_link = self.page.query_selector('a.business-urls-view__link').get_attribute('href') if self.page.query_selector('a.business-urls-view__link') else 'Ссылка на сайт отсутсвует'
                    self.data['Сайт'].append(site_link)

                    phones = [x.inner_text() + ', ' for x in self.page.query_selector_all('div.card-phones-view__phone-number')] if self.page.query_selector_all('div.card-phones-view__phone-number') else 'Телефон отсутствует'
                    phones = [x.replace('\nПоказать телефон','') for x in phones]
                    self.data['Телефон(ы)'].append(''.join(phones))

                    # self.page.locator('div.tabs-select-view__title _name_features').hover()
                    # self.page.locator('div.tabs-select-view__title _name_features').click()
                    categories = self.page.query_selector('div.orgpage-categories-info-view')
                    categories  = [x.inner_text() + ', ' for x in categories.query_selector_all('span.button__text')] if categories else 'Указанные типы отсутствуют'
                    self.data['Типы учреждений'].append(''.join(categories))

                    time.sleep(2)

            print(self.data)
            time.sleep(10)

    def get_result(self):
        return self.data

if __name__ == '__main__':
    Parser(url='https://yandex.ru/maps',place='Ярославль',institution='Больницы').parse()

