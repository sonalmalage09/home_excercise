import pytest

from client import get_employees, add_employee_from_file, delete_employees, getJsonFile


@pytest.mark.order1
def test_add_employee():
    try:
        add_employee_from_file("test_files.json")
        employees = get_employees()
        data = getJsonFile("test_files.json")
        assert employees[len(employees) - 1].name == data[0][0]
        assert employees[len(employees) - 1].title == data[0][1]
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def test_get_all_employees():
    try:
        data = getJsonFile("entities.json")
        employees = get_employees()
        assert employees[0].name == data[0][0]
        assert employees[1].title == data[0][1]
        pytest.ra
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


@pytest.mark.run(after="test_add_employee")
def test_delete_employee():
    try:
        name = getJsonFile("test_files.json")
        delete_employees(name[0][0])
        employees = get_employees(name)
        assert len(employees) == 0, " Employee is not deleted"

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


@pytest.mark.run(after='test_delete_employee')
def test_delete_inexistent_employee():
    employees = get_employees("Sunil")
    try:
        assert len(employees) == 0, " Employee doesnt exists"
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def test_get_all_employees_by_SearchCriteria():
    data = getJsonFile("entities.json")
    try:
        nameSearch = get_employees(data[0][0])
        titleSearch = get_employees(data[0][1])
        idSearch = get_employees(data[0][3])
        assert nameSearch[0].name == data[0][0]
        assert titleSearch[0].title == data[0][1]
        assert idSearch[0].id == data[0][3]
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


@pytest.mark.parametrize("invalidVal", ["Monkey", "100", "Coder", "-9999"])
def test_search_InvalidDetails(invalidVal):
    try:
        searchRes = get_employees(invalidVal)
        assert len(searchRes) == 0
    except Exception as e:
        print(e.__class__)

