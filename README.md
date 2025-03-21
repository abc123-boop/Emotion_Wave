# Full-Stack Web Application (HTML, CSS, JavaScript + Flask) 🚀

This is a full-stack web application using **HTML, CSS, and JavaScript for the frontend** and **Flask for the backend**.

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask, Flask-CORS
- **Deployment:** Render (for both frontend & backend)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/flask-html-app.git
cd flask-html-app
```

### 2️⃣ Install Dependencies

#### 📌 Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
```

No dependencies are needed for the frontend since it's plain HTML, CSS, and JavaScript.

---

## 🎯 Running the Project Locally

### 🔹 Start Flask Backend

```bash
cd backend
python app.py
```

Backend runs on `http://127.0.0.1:5000/`

### 🔹 Start Frontend

Since the frontend consists of static files (`index.html`, `styles.css`, `script.js`), you can open `index.html` directly in a browser **OR** serve it using Flask.

If serving via Flask:

1. Ensure your Flask app is configured to serve static files.
2. Access the frontend at `http://127.0.0.1:5000/`.

---

## 🌍 Deployment on Render

### 🔹 Deploy Backend

1. Push your code to GitHub
2. Create a **New Web Service** on [Render](https://render.com/)
3. Connect repo & set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Environment Variables:** `PORT=5000`

### 🔹 Deploy Frontend

1. Create a **New Static Site** on Render
2. Connect repo & set:
   - **Publish Directory:** Set it to the folder containing `index.html`

---

## 🛠 API Endpoints (Example)

| Method | Endpoint    | Description          |
| ------ | ----------- | -------------------- |
| GET    | `/api/data` | Fetch sample data    |
| POST   | `/api/send` | Send data to backend |
