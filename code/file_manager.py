from abc import abstractmethod, ABC
import os
from code.vacancy import Vacancy
import json


class FileManagerAbc(ABC):

    @abstractmethod
    def write_vacancies_to_file(self, vacancy):
        pass

    @abstractmethod
    def read_vacancies_from_file(self):
        pass

    @abstractmethod
    def del_vacancies_from_file(self, vacancy):
        pass


class FileManager(FileManagerAbc):
    file_json_vacancy_name = os.path.join('src', 'vacancy.json')

    def write_vacancies_to_file(self, vacancies):
        """
        Если файл не пустой - создаём список с его содежимым, если пустой - пустой список.
        Добавляем туда список полей каждой вакансии из vacancies по-очереди.
        Перезаписываем файл.
        :param vacancies: Список вакансий.
        :return: Ничего.
        """
        with open(self.file_json_vacancy_name, 'r+') as file:
            text = file.read()
            if text:
                data = list(json.loads(text))
            else:
                data = []

            for vac in vacancies:
                data.append({'date': vac.date,
                             'title': vac.title,
                             'employer': vac.employer,
                             'salary': vac.salary,
                             'description': vac.description,
                             'url': vac.url})
            file.seek(0)
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    def read_vacancies_from_file(self):
        """
        Читаем из файла список словарей, из каждого словаря создаём объект вакансии
        и складываем в одну переменную.
        :return: Список вакансий
        """
        vacancies = []
        with open(self.file_json_vacancy_name, 'r') as file:
            text = file.read()
            if text:
                j_text = json.loads(text)
                for line in j_text:
                    vacancies.append(Vacancy(line['date'],
                                             line['title'],
                                             line['employer'],
                                             line['salary'],
                                             line['salary'],
                                             line['description'],
                                             line['url']))
            else:
                vacancies = -1
        return vacancies

    def del_vacancies_from_file(self, vacancy):
        vacancies = self.read_vacancies_from_file()
        if vacancy in vacancies:
            vacancies.remove(vacancy)
            self.clean_the_file()
            self.write_vacancies_to_file(vacancies)

    def clean_the_file(self):
        with open(self.file_json_vacancy_name, "w"):
            pass
