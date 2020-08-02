from os import system
from time import sleep
from bot import ParseAnswers as Bot
from utils import parse_answers

try:
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import json, xlsxwriter

except ImportError:
    print('Installation of some modules, please wait for a moment.')
    system('python -m pip install -r requirements.txt')

class AutomaticTest(Bot):
    def solve(self, index: int) -> None:
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath('/html/body/nav/div/div/div/div[4]/a').click()
        self.driver.find_element_by_xpath(f'/html/body/section[2]/div/div/div[{index}]/div/div[2]/a').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_css_selector('body > section.course-detail-page > div > div.course-rules-page__btns \
        > a.btn.btn-blue-transparent.course-rules-page__btn').click()

        answers = parse_answers(self.driver.page_source)
        html = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        tests = html.find_all('div', {'class': 'test-item'})
        data = []

        for test in tests:
            data.append({
                'title': test.find('div', {'class': 'test-item__question'}).text,
                'answers': list(map(lambda x: str(x.text), test.find('div', {'class': 'test-item__answers-row'})\
                .find_all('div', {'class': 'test-item__answer'})))
            })

        for test in data:
            self.driver.implicitly_wait(1)
            answer_tests = list(filter(lambda x: AutomaticTest.clean(x['title']) \
                in AutomaticTest.clean(test['title']), answers['data']))[0]
            answer = list(filter(lambda x: x['is_true_answer'] == 1, answer_tests['answers']))

            index_of_correct = 1 if not answer else answer_tests['answers'].index(answer[0]) + 1
            index_of_test = data.index(test) + 1

            result_element = self.driver.find_element_by_xpath(f'//*[@id="app-quiz"]/div/div[3]/div[{index_of_test}]/div[3]/div/div[{index_of_correct}]/label/span')

            result_element.click()
        
        sleep(3)
    
    @staticmethod
    def clean(text: str) -> str:
        return text.replace('\t', ' ').replace('\n', ' ').strip()


if __name__ == '__main__':
    username = input('Username: ') # 'qwert'
    password = input('Password: ') # '147258'
    
    try:
        for index in range(1, 20):
            bot = AutomaticTest(show = False)
            bot.login(username, password)
            bot.solve(index)
            bot.close()

            print(f'Test {index} is done')
    except Exception as error:
        print(f'Error: {error.__class__.__name__}')
        system('pause')
        exit(1)
