# ✅ MiniSocialMediaAPI

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/) 
[![Django](https://img.shields.io/badge/Django-4.x-darkgreen?logo=django&logoColor=white)](https://www.djangoproject.com/) 
[![DRF](https://img.shields.io/badge/DRF-API-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue?logo=postgresql)](https://www.postgresql.org/)  

<p>
  <img src="https://skillicons.dev/icons?i=python,django,git,github,windows,vscode,postman,postgres">
</p>

## 📖 Description

**Taskmanagement** is a mini project built with **Django** and **Django REST Framework (DRF)**.

🔑 Key points:
- Backend built with **Django** + **DRF**  
- API documentation generated with **drf-spectacular**  
- **JWT authentication system** for secure access  

---

## ✨ Features
- 📋 Create a Project – Define the **project** and break it down into tasks.
- 👨‍💻 Assign Members – Add **members** to each **project** and assign tasks to them.
- 🏷️ Task Tagging – **Members** can tag themselves or others to claim or collaborate on tasks.
- ✅ Task Completion & Scoring – When a **task** is **completed**, award the **assigned score** to the **member who finished it**.
- 🎯 Task Levels – Each **task** has a difficulty **level**, which determines the **score value**.
- 🏆 Progress Tracking – Track total **scores** per member to **measure contributions and performance**.

---

## 🛠️ Requirements
- **Python 3.9+**  
- **PostgreSQL** (running locally or remote)  
- **Virtual environment** tool: `venv`

---

## ⚙️ Installation & Usage
```bash
1️⃣ Clone the repository
`git clone https://github.com/Amirhosein-Rezaie/TaskManagementAPI.git`
`cd TaskManagementAPI`

2️⃣ Create a virtual environment
`python -m venv .venv`
# Activate:
source `.venv/bin/activate`   # Linux/Mac
`.venv\Scripts\activate`     # Windows

3️⃣ Install dependencies
`pip install -r requirements.txt`

4️⃣ Apply migrations
`python manage.py makemigrations`
`python manage.py migrate`

5️⃣ Run the server
`python manage.py runserver`

6️⃣ use documents
after running the server open your browser and go to `http://127.0.0.1:8000/api/docs`
```
---
💡 *Hope you enjoy exploring this project as much as I enjoyed building it!*  
