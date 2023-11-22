from abc import ABC, abstractmethod
import os
import requests
import json

class SiteAPI(ABC):
    @abstractmethod
    def load_vacancy(self, keyword):
        pass

class HeadHunterAPI(SiteAPI):
    url_hh = "https://api.hh.ru/vacancies/"

    def load_vacancy(self, keyword, per_page='50'):
        """
        :param keyword: поисковая фраза
        :param per_page: количество результатов
        :return:
        """
        response = requests.get(self.url_hh, params={"text": keyword, "per_page": per_page})

        response_dict = json.loads(response.text)

        return response_dict


class SuperJobAPI(SiteAPI):
    api_key_sj = os.getenv('API_KEY_SUPER_JOB')
    url_sj = "https://api.superjob.ru/2.0/vacancies/"

    def load_vacancy(self, keyword, per_page='50'):
        """
        :param keyword: поисковая фраза
        :param per_page: количество результатов
        :return:
        """
        response = requests.get(self.url_sj, params={"keyword": keyword, "count": per_page})

        response_dict = json.loads(response.text)

        return response_dict
