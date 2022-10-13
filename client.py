import json
from typing import List

import requests
from pydantic import parse_obj_as

from ApiException import ApiException
from server import Employee

url = 'http://localhost:8000/employees'


def checkServer():
    try:
        response = requests.get(url)
    except Exception as e:
        raise f'Failed: '.format(e)
    return response.status_code


def add_employee_from_file(file_path: str):
    try:
        files = {'file': open(file_path, "rb")}
        response = requests.post(url + '/file', files=files)
    except Exception as e:
        raise f'Failed: '.format(e)
    return response.json()


def add_employee(name: str, title: str, salary: float):
    try:
        newURL = url + "?name=" + name + "&title=" + title + "&salary=" + str(salary)
        response = requests.post(newURL)
    except Exception as e:
        raise f'Failed: '.format(e)
    return response


def get_employees(criteria: str = None) -> List[Employee]:
    newUrl = url
    try:
        try:
            if criteria is not None:
                newUrl = url + "?criteria=" + criteria
        except:
            raise f"As criteria is None, API cannot be called"
        res = requests.get(newUrl)
        return parse_obj_as(List[Employee], res.json())
    except Exception as e:
        raise f'Failed: '.format(e)


def delete_employees(name: str = None):
    newUrl = url + "/" + name
    try:
        res = requests.delete(newUrl)
        print(res.json())
    except ApiException as e:
        raise f'Failed: '.format(e)
    return res.json()


def getJsonFile(file):
    val = []
    try:
        with open(file, "r") as testFile:
            testData = json.load(testFile)
        for i, j in testData.items():
            name = i
            title = j['title']
            salary = j["salary"]
            id = j['id']
            val.append([name, title, salary, id])
        testFile.close()
    except Exception as e:
        raise f'Failed: '.format(e)
    return val
