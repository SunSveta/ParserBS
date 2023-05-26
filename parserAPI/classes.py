import json

class Resume:
    __slots__ = ('first_name', 'last_name', 'link')

    def __init__(self, first_name, last_name, link):
        self.first_name = first_name
        self.last_name = last_name
        self.link = link

    def __str__(self):
        return f'{self.first_name} {self.last_name}, ссылка на резюме: {self.link}'


    def __iter__(self):
        self.value = 0
        return self.value

    def __next__(self):
        if self.value < len(self.resumes):
            self.value += 1
        else:
            raise StopIteration

class CountMixin:

    @property
    def get_count_of_resume(self):
        """
        Вернуть количество резюме от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open(self.data_file, 'r') as d:
            data = json.load(d)
            for i in data:
                return len(i)


class HHResume(CountMixin, Resume):  # add counter mixin
    """ HeadHunter Vacancy """
    data_file = 'res.json'
    resumes = []

    def __init__(self, first_name, last_name, link):
        super().__init__(first_name, last_name, link)
        self.count = CountMixin.get_count_of_resume

    @classmethod
    def add_resumes_list(cls, data_file):
        with open(f'{data_file}') as f:
            d_file = json.load(f)
            for i in d_file:
                for j in i:
                    a = j.get("first_name")
                    b = j.get('url')
                    c = j.get('last_name')

                    cls.resumes.append(HHResume(a, b, c))



    def __str__(self):
        return f'HH: ' + super().__str__()


def get_top(resumes, top_count):
    """ Должен возвращать {top_count} записей"""
    for i in range(top_count):
        print(resumes[i])

if __name__ == '__main__':

    HHResume.add_resumes_list('res.json')
    get_top(HHResume.resumes, 1)

    print(HHResume.get_count_of_resume)