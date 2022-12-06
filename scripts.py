import random
from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation


def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=name).get()
        return schoolkid
    except Schoolkid.DoesNotExist:
        raise DoesNotExist('Такого ученика нет, проверьте правильность имени')
    except Schoolkid.MultipleObjectsReturned:
        raise MultipleObjectsReturned('Найдено несколько учеников, уточните ФИО')


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject, text='Хвалю!'):
    try:
        subject = Subject.objects.filter(title=subject, year_of_study=6)[0]
    except IndexError:
        print('Проверьте правильность названия предмета и введите команду повторно')
        return
    lessons = Lesson.objects.filter(
        year_of_study=6, group_letter='А', subject=subject)
    lesson = lessons[random.randint(0, len(lessons))]
    date = lesson.date
    teacher = lesson.teacher
    Commendation.objects.create(text=text,
                                created=date,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=teacher)
    
