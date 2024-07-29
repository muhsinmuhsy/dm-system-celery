# DM-system


## Installation

1. Create a virtual environment and activate it (optional but recommended):

    ```bash
    python -m venv venv
    ```
    #### On Windows use
   `venv\Scripts\activate`
    
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Add .env:

    `SECRET_KEY=`
    `DEBUG=`
    `ALLOWED_HOSTS=`


4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (admin) account:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```



#   d m - s y s t e m - c e l e r y  
 