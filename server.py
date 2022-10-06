import json
import random
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Employee(BaseModel):
    name: str
    id: int
    title: str


class Developer(Employee):
    title = "Developer"


@app.post("/employees")
def add_employee(name: str, title: str, salary: int):
    with open("entities.json", "w") as file:
        content = json.load(file)
        id = random.randint(1, 1000)
        content[name] = {"title": title, "salary": salary, "id": id}
    

@app.get("/employees")
def get_employees(filter: str) -> dict:
    with open("entities.json", "r") as file:
        content = json.load(file)
    return content


@app.delete("/employees")
def delete_employees(name: str):
    employees = get_employees()
    del employees[name]
    with open("entities.json", "w") as file:
        json.dump(employees, file)
    

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
