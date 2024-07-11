import pytest
from model_bakery import baker
from rest_framework import status
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.test import APIClient
from django.urls import reverse
from students.models import Course, Student



@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def settings_with_max_students(settings):
    return settings.MAX_STUDENTS_PER_COURSE


# проверка получения первого курса (retrieve-логика):
@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory(_quantity=1)[0]
    response = api_client.get(reverse('courses-detail', args=[course.id]))
    assert response.status_code == 200
    assert response.data['name'] == course.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    response = api_client.get(reverse('courses-list'))
    assert response.status_code == 200
    assert len(response.data) == len(courses)


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    course_id = courses[1].id
    response = api_client.get(reverse('courses-list'), data={'id': course_id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course_id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    courses = course_factory(_quantity=3)
    course_name = courses[1].name
    response = api_client.get(reverse('courses-list'), data={'name': course_name})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course_name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(api_client):
    course_data = {'name': 'Test Course'}
    response = api_client.post(reverse('courses-list'), data=course_data)
    assert response.status_code == 201
    assert Course.objects.filter(name='Test Course').exists()


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory()
    updated_data = {'name': 'Updated Course'}
    response = api_client.put(reverse('courses-detail', args=[course.id]), data=updated_data)
    assert response.status_code == 200
    assert Course.objects.get(id=course.id).name == 'Updated Course'


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    response = api_client.delete(reverse('courses-detail', args=[course.id]))
    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()





@pytest.mark.django_db
@pytest.mark.parametrize('num_students, expected_status', [
    (20, status.HTTP_200_OK),  # успешное добавление 20 студентов
    (21, status.HTTP_200_OK),  # попытка добавить 21 студента
])
def test_max_students_per_course(settings_with_max_students, api_client, course_factory, student_factory, num_students, expected_status):
    course = course_factory()

    for _ in range(num_students):
        student = student_factory()
        response = api_client.patch(reverse('courses-detail', args=[course.id]), data={'student_id': student.id})

    if num_students > settings_with_max_students:
        assert response.status_code == expected_status
        assert f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}" in response.data.get('error', '')

    else:
        assert response.status_code == expected_status


# Ограничить число студентов на курсе
@pytest.mark.django_db
@pytest.mark.parametrize('num_students, expected_status', [
    (settings.MAX_STUDENTS_PER_COURSE, False),
    (settings.MAX_STUDENTS_PER_COURSE + 1, True),
])
def test_max_students_per_course(settings_with_max_students, api_client, course_factory, student_factory, num_students, expected_status):
    course = course_factory(_quantity=1)[0]
    students = student_factory(_quantity=num_students)
    course.students.add(*students)

    if expected_status:
        with pytest.raises(ValidationError, match=f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}"):
            course.clean()
    else:
        course.clean()
