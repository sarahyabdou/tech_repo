# tech_repo



 Overview  
This is a FastAPI backend for managing real estate and hr module , with PostgreSQL as the database and authentication using Basic Auth.

.Technologies Used. 

FastAPI (Backend framework)

PostgreSQL (Database)

SQLAlchemy (ORM)

Alembic (Database migrations)

Uvicorn (ASGI Server)

dotenv (Environment variable management)


 Installation
1️⃣ Clone the Repository

git clone https://github.com/yourusername/repository-name.git

cd repository-name

2️⃣ Create & Activate Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create a .env file and add the following:


DATABASE_URL=postgresql://your_user:your_password@localhost:5432/tech

🔄 Database Setup

Run Alembic Migrations

alembic upgrade head
 Running the API


uvicorn app.main:app --reload

 Authentication

All routes are protected, meaning only authenticated users can access them.

Uses Basic Authentication (username & password).

Ensure your request includes valid credentials in the headers.
<<
This API uses Basic Authentication.

 Real estate  Endpoints

Method	Endpoint	GET	/real_estate/leads/	View All Leads

POST	/real_estate/leads/	Add a Lead

PUT	/real_estate/leads/{lead_id}/assign/	        Assign a Lead

PUT	/real_estate/leads/{lead_id}	         Edit a Lead

DELETE	/real_estate/leads/{lead_id}	     Delete a Lead

GET	/real_estate/leads/{lead_id}	    View a Lead

POST	/real_estate/leads/{lead_id}/calls	    Create a Call

POST	/real_estate/leads/{lead_id}/meetings	Create a Meeting

Employee Management

hr	Endpoint	Description

GET	/hr/	View all employees

POST	/hr/	Add a new employee

PUT	/hr/{employee_id}	Edit an employee

DELETE	/hr/{employee_id}	Delete an employee

Salary Management
Method	Endpoint	Description

POST	/hr/{employee_id}/salaries	   Add salary for an employee

PUT	/hr/{employee_id}/salaries/{due_year}/{due_month}	 Edit salary

