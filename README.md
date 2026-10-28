# StockFlow — Smart Inventory Management System

StockFlow is a web-based inventory management application built with Django and PostgreSQL. It helps organizations manage products, monitor stock levels, and maintain inventory information through a simple, user-friendly interface.

## 🚀 Live Demo

**Live Application:** https://stockflow-mvp-c7ib.onrender.com

## ✨ Features

- **User Authentication:** User registration and login.
- **Organization Isolation:** Users can access their own organization's inventory.
- **Dashboard:** View inventory summaries and low-stock information.
- **Product Management:** Add, view, edit, and delete products.
- **Product Search:** Find products quickly.
- **Low-Stock Monitoring:** Identify products that need replenishment.
- **Organization Settings:** Configure inventory-related settings.
- **Responsive Interface:** Clean interface for inventory management.

## 🛠️ Technologies Used

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- Bootstrap
- Git and GitHub
- Render

## 📁 Project Structure

```text
stockflow-mvp/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── inventory/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── registration/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   ├── products.html
│   ├── product_form.html
│   └── settings.html
├── manage.py
├── requirements.txt
└── README.md
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/KalugotlaSairam/stockflow-mvp.git
cd stockflow-mvp
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## 🔐 Security

Production configuration should use environment variables for secret keys and database credentials. Debug mode should be disabled in production.

## 👨‍💻 Author

**Kalugotla Sairam**

GitHub: https://github.com/KalugotlaSairam

---

*StockFlow MVP — Smart and simple inventory management.*