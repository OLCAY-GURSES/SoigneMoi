SoigneMoi

SoigneMoi's web application has been designed to provide an intuitive, user-friendly interface for end-users. The web application provides seamless access to hospital functions and data.

The web application features fluid navigation and essential functionalities for an optimal user experience, such as :

Patient stay management
Creation of user accounts
Viewing stay history
And other key functionalities
The aim is to provide end-users with simplified, intuitive access to hospital information and services.

The following project is part of the "SoigneMoi" school project, made for the Studi's "ECF" of the summer 2024 exam session.


Presentation:
This website is designed to interact with mobile and desktop applications:

SoigneMoi Mobile App https://github.com/OLCAY-GURSES/sgm_phone_app
SoigneMoi Desktop App https://github.com/OLCAY-GURSES/sgm_desktop

How to install :
Prerequisites :
Python v10. or higher installed on local machine. https://www.python.org/downloads/
Have Git installed on local machine. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

1. Clone the project:
Copy the Github link in the top right-hand corner of the repository's "code" page.
In a terminal, go to the local location where you want the source folder to be cloned.
Execute the git clone command:

 git clone hhttps://github.com/OLCAY-GURSES/SoigneMoi.git
 
In principle, a folder named SoigneMOi is created. Move there:
 cd SoigneMOi

2. Create a virtual environment (here named env ) using the command :
 python3 -m venv env

3. Activate the virtual environment with the command :
for Unix/Linux platforms :
 source env/bin/activate
for Windows platforms (cmd.exe):
 source env/scripts/activate
other: see https://docs.python.org/3/library/venv.html
Your command prompt should now be preceded by (env), indicating that you are in the virtual environment.

4. Install project dependencies :
 pip install -r requirements.txt

5. Play migrations to create tables in the DB:
 python manage.py makemigrations 
 python manage.py migrate

6. Run the application :
 python manage.py runserver 

 The opening page can be found at the local address :

 http://127.0.0.1:8000/ 

 If, for example, you wish to start the server on another port 4512 : 

 python manage.py runserver 4512

Usage:

Create a Django superuser with the command :

 python manage.py createsuperuser

You can also create everything from the empty data DB:
Create a Django superuser with the above command

Then, with this superuser, you can access the Django admin area here http://127.0.0.1:8000/admin

This allows us to create a user with an administrator account for SoigneMoi. 


By logging in with this administrator account in the interface, you can access the Administrator Area to create doctor(s) (schedule management), secretary(s),...

Please refer to the Guide available in the documentation, for details of these steps to using SoigneMoi, including as a Visitor/User.











