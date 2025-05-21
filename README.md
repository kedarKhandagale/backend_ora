# Django Project
## Installation

1. **Clone the repository:**
    ```bash
    git clone <repository-link>
    cd app
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Ensure PostgreSQL is running and accessible.
    - Update database connection details in your .env file.

## Configuration
- Configuration variables are managed through a .env file at the root of the project. Here's a sample .env file:

    ```bash
    DATABASE_URL="postgresql://user:password@localhost/db_name"
    HOST="127.0.0.1"
    PORT=5432
    DEBUG=True
    ```

## Apply migrations
python manage.py makemigrations
python manage.py migrate


## Creating a New App
- To create new django app under app use below command
    ```bash
    python manage.py startapp <app_name>
    ```

## Running the Application
- Start the application
    ```bash
    python manage.py runserver
    ```



