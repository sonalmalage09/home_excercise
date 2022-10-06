from client import get_employees


def test_add_employee():
	pass


def test_delete_inexistent_employee():
	pass


def test_delete_employee():
	pass


def test_add_employee_with_existing_id():
	pass


def test_get_all_employees():
	employees = get_employees()
	assert employees[0].name == "Menny"
	assert employees[1].title == "Developer"
