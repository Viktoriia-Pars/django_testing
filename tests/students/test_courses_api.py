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
    assert data[0]['students'] == 1
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



# @pytest.mark.django_db
# def test_create_message(client, user):
#     count = Message.objects.count()
#
#     response = client.post('/messages/', data={'user': user.id, 'text': 'test text'})
#
#     assert response.status_code == 201
#     assert Message.objects.count() == count + 1
