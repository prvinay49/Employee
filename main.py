from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from database import (
    add_employee,
    retrieve_employees,
    retrieve_employee,
    delete_employee,
    greet_employee
)


class EmployeeSchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    doj: str = Field(...)
    dob: str = Field(...)
    aadhaar: str = Field(...)


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


app = FastAPI(
    title="Employee information",
    version="1.0.0",
    docs_url="/",
    redoc_url="/docs"
)


@app.post("/addEmployee", response_description="Employee data added into the database")
async def add_employee_data(employee: EmployeeSchema = Body(...)):
    employee = jsonable_encoder(employee)
    new_employee = await add_employee(employee)
    return ResponseModel(new_employee, "Employee added successfully.")


@app.get("/getAllEmployees", response_description="Employees retrieved")
async def get_employees():
    employees = await retrieve_employees()
    if employees:
        return ResponseModel(employees, "Employees data retrieved successfully")
    return ResponseModel(employees, "Empty list returned")


@app.get("/getEmployee/{id}", response_description="Employee data retrieved")
async def get_employee_data(id):
    employee = await retrieve_employee(id)
    if employee:
        return ResponseModel(employee, "Employee data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Employee doesn't exist.")


@app.delete("/deleteEmployee/{id}", response_description="Employee data deleted from the database")
async def delete_employee_data(id: str):
    deleted_employee = await delete_employee(id)
    if deleted_employee:
        return ResponseModel(
            "Employee with ID: {} removed".format(id), "Employee deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Employee with id {0} doesn't exist".format(id)
    )


@app.get("/greetEmployees")
async def greet_employees():
    valid_employees_for_greeting = await greet_employee("WORK_ANNIVERSARY")
    if valid_employees_for_greeting:
        return ResponseModel(valid_employees_for_greeting, "Congratulations on your work anniversary")
    return ResponseModel(valid_employees_for_greeting, "No one completed year by today")


@app.get("/wishEmployees")
async def wish_employees():
    valid_employees_for_wishes = await greet_employee("BIRTHDAY")
    if valid_employees_for_wishes:
        return ResponseModel(valid_employees_for_wishes, "Many more happy returns of the day")
    return ResponseModel(valid_employees_for_wishes, "No Birthdays for today")