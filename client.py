from typing import List
import requests
from pydantic import parse_obj_as
from server import Employee


url = "http://0.0.0.0:8000/employees"


def add_employee_from_file(file_path: str):
	files = {'upload_file': open(file_path, "rb")}
	response = requests.post(url, files=files)
	
	
def get_employees() -> List[Employee]:
	return parse_obj_as(List[Employee], requests.get(url))