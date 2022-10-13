import json
import random
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from ApiException import ApiException

app = FastAPI()


class Employee(BaseModel):
    name: str
    id: int
    title: str
    salary: float


class Developer(Employee):
    title = "Developer"


@app.post("/employees")
def add_employee(name: str, title: str, salary: float):
    """
    :type salary: object
    :param name:
    :param title:
    :param salary:
    :return:
    """
    with open("entities.json", "r") as file:
        content = json.load(file)
        file.close()
        empId = random.randint(1, 1000)
        content[name] = {"id": empId, "title": title, "salary": salary}
    try:
        with open("entities.json", "w") as file:
            json.dump(content, file)
            file.close()
    except Exception as e:
        raise ApiException("Failed while adding a new employee.", e.__cause__)


@app.post("/employees/file")
def receive_file(file: UploadFile = File(...)):
    """
    :param file: containing Employee details,new record is created
    :return: Successful message
    """
    try:
        contents = json.load(file.file)
        for key, values in contents.items():
            add_employee(name=key, title=values['title'], salary=float(values['salary']))
    except Exception as e:
        raise ApiException("Failed while adding a new employee from file.", e.__cause__)
    return 'File uploaded successfully'


@app.get("/employees")
def get_employees(criteria: str = None) -> List[Employee]:
    """
    :param criteria: filter is performed based on the value passed to request
    :return:
    """
    try:
        result = __getEmployees(criteria)
        employees = []
        for (key, values) in result.items():
            employees.append(Employee(name=key, id=values['id'], title=values['title'], salary=float(values['salary'])))
    except Exception as e:
        raise ApiException("Failed while getting employee details.", e.__cause__)
    return employees


def __getEmployees(criteria: str = None):
    """
    :param criteria:
    :return:
    """
    result = {}
    with open("entities.json", "r") as file:
        content = json.load(file)
        file.close()
    if criteria is not None:
        found = False
        for key, values in content.items():
            if key == criteria:
                found = True
                result.update({key: values})
        if not found:
            for key, values in content.items():
                for eachKey in values.keys():
                    if str(values[eachKey]) == criteria:
                        result.update({key: values})
    else:
        result = content
    return result


@app.delete("/employees/{name}")
def delete_employees(name: str):
    """
    :param name: Based on the name of the employee passed. record will be deleted
    :return:
    """
    try:
        employees = __getEmployees()
        del employees[name]
        with open("entities.json", "w") as file:
            json.dump(employees, file)
            file.close()
            return f'(Employee: {name} is successfully deleted)'
    except ApiException as e:
        raise Exception("Failed while deleting a employee.")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
