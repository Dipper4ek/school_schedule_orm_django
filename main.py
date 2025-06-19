import django
import os
from datetime import datetime, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_schedule.settings')
django.setup()

from schedule_app.models import Subject, Teacher, Class, Student, Schedule, Grade

DAY_CHOICES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Введіть непорожнє значення!")

def add_subject():
    name = input_non_empty("Назва предмета: ")
    description = input("Опис предмета (можна пропустити): ").strip()
    if Subject.objects.filter(name=name).exists():
        print("Такий предмет вже існує!")
        return
    Subject.objects.create(name=name, description=description)
    print("Предмет додано!")

def add_teacher():
    first_name = input_non_empty("Ім'я вчителя: ")
    last_name = input_non_empty("Прізвище вчителя: ")
    name = input_non_empty("Предмет (назва): ")
    try:
        subject = Subject.objects.get(name=name)
    except Subject.DoesNotExist:
        print("Такого предмета не існує!")
        return
    Teacher.objects.create(first_name=first_name, last_name=last_name, subject=subject)
    print("Вчителя додано!")

def add_class():
    name = input_non_empty("Назва класу: ")
    year_str = input_non_empty("Рік навчання (число): ")
    try:
        year = int(year_str)
        if year < 1:
            raise ValueError
    except ValueError:
        print("Рік навчання повинен бути додатнім числом!")
        return
    if Class.objects.filter(name=name).exists():
        print("Такий клас вже існує!")
        return
    Class.objects.create(name=name, year=year)
    print("Клас додано!")

def add_student():
    first_name = input_non_empty("Ім'я учня: ")
    last_name = input_non_empty("Прізвище учня: ")
    class_name = input_non_empty("Клас (назва): ")
    try:
        student_class = Class.objects.get(name=class_name)
    except Class.DoesNotExist:
        print("Такого класу не існує!")
        return
    Student.objects.create(first_name=first_name, last_name=last_name, student_class=student_class)
    print("Учня додано!")

def add_schedule():
    day = input_non_empty("День тижня (Mon, Tue, Wed, Thu, Fri, Sat, Sun): ")
    if day not in DAY_CHOICES:
        print("Некоректний день тижня!")
        return
    start_time_str = input_non_empty("Час початку (HH:MM, 24-годинний формат): ")
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
    except ValueError:
        print("Некоректний формат часу!")
        return

    subject_name = input_non_empty("Предмет (назва): ")
    class_name = input_non_empty("Клас (назва): ")
    teacher_lastname = input_non_empty("Прізвище вчителя: ")

    try:
        subject = Subject.objects.get(name=subject_name)
    except Subject.DoesNotExist:
        print("Такого предмета немає!")
        return

    try:
        student_class = Class.objects.get(name=class_name)
    except Class.DoesNotExist:
        print("Такого класу немає!")
        return

    # Вчителя шукаємо за прізвищем і предметом
    teachers = Teacher.objects.filter(last_name=teacher_lastname, subject=subject)
    if not teachers.exists():
        print("Вчителя з таким прізвищем та предметом не знайдено!")
        return
    if teachers.count() > 1:
        print("Знайдено кілька вчителів з таким прізвищем та предметом. Використано першого.")
    teacher = teachers.first()

    Schedule.objects.create(day_of_week=day, start_time=start_time, subject=subject,
                            student_class=student_class, teacher=teacher)
    print("Заняття додано!")

def add_grade():
    student_lastname = input_non_empty("Прізвище учня: ")
    student_firstname = input_non_empty("Ім'я учня: ")
    subject_name = input_non_empty("Предмет (назва): ")

    try:
        student = Student.objects.get(first_name=student_firstname, last_name=student_lastname)
    except Student.DoesNotExist:
        print("Учня не знайдено!")
        return

    try:
        subject = Subject.objects.get(name=subject_name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено!")
        return

    grade_str = input_non_empty("Оцінка (число): ")
    try:
        grade_val = int(grade_str)
        if not (1 <= grade_val <= 12):
            print("Оцінка має бути в межах 1-12!")
            return
    except ValueError:
        print("Оцінка має бути числом!")
        return

    date_str = input("Дата (YYYY-MM-DD), або пусто для сьогодні: ").strip()
    if date_str:
        try:
            date_val = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Некоректний формат дати!")
            return
    else:
        date_val = datetime.today().date()

    Grade.objects.create(student=student, subject=subject, grade=grade_val, date=date_val)
    print("Оцінка додана!")

def main():
    while True:
        print('''
--- МЕНЮ ---
1. Додати предмет
2. Додати вчителя
3. Додати клас
4. Додати учня
5. Додати заняття в розклад
6. Додати оцінку
0. Вихід
        ''')
        choice = input("Оберіть дію: ").strip()
        if choice == '1':
            add_subject()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            add_class()
        elif choice == '4':
            add_student()
        elif choice == '5':
            add_schedule()
        elif choice == '6':
            add_grade()
        elif choice == '0':
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == '__main__':
    main()
