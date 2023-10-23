# sports24h

Project made for the course "Development for Internet and Mobile Apps".

Technologies used:
- Python
- HTML
- CSS
- JavaScript
- Django
- React

Sports website for buying and selling sports products.
There are 3 types of users: client, seller and admin. 
Sellers can make posts (announcing sales, e.g.) and publish new products for sale.
Cliens can like and comment posts and can add products to the shopping cart.
Users can follow each other and subcribe to forums (and only filter for items belonging to that forum).

### Necessary dependencies

Besides Python 3, Django and the editor PyCharm, you will also need to install:
- the Node.js library which handles javascript events concurrently
- the npm tool, which allows installing and managing different versions of javascript libraries 

Other tools like Bootstrap, Reactstrap and Axios will be installed during the frontend development.

````
pip install django

pip install djangorestframework django-cors-headers

python -m pip install Pillow
````

### Steps to execute the project

Open a terminal inside the 'sitediam' folder:
````
python manage.py runserver
````

Navigate to the url http://localhost:8000/sports24h

### Steps to execute the react frontend

Open a new terminal inside the 'sitediam/sports24h-frontend':

````
npm start
````
Navigate to the url http://localhost:3000/