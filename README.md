# AR web application

This is a web application for Buddhist NGOs to keep track of the allowable requisites. NON-COMMERCIAL use only.  

## Useful commands

Create a new conda environment based on the requirements file:
```sh
conda env create -f "file_name"
conda activate "env_name"
```
Then, initialise the database with the following commands:
```sh
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py collectstatic
```
Create a superuser with user profile and run the server:
```sh
python manage.py createsuperuser
python manage.py shell

from accounts.models import Profile
from django.contrib.auth.models import User
users_without_profile = User.objects.filter(profile__isnull=True)
for user in users_without_profile:
    Profile.objects.create(user=user)

python manage.py runserver                              
```

## 20/4/2020

**Changes**

- Initial commit

## 12/5/2020

**Changes**
- Allow filter by month/date range
- Generate receipt
- Export report (monthly/complete)
- Add in column header to transaction detail table
