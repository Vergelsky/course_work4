from abc import abstractmethod, ABC
import os
from vacancy import Vacancy
import json

class FileManagerAbc(ABC):
    file_vacancy_name = os.path.join('src', 'vacancy.txt')

    @abstractmethod
    def writhe_vacancy_to_file(self, vacancy):
        pass

    @abstractmethod
    def read_vacancies_from_file(self):
        pass


class FileManager(FileManagerAbc):
    def writhe_vacancy_to_file(self, vacancy):
        with open(self.file_vacancy_name, 'a') as file:
            file.write(vacancy.gen_string())

    def read_vacancies_from_file(self):
        with open(self.file_vacancy_name, 'r') as file:
            text = file.readlines()
        vacancies = []
        for line in text:
            vacancies.append(Vacancy(line))