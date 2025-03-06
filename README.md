<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Jx1126">
    <img src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/147470595?s=200&v=4&h=300&w=300&fit=cover&mask=circle&maxage=7d" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">eLearning Platform</h3>

  <p align="center">
    CM3035 - Advanced Web Development Final
    <br />
    <a href="https://github.com/Jx1126/awd-final"><strong>Repository Source »</strong></a>
    <br />
  </p>
</div>

## About The Project
CM3035 - Advanced Web Developmenmt Final - Create an eLearning platform designed to provide an interactive online learning experience. The GitHub repository for this project is currently private, but it can be made public upon request if required by the examiner.

### Built With

* ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
* ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
* ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
* ![Flowbite](https://img.shields.io/badge/Flowbite-0078D7?style=for-the-badge&logoColor=white)
* ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)

<br />

## Getting Started

### Installation Guide

To set up and run the application, follow these steps:

1. **Unzip the Project Folder**
    - Extract the eLearning project from the ZIP file to any location.

2. **Navigate to the Project Directory** 
   Open a terminal and change the directory into the project folder:
  ```powershell
    cd elearning
  ```
3. **Install Required Dependencies**
    -	Install required Python packages using requirement.txt:
  ```powershell
    pip install -r requirements.txt
  ```
4.	**Run the Development Server**
    -	Run the eLearning project:
  ```powershell
    python manage.py runserver
  ```
<br />

### Celery and Redis Setup

Celery is used to handle background tasks, while Redis serves as the message broker for Celery. To set up, please follow these steps:

1. **Start Redis Server via Ubuntu**
    -	To start Redis:
    ```powershell
      sudo service redis-server start
    ```
    -	To check if Redis is running:
    ```powershell
      sudo service redis-server status
    ```
    -	To stop Redis:
    ```powershell
      sudo service redis-server stop
    ```

2.	**Start Celery Worker**
    -	Starts Celery (Windows):
    ```powershell
      celery -A elearning worker --loglevel=info -P threads
    ```
    -	Starts Celery for other OS:
    ```powershell
      celery -A elearning worker --loglevel=info
    ```
<br />

### Installation and Setup Troubleshooting
If the application does not run correctly, please try the following solutions:
-	**CSS not rendering properly**
    - Try rebuilding Tailwind CSS
    ```powershell
      npm run css
    ```
- Styling still not working
    - Try installing the node modules
    ```powershell
      npm install
    ```
-	WebSocket connection failed immediately
    - Ensure Daphne is installed
    ```powershell
      pip install daphne
    ```
    - Rerun the server
    ```powershell
      python manage.py runserver
    ```



<!-- USAGE -->
## Usage

### Running Unit Tests
- To run the unit tests, run the following command:
```powershell
python manage.py test
```
- For more testing information, run the following:
```powershell
python manage.py test -v 2
```

<br />

### Django Admin Panel
**URL:** http://127.0.0.1:8000/admin/
<br>
**Username:** admin
<br>
**Password:** password

<br />

### Login Credentials
The following are the login credentials for the pre-seeded user accounts:
<br>
|     Username     |     Role       |     Password        |
|------------------|----------------|---------------------|
|     student_1    |     Student    |     studentone      |
|     student_2    |     Student    |     studenttwo      |
|     student_3    |     Student    |     studentthree    |
|     teacher_1    |     Teacher    |     teacherone      |
|     teacher_2    |     Teacher    |     teachertwo      |
|     teacher_3    |     Teacher    |     teacherthree    |

<br />

## License

Distributed under the GNU General Public License v3.0. See `LICENSE.txt` for more information.