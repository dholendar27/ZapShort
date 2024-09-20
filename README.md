# ZapShort - URL Shortener

**ZapShort** is a fast, secure, and customizable URL shortener that converts long links into short, shareable URLs. With features like JWT-based user authentication, custom aliases, and click tracking, ZapShort makes link sharing simple and secure.

This README will guide you through setting up the virtual environment, installing dependencies, configuring JWT authentication, and running the Flask server.

## Features

- **Custom URL Aliases**: Create short URLs with custom endings.
- **Click Tracking**: Track the number of clicks for each shortened URL.
- **JWT Authentication**: Users must log in using JWT to shorten URLs.
- **Secure and Open Source**: The project is fully open-source and highly customizable.

## Prerequisites

- Python 3.x installed on your system
- Pip (Python package installer)
- `virtualenv` for creating isolated Python environments

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dholendar27/zapshort.git
cd zapshort
```

### 2. Create a Virtual Environment

In the project directory, create a virtual environment using `virtualenv`:

```bash
# Install virtualenv if you don't have it installed
pip install virtualenv

# Create virtual environment
virtualenv venv
```

### 3. Activate the Virtual Environment

For **Windows**:

```bash
venv\Scripts\activate
```

For **macOS/Linux**:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

The project dependencies, including `flask-jwt-extended`, are listed in the `Pipfile`. To install them, run:

```bash
pip install pipenv
pipenv install
```

This will install dependencies such as:
- `Flask`
- `Flask-JWT-Extended`
- `Flask-SQLAlchemy`

### 5. Set Up Environment Variables

To secure the JWT token, you need to set the secret key in config file. This key will be used to sign the JWT tokens.

```bash
JWT_SECRET_KEY="your_secret_key"
```

### 6. Set Up the Flask App

Ensure that `FLASK_APP` is set to `run.py` in your environment.

For **Windows**:

```bash
set FLASK_APP=run.py
```

For **macOS/Linux**:

```bash
export FLASK_APP=run.py
```

### 7. Run the Flask Server

To start the Flask development server, run the following command:

```bash
flask run --port=5009
```

Alternatively, you can directly run the `run.py` file:

```bash
python run.py
```

The server will now be running on `http://localhost:5009`.

---

## URL Shortener Functionality

### How It Works

1. **User Registration/Login**: Users must sign up or log in using JWT-based authentication.
2. **Token Generation**: After login, a JWT token is generated and provided to the user.
3. **Authenticated URL Shortening**: The user passes this token in the header to shorten URLs.
4. **Generate Short URL**: A unique short code is generated from the provided long URL.
5. **Custom Aliases**: Users can create custom aliases instead of a randomly generated short code.
6. **Access Short URL**: When someone enters the short URL (e.g., `http://localhost:5009/shortcode`), they are redirected to the original long URL.
7. **Click Tracking**: Every time a short URL is accessed, the click count is tracked.

---

## JWT Authentication

ZapShort uses **`extended_flask_jwt`** to implement JWT-based authentication. Users must log in and receive a JWT token before they can shorten URLs.

### Endpoints for Authentication:

- **Register**: `POST /register`
  - Users register with a username and password.
  - Example payload:
    ```json
    {
      "first_name": "firstname",
      "last_name": "lastname",
      "email": "abc@gmail.com",
      "password": "password123"
    }
    ```

- **Login**: `POST /login`
  - Users log in with their credentials to receive a JWT token.
  - Example payload:
    ```json
    {
      "email": "abc@gmail.com",
      "password": "password123"
    }
    ```

- **Protected Endpoint**: `POST /shorten`
  - Users must pass the JWT token in the request header as `Authorization: Bearer <token>` to shorten URLs.

### Example of JWT Token Authentication:

1. **User Login**:

   Request:

   ```bash
   POST /login
   ```

   Payload:

   ```json
   {
     "email": "abc@gmail.com",
     "password": "password123"
   }
   ```

   Response (JWT Token):

   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
     "refresh_token": "eyJhbGciON2mnd1NiIsInR5cCI6IkpXVCJ9..."
   }
   ```

2. **Authenticated URL Shortening**:

   After receiving the token, the user can shorten URLs by passing the token in the headers.

   Request:

   ```bash
   POST /shorten
   ```

   Headers:

   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

   Payload:

   ```json
   {
     "original_url": "https://www.example.com/some-long-url"
   }
   ```

---

## URL Shortener Workflow

1. **Login/Signup**: The user must register or log in to the application to access the URL shortening feature.
2. **Shorten URL**: The authenticated user sends a request with the long URL.
3. **Generate Short URL**: The server generates a unique short code or uses the provided custom alias.
4. **Redirect**: When the short URL is accessed, the app redirects to the original long URL.

### Example Workflow:

- **Step 1**: User logs in with JWT and receives a token.
- **Step 2**: Authenticated user enters a long URL (e.g., `https://www.example.com/some-long-url`) to shorten.
- **Step 3**: The app generates a short URL like `http://localhost:5009/xyz123`.
- **Step 4**: User shares the short URL.
- **Step 5**: When the short URL is visited, the user is redirected to the long URL.

---

## File Structure

```bash
zapshort/
│
├── venv/                     # Virtual environment directory (created after running virtualenv)
├── app/                      # Main application folder
│   ├── __init__.py           # Initializes the Flask app and integrates extensions (Flask-JWT, SQLAlchemy)
│   ├── models.py             # Database models for User, URL, etc.
│   ├── routes.py             # Flask routes (URL shortening logic & JWT authentication)
│   ├── config.py             # Application configurations (e.g., JWT settings, database)
│   └── extensions.py         # Extensions like JWT, SQLAlchemy are instantiated here
│
├── run.py                    # Main entry point to run the Flask app
├── Pipfile                   # Project dependencies for pipenv (includes Flask, Flask-JWT-Extended, etc.)
├── __init__.py               # Initializes the package (ensures `zapshort/` is treated as a Python package)
└── README.md                 # Documentation (this file)

```
