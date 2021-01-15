# Environment setup

I recommend to use Python's environment with:

```python -m venv```

Now source the environment:

```env\Scripts\activate```

Install all required modules:

```pip install -r requirements.txt```
# First time use
Migrate the database with:

```python manage.py migrate```

## Usage
```python manage.py runserver```

server: http://127.0.0.1:8000/

# Creating super user:
Run command:

```python manage.py createsuperuser```


# Super user credentials:
admin site: http://127.0.0.1:8000/admin/

login: admin

password: admin

email: admin@admin.com

# Generating code coverage

Setup:

```coverage run --source='.' manage.py test server```

Generate report:

```coverage report```

Generate html report:

```coverage html```

To generate reports excluding unit tests code use:

```coverage report --omit=.\server\tests\*```

```coverage html --omit=.\server\tests\*```

# Integration with Selenium testing

https://docs.djangoproject.com/pl/3.1/topics/testing/tools/#django.test.LiveServerTestCase
