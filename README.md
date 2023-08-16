<!-- classification_image_enhancement_fuzzy_flask -->
# Getting Started
<img alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img alt="flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"> <img alt="html" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img alt="css" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img alt="tailwind" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"> <img alt="javascript" src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"> <img alt="jquery" src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white">  

Follow the steps below to get the Flask web application up and running on your local machine.

## Prerequisites
Make sure you have the following software installed:

Python (3.6 or higher)

pip (Python package manager)

## Installation
Clone this repository to your local machine:
```
git clone https://github.com/Marwahns/classification_image_enhancement_fuzzy_flask.git
```
Navigate to the project directory:
```
cd classification_image_enhancement_fuzzy_flask
```
Create a virtual environment (optional, but recommended):
```
python -m venv venv
.\venv\Scripts\activate # Pada Mac: source venv/bin/activate
```
Install the required Python packages using pip:
```
pip install -r requirements.txt
```
If the previous command does not work, run the following command to create the `requirements.txt` file
```
pip freeze > requirements.txt
```
## Running the Application
Start the Flask development server:
```
python app.py
```
Open your web browser and go to `http://localhost:5000` to see the Flask web application in action.

Once you have generated the requirements.txt file, you can deactivate the virtual environment using the command:
```
deactivate
```
## Project Structure
```
classification_image_enhancement_fuzzy_flask/
│
├── source/
│   ├── handle_image.py
│   ├── image_enhancement_mamdani.py
│   ├── image_enhancement_sugeno.py
│   ├── image_enhancement_tsukamoto.py
│   ├── image_enhancement.py
│   └── pneumonia_detection.py
│
├── static/
│   ├── css/
│   │   └── newStlye.css
│   ├── image/
│   │   └── icon-logo.png
│   └── js/
│       ├── newScript.js
│       └── vanilla-tilt.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── notFound.html
│
├── app.py
├── README.md
└── requirements.txt
```
