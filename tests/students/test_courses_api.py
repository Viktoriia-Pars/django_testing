import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course
from students.serializers import CourseSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory



@pytest.mark.django_db
def test_get_course(client, user):
    # Arrange
    cours1 = Course.objects.create(name='Math')
    cours2 = Course.objects.create(name='Literature')
    Ivan = Student.objects.create(name= 'Ivan', birth_date='1987-2-21')
    cours2.students.add(Ivan)


    # Act

    response = client.get('/api/v1/courses/')
    response1 = client.get('/api/v1/students/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    data1 = response1.json()
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Math'
    assert data[0]['students'] == list(cours1.students.all())
    assert data1[0]['birth_date'] == '1987-02-21'

@pytest.mark.django_db
def test_get_courses(client, user, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert data[i]['id'] == courses[i].pk
        assert data[i]['name'] == courses[i].name
        assert data[i]['students'] == list(courses[i].students.all())

@pytest.mark.django_db
def test_get_course_filter_id(client, user, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=10)


    # Act
    id_ = courses[0].pk
    name_ = courses[0].name
    response = client.get(f'/api/v1/courses/?name={name_}')
    response1 = client.get(f'/api/v1/courses/{id_}/')

    # Assert
    assert response1.status_code == 200
    data = response.json()
    data1 = response1.json()
    assert len(data) == 1
    assert data1['id'] == id_
    assert data[0]['name'] == name_


@pytest.mark.django_db
def test_create_course(client, user):
    # Arrange
    course_data = {'name': 'History'}
    stud_data = {'name': 'Ivan', 'birth_date':'1987-2-21'}

    # Act

    response = client.post('/api/v1/courses/', data=course_data)
    response1 = client.post('/api/v1/students/', data=stud_data)

    # Assert
    assert response.status_code == 201
    assert response1.status_code == 201
    data = response.json()
    data1 = response1.json()
    assert data['name'] == 'History'
    assert data1['name'] == 'Ivan'
    assert data1['birth_date'] == '1987-02-21'

@pytest.mark.django_db
def test_update_course(client, user, courses_factory, students_factory):
    # Arrange
    courses = courses_factory(_quantity=10)
    students = students_factory(_quantity=10)
    course_data = {'name': 'History'}
    stud_data = {'name': 'Ivan', 'birth_date': '1987-02-21'}

    # Act
    id_c = courses[3].pk
    id_s = students[3].pk
    response = client.patch(f'/api/v1/courses/{id_c}/', data=course_data)
    response1 = client.patch(f'/api/v1/students/{id_s}/', data=stud_data)

    # Assert
    assert response.status_code == 200
    assert response1.status_code == 200
    data = response.json()
    data1 = response1.json()
    assert data['name'] == 'History'
    assert data1['name'] == 'Ivan'
    assert data1['birth_date'] == '1987-02-21'

@pytest.mark.django_db
def test_delete_course(client, user, courses_factory, students_factory):
    # Arrange
    courses = courses_factory(_quantity=10)
    students = students_factory(_quantity=10)

    # Act
    id_c = courses[5].pk
    id_s = students[5].pk
    response = client.delete(f'/api/v1/courses/{id_c}/')
    response1 = client.delete(f'/api/v1/students/{id_s}/')

    # Assert
    assert response.status_code == 204
    assert response1.status_code == 204