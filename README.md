# CSC2033_Team06_22-23


## Name  

The name of our project is Hunger Help. Hunger help was inspired by our recognition of the issues surrounding global hunger but also in spirit of our current climate due to the cost-of-living crisis. 

 

## Description 

With hunger help, we are highlighting - to a variety of individuals - that not only is there help out there, but also, there is a way to maintain a healthy appetite even when on a budget. We are also striving to get our message out to the general public to join the fight against global hunger and henceforth creating a community of support and love available to all who require it.  

 

## Features 

#### Register and Login 

As a user, you will be required to register your details. This includes your name, email, password and phone number. There are validators and hashing as a part of this so passwords are stored safely and so when entering details, all information is in the correct format. There is also a click-box to allow users to sign on for email notifications. After doing so, an account is created to allow full use of the site and then storing these details so all they must do for future use is login with a username and password. As part of the login, reCAPTCHA is used as an extra layer of security.  

 

#### Food Bank Locator 

Once situated with an account, the user will be able to find information and location services dedicated to food banks surrounding the area. The information and facts and figures are presented on the about us page. The location of food banks is displayed with a link to google maps and you can enter a location to point out the nearby food banks.  

 

#### Blog/Recipe Section 

Another function of our site that can then be accessed is the recipes blog page. Within this page, you can view all recipes posted on our website. If you are logged in you can then post, edit, and delete your own recipes.  

 

#### Email Notification 

As stated above, users can opt in to get notifications to their email account every time a new recipe is uploaded with a link to the blog page so they can view it. This was created using SendGrid which is an MTA.  

 

## Installation 

Users are expected to install all the python modules listed in the requirements.txt file for the code to run as intended. 

#### Requirements.txt 
 
``````
Flask
WTForms 
Flask-WTF 
email_validator 
python-dotenv 
flask_sqlalchemy 
bcrypt 
mysql-connector-python 
mysqlclient 
flask_login 
Flask-Reuploaded 
flask_uploads 
flask_testing 
sendgrid 
``````

## Usage 


To run the code, run “app.py” and click the website link that appears in the console 

#### Database Initialization 

To initialise the database run the following code in the python console one by one:  

`From app import db `

`From models import init_db `

`init_db()  `

It should present SQL commands after that if successful. 

 

#### Testing: 
To run our test file, simply run the module “test.py” 

 

If you want to access our admin features, go to the login page and login with the following details: 

`Email: admin@email.com `

`Password: Admin1!`  

## Support 

For support, please email hungerhelphelp@gmail.com and someone will reach out.  
 

## Authors and acknowledgment 
#### Link to git repo: https://github.com/newcastleuniversity-computing/CSC2033_Team06_22-23.git

#### GitHub Profiles: 

Andrew Mason: https://github.com/AndrewJM7 

Josh Milner:  https://github.com/JMilner2 

Shaikha Almajed: https://github.com/shaikhaalmajed 

Vilius Rasevicius:  https://github.com/Viliuxxeris 

 

 

Project Status:
The project is complete. 

 