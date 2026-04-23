# 🚀 Enterprise Quiz Platform (Full-Stack)
https://online-quiz-platform-70ionct03-keerthilingams-projects.vercel.app/

A professional, decoupled Full-Stack application designed with a robust **Python (Flask)** backend and a high-end **Glassmorphism UI** frontend. This project demonstrates industrial-grade architecture, featuring Role-Based Access Control (RBAC), JWT authentication, and secure MongoDB integration.

---

## 🌟 Core Features

### 👤 Student Features
- **Secure Authentication:** Register and Login with password hashing.
- **Dynamic Quiz Consumption:** Real-time fetching of questions from the database.
- **Anti-Cheat Logic:** Intelligent random shuffling of question orders for every unique attempt.
- **Digital Report Card:** Instant access to historical performance and grading stored in the cloud.

### 🛠 Admin (Teacher) Features
- **VIP Access:** Protected dashboard accessible only via a secret "Organization Code."
- **Question Management:** Full CRUD (Create, Read, Delete) capabilities for quiz content.
- **User Analytics:** Monitor all registered participants and their access roles.
- **Category Control:** Organize questions by subjects (Python, SQL, etc.).

---

## 🛠 The Tech Stack

### Backend (The Brain)
- **Python & Flask:** Powering the RESTful API "Waiters."
- **PyJWT:** Implementing JSON Web Tokens for industry-standard state-less security.
- **Werkzeug:** Utilizing military-grade password hashing (pbkdf2:sha256).
- **PyMongo:** Driving the connection to the NoSQL storage layer.

### Database (The Vault)
- **MongoDB:** Using a flexible Document-based schema to store Users, Questions, and Scores.

### Frontend (The Interface)
- **HTML5 & Vanilla CSS:** Custom-engineered Glassmorphism design with responsive gradients.
- **JavaScript (Async/Fetch):** Decoupled logic that communicates with the Backend via JSON data packets.

---

## 📂 File Architecture: "What is What?"

### Root Files
- `app.py`: The Main Entry Point. It initializes the server and registers all API routes.
- `database.py`: The Database Connector. Centralizes the connection to MongoDB to prevent circular imports.
- `.env`: The Secret Box. Stores your sensitive MongoDB URI and JWT Secret Key.
- `requirements.txt`: The Dependency List. Tells the cloud exactly which tools to install.

### 🛣 Routes (The API Waiters)
- `routes/auth_routes.py`: Handles the "Bouncer" logic—Registration, Login, and JWT generation.
- `routes/quiz_routes.py`: Handle the "Kitchen" logic—fetching questions, grading tests, and managing the question database.

### 🎨 Frontend (The Customer Room)
- `frontend/index.html`: The Auth Portal. Automatically detects your role (User vs Admin) and routes you.
- `frontend/student.html`: The Student Dashboard. Handles the quiz taking and report card logic.
- `frontend/admin.html`: The Admin Command Center. Where data is injected into the system.
- `frontend/style.css`: The Design System. Contains the global styling and animations.

---

## 🧠 Architectural Concept: The "Restaurant" Analogy

This project uses a **Decoupled API Architecture**:
1. **The Customer (Frontend):** Sits in the dining room and never sees the kitchen. They just look at the menu (HTML).
2. **The Waiter (API/Python):** Takes the customer's request (Login/Start Quiz) in a JSON box and carries it to the back.
3. **The Kitchen (Backend):** Processes the data, checks the "VIP Token" (JWT), and retrieves the food (Data) from the Pantry.
4. **The Pantry (MongoDB):** Where the raw data is safely stored.

---

## 🛡 Security & Anti-Cheat

### JWT Authentication
Instead of old-school "sessions," this app uses **JSON Web Tokens**. Once you log in, you are given a cryptographically signed "VIP Wristband." Every time you ask for a quiz or try to add a question, the Python "Bouncer" checks your wristband for the correct stamp.

### Intelligent Shuffling
To prevent students from memorizing "Question 1 is B," the frontend uses a **Shuffle Algorithm**. It grabs the 16 questions for a subject and shuffles their order randomly in the browser's memory, ensuring every exam feels unique.

---

## 🚀 How to Run Locally

1. **Clone the repo:** `git clone <your-repo-link>`
2. **Setup Venv:** `python -m venv venv`
3. **Activate & Install:** `.\venv\Scripts\activate` and `pip install -r requirements.txt`
4. **Configure Secrets:** Create a `.env` file with your `MONGO_URI`.
5. **Launch:** `python app.py`
