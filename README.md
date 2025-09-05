<<<<<<< HEAD
# Biometric Authentication System (Facial Recognition)

This project provides a secure and user-friendly authentication system using facial recognition. It replaces or supplements traditional password-based logins with biometric verification, making it harder for unauthorized users to gain access while providing a seamless experience for legitimate users.

The repository contains two primary implementations:
1.  A **Desktop Application** built with Python and a `customtkinter` GUI.
2.  A **Web Application** with a React frontend and a Python (FastAPI) backend.

---

## 🌟 Features

- **Secure Facial Registration:** Easily enroll users by capturing their facial data.
- **Real-Time Authentication:** Log in instantly by simply looking at the camera.
- **Encrypted Data Storage:** All biometric data (face descriptors) is encrypted before being saved, ensuring confidentiality and protecting against data breaches.
- **Dual Implementations:** Includes both a standalone desktop app and a full-stack web version.
- **Modular Architecture:** The code is organized into distinct modules for the GUI, facial analysis, data storage, and encryption, making it easy to maintain and extend.

---

## 🛠️ Architecture & Technology Stack

### Desktop Application
- **Language:** Python
- **GUI:** `customtkinter`
- **Facial Recognition:** `dlib`, `OpenCV`, `face_recognition`, `deepface`
- **Data Encryption:** `cryptography`

### Web Application
- **Backend:**
  - **Framework:** `FastAPI`
  - **Language:** Python
  - **Facial Recognition:** `dlib`, `OpenCV`, `face_recognition`, `deepface`
  - **Authentication:** `python-jose` (for JWT)
- **Frontend:**
  - **Framework:** `React.js`
  - **HTTP Client:** `Axios`
  - **Routing:** `react-router-dom`

---

## ⚙️ Setup and Installation

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/en/download/) (for the web application)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### 2. Download the Dlib Shape Predictor Model

This project requires the `shape_predictor_68_face_landmarks.dat` model file for facial landmark detection. Due to its size, it has not been included in this repository.

- **Download it from here:** [shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
- **Extract it:** Unzip the downloaded file to get `shape_predictor_68_face_landmarks.dat`.
- **Place it:**
    - For the **Desktop App**, place the file in the root directory of the project.
    - For the **Web App**, place the file inside the `web/backend/` directory.

---

### 🖥️ Running the Desktop Application

1.  **Navigate to the project root directory.**

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    *Note: This project requires specific versions of TensorFlow and NumPy.*
    ```bash
    pip install -r requirement.txt
    pip install tensorflow==2.17.0 numpy==1.23.5
    ```
    *If you encounter issues, you may need to install `dlib` manually. Please refer to the official `dlib` installation guide for your OS.*

4.  **Run the application:**
    ```bash
    python main.py
    ```

---

### 🌐 Running the Web Application

The web application consists of a backend and a frontend that must be run separately.

#### A. Backend Setup (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd "web/backend"
    ```

2.  **Create and activate a new Python virtual environment:**
    ```bash
    # For Windows
    python -m venv venv_web
    .\venv_web\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv_web
    source venv_web/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will be running at `http://127.0.0.1:8000`.

#### B. Frontend Setup (React)

1.  **Open a new terminal.**

2.  **Navigate to the frontend directory:**
    ```bash
    cd "web/frontend"
    ```

3.  **Install the required npm packages:**
    ```bash
    npm install
    ```

4.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The React application will be accessible at `http://localhost:5173` (or another port if 5173 is busy). Open this URL in your web browser.

5  ## 🤝 Contributors
   
   - **[Salah Yasin](https://github.com/salah47)** - Database,Backend and Hshing 
     
   - **[Steohen N.A Ellis](https://github.com/)** - GUI and FrontEnd
    
   - **[Aditya Rishav](https://github.com/adityarishav)** - Main face data login logic and backend

