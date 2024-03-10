# NeoAuth-project
NeoAuth project is an backend part of the web application for authorization and registration using Django Rest Framework.

### Technologies
---
- Python
- Django Rest Framework
- Swagger UI
- Nginx
- Docker

### Install
---
#### Without docker
1. Clone repository to your local machine:
```
git clone ssh/https-key
```
2. Create virtual environment and activate virtual environment:
- On `Windows`:
```
python -m env venv
```
```
venv\Scripts\activate.bat
```
- On `Linux/MacOs`
```
python3 -m env venv
```
```
source venv/bin/activate
```
3. Add `.env` file to the root and fill with your data next variables:
```
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
```
4. Install all dependecies:
```
pip install -r requirements.txt
```
5. Run the project on your local host:
```
python/python3 manage.py runserver
```
### Authors
---
[Mamatair uulu Zakirbek, 2024](https://github.com/zakirdaniarov)
