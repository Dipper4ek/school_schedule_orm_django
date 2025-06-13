import django_setup
from schedule_app.models import Subject, Teacher, Class, Student

Subjects = {}
Classes = {}

while True:
    print('\n--- MENU ---')
    print('1. Add Teacher to Subject')
    print('2. Add Student to Class')
    print('3. Get All Students from Class')
    print('4. Get All Teachers from Subject')
    print('5. Get Table (Summary)')
    print('6. Add Subject')
    print('7. Add Class')
    print('0. EXIT')

    n = input('Number: ').strip()

    if n == '1':
        if not Subjects:
            subject = input('Enter subject name: ').strip().lower().replace(" ", "")
            Subjects[subject] = Subject.objects.create(name=subject)

        print('\nAvailable subjects:')
        for key in Subjects:
            print(f"- {key}")

        subject_key = input('Choose subject: ').strip().lower().replace(" ", "")
        if subject_key not in Subjects:
            print("Subject not found!")
            continue

        teacher_name = input('Teacher name: ').strip()
        Teacher.objects.create(name=teacher_name, subject=Subjects[subject_key])
        print(f'Successfully added teacher "{teacher_name}" to subject "{subject_key}".')

    elif n == '2':
        if not Classes:
            class_name = input('Enter class name: ').strip().upper().replace(" ", "")
            Classes[class_name] = Class.objects.create(name=class_name)

        print('\nAvailable classes:')
        for key in Classes:
            print(f"- {key}")

        class_key = input('Choose class: ').strip().upper().replace(" ", "")
        if class_key not in Classes:
            print("Class not found!")
            continue

        student_name = input('Student name: ').strip()
        Student.objects.create(name=student_name, student_class=Classes[class_key])
        print(f'Successfully added student "{student_name}" to class "{class_key}".')

    elif n == '3':
        print('\nAvailable classes:')
        for key in Classes:
            print(f"- {key}")

        class_key = input('Choose class: ').strip().upper().replace(" ", "")
        if class_key not in Classes:
            print("Class not found!")
            continue

        students = Student.objects.filter(student_class=Classes[class_key])
        print(f"\nStudents in class {class_key}:")
        for student in students:
            print(f"- {student.name}")

    elif n == '4':
        print('\nAvailable subjects:')
        for key in Subjects:
            print(f"- {key}")

        subject_key = input('Choose subject: ').strip().lower().replace(" ", "")
        if subject_key not in Subjects:
            print("Subject not found!")
            continue

        teachers = Teacher.objects.filter(subject=Subjects[subject_key])
        print(f"\nTeachers for subject {subject_key}:")
        for teacher in teachers:
            print(f"- {teacher.name}")

    elif n == '5':
        print('\n--- SUMMARY TABLE ---')
        print('Subjects:')
        for subject in Subject.objects.all():
            print(f"- {subject.name}")
        print('\nTeachers:')
        for teacher in Teacher.objects.all():
            print(f"- {teacher.name} teaches {teacher.subject.name}")
        print('\nClasses:')
        for cls in Class.objects.all():
            print(f"- {cls.name}")
        print('\nStudents:')
        for student in Student.objects.all():
            print(f"- {student.name} in class {student.student_class.name}")

    elif n == '6':
        subject = input('Enter new subject name: ').strip().lower().replace(" ", "")
        if subject in Subjects:
            print("Subject already exists!")
        else:
            Subjects[subject] = Subject.objects.create(name=subject)
            print(f"Added subject: {subject}")

    elif n == '7':
        class_name = input('Enter new class name: ').strip().upper().replace(" ", "")
        if class_name in Classes:
            print("Class already exists!")
        else:
            Classes[class_name] = Class.objects.create(name=class_name)
            print(f"Added class: {class_name}")

    elif n == '0':
        print("Exiting...")
        break

    else:
        print("Invalid option. Please try again.")
