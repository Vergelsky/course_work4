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


def show_vacancies(vacancies_list):
    for i in range(len(vacancies_list)):
        print(f"{i + 1}: {vacancies_list[i]}")


def sort_vacancies(vacancies_list):
    return sorted(vacancies_list)


if __name__ == '__main__':
    while True:
        print("Какую работу искать? (1 - открыть сохранённый поиск)")
        search_text = input()
        if search_text == '1':
            fm = FileManager()
            vacancies = fm.read_vacancies_from_file()
            if vacancies == -1:
                print("Нет сохранённых данных")
                continue
            print("Сохранённый поиск:")
            show_vacancies(vacancies)
            print("Удалить или новый поиск? (1 - удалить, 0 - новый поиск)")
            need_delete = int(input())
            if need_delete:
                print("Укажите номер удаляемой вакансии, -1 - удалить всё, 0 - новый поиск:")
                number = int(input())
                if number > 0:
                    fm.del_vacancies_from_file(vacancies[number - 1])
                    vacancies = fm.read_vacancies_from_file()
                    show_vacancies(vacancies)
                    continue
                elif number:
                    fm.clean_the_file()
                    continue
                else:
                    continue
        else:
            print("Сколько вариантов найти?")
            request_text = input()
            if request_text:
                per_page = int(request_text) // 2
            else:
                per_page = 20
            vacancies = create_vacancies(search_text, per_page)
            show_vacancies(vacancies)

        print("Сохранить, сортировать или новый поиск? (1 - сохранить, 2 - сортировать, 0 - новый поиск)")
        need_action = int(input())
        if need_action == 1:
            f = FileManager()
            f.write_vacancies_to_file(vacancies)
        elif need_action == 2:
            vacancies = sort_vacancies(vacancies)
            show_vacancies(vacancies)
            continue
        else:
            continue
