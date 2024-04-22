# library_manager

This is a simple library manager application developed using Django and Django REST Framework.

## Installation

1. make a folder named library
    ```bash
        sudo mkdir library
    ```

2. Create a virtual environment (optional but recommended):

```bash
python3.10 -m venv myenv
```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
     
   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```

2. Clone the repository:

```bash
    git clone https://github.com/ajay-8/library_manager.git
    cd library_manager/library_manager
    touch .env
```
Paste the below content in file

```bash
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
```
Replace db creds according to your need.


4. Install the required dependencies:

```bash
pip install -r requirements/requirements.txt
```

## Usage

1. Run the migrations to create the database schema:

```bash
python manage.py migrate
```

2. Create a superuser (admin) account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

3. Start the development server:

```bash
python manage.py runserver
```
## OR RUN 

```bash
    sudo docker-compose -f docker-compose.yml up --build -d
```

Open a web browser and navigate to http://127.0.0.1:8000/admin to access the Django admin interface.

Use the admin interface to create authors and books.

Open a web browser and navigate to http://127.0.0.1:8000/ to access the library.


## API Documentation
- https://documenter.getpostman.com/view/19937009/2sA3Bq2qJo

