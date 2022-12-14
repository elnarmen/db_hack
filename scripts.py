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
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject, text='Хвалю!'):
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    subject = Subject.objects.filter(title=subject, year_of_study=year_of_study).first()
    if not subject:
        print('Проверьте правильность названия предмета и введите команду повторно')
        return
    lessons = Lesson.objects.filter(year_of_study=year_of_study,
                                    group_letter=group_letter,
                                    subject=subject).order_by('date')
    lesson = random.choice(lessons)
    date = lesson.date
    teacher = lesson.teacher
    Commendation.objects.create(text=text,
                                created=date,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=teacher)
