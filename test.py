"""
Author: Josh Milner + Vilius Rasevicius + Shaikha Almajed
Description: This code is a testing file to test all the key functions of our code base
"""
import unittest
from flask_testing import TestCase
from flask_login import current_user, login_user
from app import app, db
from models import User
from users.forms import RegisterForm, LoginForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from blog.forms import EditRecipeForm
from models import Post
from blog.forms import RecipeForm


class FlaskTest(TestCase):
    def create_app(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # Set up the test environment
        db.create_all()

    def tearDown(self):
        # Tear down the test environment
        db.session.remove()
        db.drop_all()

    def test_register(self):
        # Create a form for registration
        form = RegisterForm()
        form.email.data = 'test@example.com'
        form.firstname.data = 'John'
        form.lastname.data = 'Doe'
        form.phone.data = '1234-567-8901'
        form.password.data = 'Password1!'
        form.confirm_password.data = 'Password1!'
        form.notifications.data = True

        # Perform a POST request to register a new user
        response = self.client.post('/register', data=form.data, follow_redirects=True)
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(email=form.email.data).first()
        # Assert that the user exists in the database
        self.assertIsNotNone(user)
        # Assert that the user attributes match the form data
        self.assertEqual(user.email, form.email.data)
        self.assertEqual(user.firstname, form.firstname.data)
        self.assertEqual(user.lastname, form.lastname.data)
        self.assertEqual(user.phone, form.phone.data)
        self.assertTrue(user.password)  # Password should be hashed and stored
        self.assertEqual(user.notifications, form.notifications.data)
        self.assertEqual(user.role, 'user')

    def test_login(self):
        # Create a form for login
        form = LoginForm()
        form.email.data = 'test@example.com'
        form.password.data = 'Password1!'

        # Create a test user and add it to the database
        user = User(email='test@example.com', firstname='John', lastname='Doe',
                    phone='1234-567-8901', password='Password1!', notifications=True, role='user')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data=form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Assert that the current user is authenticated
        self.assertTrue(current_user.is_authenticated)
        # Assert that the current user attributes match the test user
        self.assertEqual(current_user.email, user.email)
        self.assertEqual(current_user.firstname, user.firstname)
        self.assertEqual(current_user.lastname, user.lastname)
        self.assertEqual(current_user.phone, user.phone)
        self.assertEqual(current_user.role, user.role)

    def test_register_invalid_email_format(self):
        # Perform a POST request to register with an invalid email format
        response = self.client.post('/register', data=dict(
            email='invalid_email',
            firstname='John',
            lastname='Doe',
            phone='1234-567-8901',
            password='Password1!',
            confirm_password='Password1!',
            notifications=False
        ), follow_redirects=True)
        # Assert that the response contains the expected error message
        self.assertIn(b'Invalid email address.', response.data)

    def test_register_existing_email(self):
        # Create an existing user with the specified email
        existing_user = User(email='test@example.com',
                             firstname='John',
                             lastname='Doe',
                             phone='1234-567-8910',
                             password='Password1!',
                             notifications=False,
                             role='user')

        db.session.add(existing_user)
        db.session.commit()

        response = self.client.post('/register', data=dict(
            email='test@example.com',
            firstname='Jane',
            lastname='Smith',
            phone='1234-567-8901',
            password='P@ssw0rd',
            confirm_password='P@ssw0rd',
            notifications=False
        ), follow_redirects=True)
        self.assertIn(b'Email address already exists', response.data)

    def test_register_invalid_password(self):
        # Perform a POST request to register with an invalid password format
        response = self.client.post('/register', data=dict(
            email='test@example.com',
            firstname='John',
            lastname='Doe',
            phone='1234-567-8901',
            password='invalid_password',
            confirm_password='invalid_password',
            notifications=False
        ), follow_redirects=True)
        self.assertIn(b'Must contain at least 1 digit, 1 lowercase word character,'
                      b' 1 uppercase word character and 1 special character', response.data)

    def test_login_incorrect_email(self):
        # Simulate 4 failed login attempts by setting 'attempts' in the session
        with self.client.session_transaction() as sess:
            sess['attempts'] = 4  # Simulate 4 failed login attempts

        response = self.client.post('/login', data=dict(
            email='nonexistent_email@example.com',
            password='Password1!',
            recaptcha='recaptcha'
        ), follow_redirects=True)

        self.assertIn(b'Number of incorrect login attempts exceeded. please click <a href="/reset">here</a> to reset.',
                      response.data)

    def test_login_incorrect_password(self):
        # Create an existing user
        existing_user = User(email='test@example.com',
                             firstname='John',
                             lastname='Doe',
                             phone='1234-567-8910',
                             password='Password1!',
                             notifications=False,
                             role='user')

        db.session.add(existing_user)
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['attempts'] = 4  # Simulate 4 failed login attempts

        # Perform a POST request to login with an incorrect password
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='incorrect_password',
            recaptcha='recaptcha'
        ), follow_redirects=True)

        self.assertIn(b'Number of incorrect login attempts exceeded. please click <a href="/reset">here</a> to reset.',
                      response.data)

    def test_logout(self):

        # Create a test user
        user = User(email='test@example.com', firstname='John', lastname='Doe',
                    phone='1234-567-8901', password='Password1!', notifications=True, role='user')
        db.session.add(user)
        db.session.commit()
        login_user(user)
        self.assertTrue(current_user.is_authenticated)

        # Perform a GET request to logout endpoint
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_anonymous)

    def test_blog_add_post(self):

        # Create a test user
        user = User(email='test@example.com', firstname='John', lastname='Doe',
                    phone='1234-567-8901', password='Password1!', notifications=True, role='user')
        db.session.add(user)
        db.session.commit()
        login_user(user)
        self.assertTrue(current_user.is_authenticated)

        # Create a test post
        post = Post(
            title='Test Post',
            recipe='Add one table spoon of salt...',
            ingredients='Ingredient 1, Ingredient 2, Ingredient 3',
            price='9.99',
            image='images/images/lily-banse--YHSwy6uqvk-unsplash.jpg',
            user_id=user.id  # Assign the user ID to the post's user_id field
        )
        db.session.add(post)
        db.session.commit()

        # Populate the form data
        form = RecipeForm()
        form.title.data = 'Test Post'
        form.recipe.data = 'Add one table spoon of salt...'
        form.ingredients.data = 'Ingredient 1, Ingredient 2, Ingredient 3'
        form.price.data = '9.99'

        # Perform a POST request to add a new blog post
        response = self.client.post('/blog', data=form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        post = Post.query.filter_by(title='Test Post').first()
        # Assert that the post exists in the database
        self.assertIsNotNone(post)
        # Assert that the post attributes match the form data
        self.assertEqual(post.title, form.title.data)
        self.assertEqual(post.recipe, form.recipe.data)
        self.assertEqual(post.ingredients, form.ingredients.data)
        self.assertEqual(post.price, form.price.data)

    def test_blog_email_notif(self):
        # Create a user with email notifications enabled
        user = User(email='joshuaftmilner@gmail.com', firstname='John', lastname='Doe',
                    phone='1234-567-8901', password='Password1!', notifications=True, role='user')
        db.session.add(user)
        db.session.commit()

        email_list = User.query.filter_by(notifications=True).all()
        # Iterate over the email list and send an email notification to each user
        for emails in email_list:
            message = Mail(
                from_email='hungerhelphelp@gmail.com',
                to_emails=emails.email,
                subject='Hello From HungerHelp!',
                html_content='<html><body>'
                             '<h1>A new recipe has been posted on our blog!</h1>'
                             '<p>Click the link below to check it out:</p>'
                             '<p><a href="http://127.0.0.1:5000/blog_home">View Blog</a></p>'
                             '<p>Thank you for reading!</p>'
                             '</body></html>')
            # Send the email using SendGrid API
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            self.assertEqual(response.status_code, 202)

    def test_price_valid_input(self):
        # Create a form and set a valid price value
        form = EditRecipeForm()
        form.price.data = "1.99"

        # Assert that the form validates the input as valid
        self.assertTrue(form.validate())

    def test_price_invalid_input(self):
        # Create a form and set an invalid price value
        form = EditRecipeForm()
        form.price.data = "1.999"

        # Assert that the form validates the input as invalid
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
