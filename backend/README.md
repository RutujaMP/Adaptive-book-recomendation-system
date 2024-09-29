# BookABook
# Python verison: 3.9

# To depoly backend server
1. make sure the db 'db_test.sqlite3' is under the folder 'backend'
2. make sure the 'mood_matrix.csv' is under the folder 'backend/data'
3. run following commands:
```
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The following link shows how to call the api in the backend: https://api.postman.com/collections/29923394-99c845a9-af6a-40b4-8ac4-c274f7af1ff3?access_key=PMAT-01HT2B7EB2S2WBJXTG675R3S9A 

