# 📄 Description
Breaking Budget is a web application for expense management developed with Django. The application allows managing travel expenses with two types of roles: administrators and travelers. Administrators can create and manage traveler users, while travelers can register their expenses and manage them according to their status. The system implements a complete authentication and authorization flow, with different permissions based on user role.

# 💻 Technologies Used
- **Django 5.2.6 (LTS)**: Python web framework for backend
- **Python 3.11.5**: Base programming language
- **SQLite**: Lightweight database for development
- **HTML/CSS**: For user interface
- **Pyenv**: Python version manager
- **Pytest**: Testing framework

# 📋 Requirements
- Python 3.11.5 (recommended to use pyenv)
- pip (Python package manager)
- Virtualenv or equivalent virtual environment
- Git (to clone the repository)

# 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/username/breaking-budget.git
```

2. Navigate to the project directory:
```bash
cd breaking-budget
```

3. Create and activate virtual environment:
```bash
pyenv virtualenv 3.11.5 breaking-budget-env
pyenv activate breaking-budget-env
```

5. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

6. Run database migrations:
```bash
python manage.py migrate
```

# 🗄️ Database Population

## Create test data:

### 1. Create test users:
```bash
python manage.py create_initial_users
```

### 2. Create test expenses:
```bash
python manage.py create_initial_expenses
```

## Delete previous data if needed:

### 1. Erase all users:
```bash
python manage.py shell -c "from users.models import CustomUser; CustomUser.objects.all().delete()"
```

### 2. Erase all expenses:
```bash
python manage.py shell -c "from expenses.models import Expense; Expense.objects.all().delete()"
```

# ▶️ Execution

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application:
   - Open your browser and go to `http://127.0.0.1:8000/login/`

3. Create an account or log in:
   - Register as a new user or use the test data (see Database Population section)

4. Explore the functionalities based on your role:
   - **Travelers**: Add, edit, and delete pending expenses; change password
   - **Admins**: Manage travelers, update expense status, manage own expenses and password

# 🏗️ Project Structure
The project follows Django's MVC architecture and is organized as follows:

**Apps:**
- **users**: User management, authentication, and roles
- **expenses**: Expense management and status tracking

**Main Features:**
- User authentication and authorization
- Role-based permissions (Admin and Traveler)
- Expense and User CRUD operations
- Password management for all users

# 🧪 Testing

Run tests using pytest from the main project directory:
```bash
pytest
```

This will run all test suites and provide coverage information.

# 🌐 Deployment
This project is designed for academic and learning purposes. No production deployment configuration is included.

# 🤝 Contributions
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch:
```bash
git checkout -b feature/NewFeature
```
3. Make your changes and commit:
```bash
git commit -m "Add New Feature"
```
4. Push changes to your repository:
```bash
git push origin feature/NewFeature
```
5. Create a pull request

# 📝 License
This project is developed for educational purposes.

# 👥 User Roles and Permissions

## Administrator
- **User Management**: Create and delete traveler accounts
- **Data Management**: Edit all traveler information (except passwords)
- **Expense Oversight**: Update status of all expenses when status is pending
- **Personal Account**: Create and manage own expenses, edit own password

## Traveler
- **Expense Management**: Add expenses. Edit and delete own expenses when status is pending
- **Account Management**: Edit own password
- **Limited Access**: Cannot access admin functionalities or other users' data

## Authentication
- Secure login system for all users
- Password protection and management
- Role-based access control throughout the application