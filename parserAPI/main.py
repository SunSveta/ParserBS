import requests
from abc import ABC, abstractmethod
import json
from connector import Connector
from classes import HHResume
from classes import get_top

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        raise NotImplementedError("Необходимо определить метод get_request")

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector(f'{file_name}')
        return connector


class HH(Engine):
    __url = 'https://api.hh.ru/'
    __per_page = 20

    def get_resumes(self, search_word, page):
        response = requests.get(f'{self.__url}resumes?text={search_word}&page={page}')
        print(response.status_code)
        if response.status_code == 200:
            return response.json()
        return None

    def get_request(self, search_word, resumes_count):
        page = 0
        result = []
        while self.__per_page * page < resumes_count:
            tmp_result = self.get_resumes(search_word, page)
            if tmp_result:
                result += tmp_result.get('items')
                page += 1
            else:
                break
        return result


if __name__ == '__main__':
    website = int(
        input('Выберете сайт, на котором будет производиться поиск: \n1 - https://hh.ru\n2 - https://superjob.ru\n'))
    search_word = input('Введите ключевое слово для поиска: ')
    top_count = int(input('Сколько записей нужно вывести?  '))

    while True:
        resumes_count = 100
        if website == 1:
            hh_engine = HH()
            resHH = hh_engine.get_request(search_word, resumes_count)
            a = HH.get_connector('res.json')
            a.insert(resHH)
            HHResume.add_resumes_list('res.json')
            get_top(HHResume.resumes, top_count)
            print(HHResume.get_count_of_resume)
        break
