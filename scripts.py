def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=name).get()
        return schoolkid
    except ObjectDoesNotExist:
        print('Такого ученика нет')
    except MultipleObjectsReturned:
        print('Найдено несколько имен')
    return


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    subject = Subject.objects.filter(title=subject, year_of_study=6)[0]
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject=subject)[0]
    date = lesson.date
    teacher = lesson.teacher
    Commendation.objects.create(text='Хвалю!',
                                created=date,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=teacher)
