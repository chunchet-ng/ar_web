# AR web application

This is a web application for Buddhist NGOs to keep track of the allowable requisites. NON-COMMERCIAL use only.  

## Useful commands

Create a new conda environment based on the requirements file.

```sh
conda env create -f "file_name"
conda activate "env_name"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
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
