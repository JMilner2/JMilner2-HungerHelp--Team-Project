"""
Author: Josh and Andrew
Description: This module defines a Flask blueprint for a blog feature. It includes routes and views for creating,
 displaying, and accessing recipes.
"""
import notifications
from blog.forms import RecipeForm, images, EditRecipeForm
from models import Post
from flask import Blueprint, render_template, url_for, send_from_directory
from app import db, app, requires_roles
from flask_login import login_required, current_user

blog_blueprint = Blueprint('blog', __name__, template_folder='templates')


# Send a file from within a directory using send_file.
@app.route("/images/images/<filename>")
def get_file(filename):
    return send_from_directory("images/images", filename)


# blog function for handling blog form inputs
@blog_blueprint.route('/blog', methods=['GET', 'POST'])
@login_required
@requires_roles('user', 'admin')
def blog():
    form = RecipeForm()
    if form.validate_on_submit():

        # receives image and saves to app default file path
        image_name = images.save(form.image.data)
        # gets url for image to save in the database
        image_url = url_for("get_file", filename=image_name)

        new_post = Post(user_id=current_user.id,
                        title=form.title.data,
                        recipe=form.recipe.data,
                        ingredients=form.ingredients.data,
                        image=image_url,
                        price=form.price.data)

        # add the new recipe to the database
        db.session.add(new_post)
        db.session.commit()

        # sends email notification of new blog post to all users signed up
        notifications.send_emails()

        return render_template('/blog/blog.html', form=form, file_url=image_url)

    return render_template('/blog/blog.html', form=form)


# gets all recipe posts from database and passes them to blog_home to display
@blog_blueprint.route('/blog_home', methods=['GET','POST'])
def blog_home():
    recipes = Post.query.all()
    order_by = "recent"
    if recipes:
        return render_template('blog/blog_home.html', recipes=recipes, order_by=order_by)

    return render_template('blog/blog_home.html')


# sorts recipe Posts by either amount of views or most recent and renders a new blog_home
@blog_blueprint.route('/order_recipes/<order>', methods=['GET','POST'])
def order_recipes(order):
    if order == "views":
        recipes = Post.query.order_by(Post.views.desc()).all()
        return render_template('blog/blog_home.html', recipes=recipes, order_by=order)
    if order == "recent":
        recipes = Post.query.order_by(Post.post_id.desc()).all()
        return render_template('blog/blog_home.html', recipes=recipes, order_by=order)


# gets the clicked on recipe from the database to display it fully in recipe.html
@blog_blueprint.route('/recipe/<recipe_id>', methods=['GET','POST'])
def recipe(recipe_id):
    recipe = Post.query.filter_by(post_id=recipe_id).first()
    if recipe:
        # increments views as it's been clicked on
        views = recipe.views
        views += 1
        recipe.views = views
        db.session.commit()
        return render_template('blog/recipe.html', recipe=recipe)

    return render_template('blog/recipe.html')


# deletes the recipe when delete is clicked, can only be done by admins or by the posts author
@login_required
@requires_roles('user', 'admin')
@blog_blueprint.route('/delete_recipe/<recipe_id>', methods=['GET','POST'])
def delete_recipe(recipe_id):
    recipe = Post.query.filter_by(post_id=recipe_id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        recipes = Post.query.all()

        return render_template('blog/blog_home.html', recipes=recipes)

    return render_template('blog/recipe.html')


# Allows authors or admins to edit their posts.
@login_required
@requires_roles('user', 'admin')
@blog_blueprint.route('/edit_recipe/<recipe_id>',  methods=['GET','POST'])
def edit_recipe(recipe_id):
    form = EditRecipeForm()
    # gets recipe to edit
    recipe = Post.query.filter_by(post_id=recipe_id).first()

    # if statements allow users to edit as much or as little as they want
    if form.validate_on_submit():
        if form.image.data:
            image_name = images.save(form.image.data)
            image_url = url_for("get_file", filename=image_name)
            recipe.image = image_url

        if form.title.data:
            recipe.title = form.title.data

        if form.recipe.data:
            recipe.recipe = form.recipe.data

        if form.ingredients.data:
            recipe.ingredients = form.ingredients.data

        if form.price.data:
            recipe.price = form.price.data

        db.session.commit()

        return render_template('blog/recipe.html', recipe=recipe)

    if recipe:
        return render_template('blog/edit_recipe.html', recipe=recipe, form=form)

    return render_template('blog/blog_home.html')
