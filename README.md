# 🎓 Student Portal & Academic Analytics

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Analytics](https://img.shields.io/badge/Powered%20By-quickgraph--darius12-orange.svg)](https://test.pypi.org/project/quickgraph-darius12/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Student__portal-black.svg)](https://github.com/NIYONKURU-DARIUS/Student_portal)

A modern Django web application designed for comprehensive student academic record management and visual data analytics. The system integrates full **CRUD operations**, role-based permission control, and embedded **analytics visualizations** powered by the custom package [`quickgraph-darius12`](https://test.pypi.org/project/quickgraph-darius12/).

---

## 🚀 Key Features

### 1. 📋 Student Record Management (CRUD)
- **Create (`/students/add/`)**: Add new student profiles with registration numbers, courses, study hours, and academic marks.
- **Read / Directory (`/students/`)**: Clean dashboard listing all students with real-time search, course filters, and academic performance status badges.
- **Update (`/students/edit/<id>/`)**: Edit student records with pre-populated forms and validation.
- **Delete (`/students/delete/<id>/`)**: Safe deletion protected by a confirmation interface.

### 2. 📊 Visual Academic Analytics (`quickgraph-darius12`)
The application embeds graphs dynamically generated on the server using `quickgraph-darius12`:
- 🥧 **Pie Chart (`pie_graph`)**: Enrollment distribution categorized by academic course/major.
- 📊 **Bar Chart (`bar_graph`)**: Comparative average marks across departments.
- 🔵 **Scatter Plot (`scatter_graph`)**: Correlation analysis between weekly study hours and student exam marks.
- 📈 **Line Plot (`line_graph`)**: Sequential student score trajectories and performance benchmarks.

### 3. 🔐 Security & Roles
- Built-in user authentication and role management (`setup_roles` command).
- Granular permissions and custom decorators to secure sensitive actions.

---

## 🛠️ Project Structure

```text
student_portal/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── media/
│   └── graphs/                 # Server-rendered analytics charts
├── static/
│   ├── css/
│   └── js/
├── student_portal/             # Core project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── students/                   # Main application
    ├── admin.py
    ├── forms.py
    ├── models.py
    ├── graph_utils.py          # QuickGraph integration layer
    ├── views.py
    ├── urls.py
    ├── management/commands/    # Role setup and utility scripts
    └── templates/students/     # Bootstrap 5 responsive templates
```

---

## 💻 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/NIYONKURU-DARIUS/Student_portal.git
cd Student_portal
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple quickgraph-darius12
```

### 4. Apply Migrations & Set Up Roles
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_roles
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Visit the application in your browser:
- **Student Directory**: [http://127.0.0.1:8000/students/](http://127.0.0.1:8000/students/)
- **Visual Analytics Dashboard**: [http://127.0.0.1:8000/students/analytics/](http://127.0.0.1:8000/students/analytics/)
- **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Tests

To execute unit tests:
```bash
python manage.py test students
```

---

## 👤 Author

- **Darius NIYONKURU**
- GitHub: [@NIYONKURU-DARIUS](https://github.com/NIYONKURU-DARIUS)
- Email: [dariusniyonkuru351@gmail.com](mailto:dariusniyonkuru351@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.
