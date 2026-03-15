💰 Budget Manager API

A personal finance management API built with Django and Django REST Framework.
The application allows users to track their income, expenses, categories, and wallet balance.

This project was built as a backend learning project to practice:

REST API development

database relationships

business logic

financial transaction handling

🚀 Features

✔ User registration and authentication
✔ Automatic wallet creation for every new user
✔ Income and expense transactions
✔ Custom categories per user
✔ Wallet balance tracking
✔ Dashboard statistics
✔ Last 5 transactions overview
✔ REST API endpoints

🏗 Tech Stack

Python

Django

Django REST Framework

SQLite

Postman (API testing)

📊 Dashboard

The dashboard endpoint returns financial statistics for the logged-in user.

Example response:

{
  "current_balance": 1200,
  "total_expenses": 350,
  "total_income": 1550,
  "last_5_transactions": [
    {
      "id": 10,
      "type": "EXPENSE",
      "amount": 25,
      "category": "Food",
      "description": "Lunch",
      "created_at": "2026-03-15"
    }
  ]
}
🗄 Database Models
User

Custom Django user model.

Each user automatically receives a wallet after registration.

Wallet

Represents the user's financial account.

Fields:

user

current_balance

created_at

Relationship:

User → OneToOne → Wallet

Category

Categories belong to a specific user.

Examples:

Salary

Food

Transport

Entertainment

Fields:

name

type (INCOME / EXPENSE)

user

Transaction

Represents financial activity in the wallet.

Fields:

wallet

type (INCOME / EXPENSE)

amount

category

description

created_at

Relationships:

Wallet → OneToMany → Transactions
Category → OneToMany → Transactions

🔌 API Endpoints

Base URL:

http://127.0.0.1:8000/api/
Wallet API
Get wallets
GET /api/wallets/

Returns the wallet belonging to the authenticated user.

Transaction API
Get all transactions
GET /api/transactions/

Returns all transactions for the user wallet.

Create transaction
POST /api/transactions/

Example request:

{
  "type": "EXPENSE",
  "amount": 25,
  "category": 2,
  "description": "Lunch"
}
Get single transaction
GET /api/transactions/{id}/
Update transaction
PUT /api/transactions/{id}/
Delete transaction
DELETE /api/transactions/{id}/
Dashboard API
Get dashboard statistics
GET /api/stats/dashboard/

Returns:

wallet balance

total income

total expenses

last 5 transactions

⚙️ Installation

Clone the repository

git clone https://github.com/yourusername/budget-manager.git

Move into project folder

cd budget-manager

Create virtual environment

python -m venv venv

Activate environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Apply migrations

python manage.py migrate

Create superuser (optional)

python manage.py createsuperuser

Run development server

python manage.py runserver

Server will start at:

http://127.0.0.1:8000
🧪 Testing

You can test the API using:

Postman

Django Admin

Curl

Browser (for GET endpoints)

📁 Project Structure
budget_manager/
│
├── users/            # Custom user model
├── tracker/          # Wallet, transactions, categories
├── serializers.py
├── views.py
├── models.py
├── urls.py
│
├── manage.py
└── settings.py
🔮 Future Improvements

Planned improvements:

Monthly statistics

Category expense charts

Budget limits per category

Export reports

Frontend (React or Vue)

Authentication tokens (JWT)

👨‍💻 Author

Backend project created for practicing:

Django

REST APIs

database design

backend architecture