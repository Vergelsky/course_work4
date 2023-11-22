from code.vacancy import Vacancy
from code.file_manager import FileManager
from code.site_api import HeadHunterAPI, SuperJobAPI
from datetime import datetime

hh_api = HeadHunterAPI()
sj_api = SuperJobAPI()

def create_vacancies(request, per_page=100):
    vacancies_list = []
    per_page = per_page if per_page <= 100 else 100

    hh_response = hh_api.load_vacancy(request, per_page)['items']

    for item in hh_response:
        vacancies_list.append(Vacancy(datetime.fromisoformat(item['published_at']).timestamp(),
                                      item['name'],
                                      item['employer']['name'],
                                      item['salary']['from'],
                                      item['salary']['to'],
                                      item['snippet']['responsibility'],
                                      item['alternate_url']))

    sj_response = sj_api.load_vacancy(request, per_page)['objects']

    for item in sj_response:
        vacancies_list.append(Vacancy(item['date_published'],
                                      item['profession'],
                                      item.get('client').get('title'),
                                      item['payment_from'],
                                      item['payment_to'],
                                      item['candidat'],
                                      item['link']))
    return vacancies_list

if __name__ == '__main__':
    print("Какую работу искать?")
    request_text = input()
    print("Сколько вариантов найти?")
    per_page = int(input())//2

    vacancies = create_vacancies(request_text, per_page)

    for vac in vacancies:
        print(vac)

