# 🎬 Movie Navigator

**Movie Navigator** is a web application built with **FastAPI** that allows users to explore movies by genre and release year, get intelligent (mock) recommendations, and manage personal movie lists.  
It integrates with the **TMDB API** to fetch real movie data and uses a **Mock AI** module for generating recommendations.
https://movie-navigator-4.onrender.com
---

## 🚀 Overview

The project demonstrates the use of modern web technologies to build an intelligent movie browsing platform:
- 🔍 Search movies by **genre** and **year**
- 💡 Get **AI-style recommendations** (via a mock recommendation engine)
- 📋 Create and manage **personal movie lists**
- 🎞️ Fetch real movie data (titles, ratings, posters) using the **TMDB API**

---

## 🧠 Key Features

| Feature | Description |
|----------|-------------|
| 🔎 Movie Search | Filter by genre and release year |
| 💡 Intelligent Recommendations | Suggests similar movies using a mock AI function |
| 🗂️ Personal Lists | Create, delete, and manage movie collections |
| 💾 Database Storage | SQLite with SQLAlchemy ORM integration |
| 🎨 User Interface | Clean Jinja2 templates with Tailwind CSS |

---

## 🧰 Technologies Used

- **FastAPI** — main web framework  
- **Jinja2** — templating engine  
- **SQLite + SQLAlchemy** — local database  
- **TMDB API** — external movie data provider  
- **Mock AI** — simulated recommendation logic  

---

## 📁 Project Structure

📦 movie-navigator/
│
├── app/
│ ├── controllers/
│ │ ├── movie_controller.py
│ │ └── list_controller.py
│ │
│ ├── services/
│ │ ├── movie_service.py
│ │ ├── list_service.py
│ │
│ ├── models/
│ │ ├── movie.py
│ │ ├── movie_list.py
│ │ └── movie_list_item.py
│ │
│ ├── database/
│ │ └── database.py
    └── init_db.py
│ │
│ └── main.py
│
├── views/
│ ├── index.html
│ ├── base.html
│ ├── movies.html
│ ├── about.html
│ ├── lists.html
│ ├── list_detail.html
│ └── recommendations.html
│
├── .env
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/movie-navigator.git
cd movie-navigator

Create a virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt
TMDB_API_KEY=your_tmdb_api_key_here

Get your API key from:
🔗 https://developer.themoviedb.org/

Run the Application
uvicorn app.main:app --reload

```

