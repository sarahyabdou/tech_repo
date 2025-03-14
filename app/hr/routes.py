from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import EmployeesInfo,EmployeesSalaries,CompanyInfo,UserInfo
from app.auth import get_current_user
from app.schemas import EmployeeCreate,SalaryCreate,SalaryUpdate,EmployeeUpdate,AllEmployeesResponse,EmployeeResponse
hr_router = APIRouter(dependencies=[Depends(get_current_user)])
@hr_router.post("/")
def add_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),

):

    company = db.query(CompanyInfo).filter(CompanyInfo.company_domain == employee_data.company_domain).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    existing_employee = db.query(EmployeesInfo).filter(
        EmployeesInfo.user_uid == employee_data.user_uid
    ).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Employee with this UUID already exists")


    new_employee = EmployeesInfo(
        company_domain=employee_data.company_domain,
        contact_name=employee_data.contact_name,
        business_phone=employee_data.business_phone,
        personal_phone=employee_data.personal_phone,
        business_email=employee_data.business_email,
        personal_email=employee_data.personal_email,
        gender=employee_data.gender,
        is_company_admin=employee_data.is_company_admin,
        user_uid=employee_data.user_uid
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Employee added successfully", "employee": new_employee}

@hr_router.post("/{employee_id}/salaries")
def add_salary(
    employee_id: int,
    salary_data: SalaryCreate,
    db: Session = Depends(get_db),
):

    employee = db.query(EmployeesInfo).filter(
        EmployeesInfo.company_domain == salary_data.company_domain,
        EmployeesInfo.employee_id == employee_id
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")


    new_salary = EmployeesSalaries(
        company_domain=salary_data.company_domain,
        employee_id=employee_id,
        gross_salary=salary_data.gross_salary,
        insurance=salary_data.insurance,
        taxes=salary_data.taxes,
        net_salary=salary_data.net_salary,
        due_year=salary_data.due_year,
        due_month=salary_data.due_month,
        due_date=salary_data.due_date
    )

    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)

    return {"message": "Salary added successfully", "salary": new_salary}
@hr_router.put("/{employee_id}")
def edit_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    employee = db.query(EmployeesInfo).filter(EmployeesInfo.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee_data.dict(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return {"message": "Employee updated successfully", "employee": employee}

@hr_router.put("/{employee_id}/salaries/{due_year}/{due_month}")
def edit_salary(
    employee_id: int,
    due_year: int,
    due_month: int,
    salary_data: SalaryUpdate,
    db: Session = Depends(get_db)
):

    salary = db.query(EmployeesSalaries).filter(
        EmployeesSalaries.employee_id == employee_id,
        EmployeesSalaries.due_year == due_year,
        EmployeesSalaries.due_month == due_month
    ).first()
    if not salary:
        raise HTTPException(status_code=404, detail="Salary record not found")



    for key, value in salary_data.dict(exclude_unset=True).items():
        setattr(salary, key, value)

    db.commit()
    db.refresh(salary)

    return {"message": "Salary updated successfully", "salary": salary}
@hr_router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(EmployeesInfo).filter(EmployeesInfo.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")


    db.query(EmployeesSalaries).filter(
        EmployeesSalaries.company_domain == employee.company_domain,
        EmployeesSalaries.employee_id == employee_id
    ).delete()


    db.delete(employee)
    db.commit()

    return {"message": "Employee and related salary records deleted successfully"}
@hr_router.get("/", response_model=AllEmployeesResponse)
def view_all_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(EmployeesInfo).all()


    employees_response = [
        EmployeeResponse(
            employee_id=employee.employee_id,
            company_domain=employee.company_domain,
            contact_name=employee.contact_name,
            business_phone=employee.business_phone,
            personal_phone=employee.personal_phone,
            business_email=employee.business_email,
            personal_email=employee.personal_email,
            gender=employee.gender,
            is_company_admin=employee.is_company_admin,
            user_uid=str(employee.user_uid),
            salaries=[]
        )
        for employee in employees
    ]

    return AllEmployeesResponse(employees=employees_response)