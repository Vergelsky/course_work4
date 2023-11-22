import datetime


class Vacancy:
    def __init__(self, date, title, employer, salary_min, salary_max, description, url):
        self.date = date
        self.title = title
        self.employer = employer
        self.description = description
        self.url = url

        if salary_min:
            if salary_max:
                # если указаны от и до - устанавливаем среднее арифметическое
                self.salary = (salary_min + salary_max) // 2
        # если есть только одна из них - устанавливаем её
            else:
                self.salary = salary_min
        else:
            self.salary = salary_max

    def __str__(self):
        return f"Вакансия {self.title}, " \
               f"зарплата: {self.salary}, " \
               f"дата публикации: {datetime.datetime.fromtimestamp(self.date)}"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary
