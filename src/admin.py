import os
from flask_admin import Admin
from models import db, User, Puzzle, Order
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
  def on_model_change(self, form, model, is_created=False):
        model.picture_of_puzzle = model.picture_of_puzzle
        model.picture_of_box = model.picture_of_box
        pass
        # column_list = ('name_of_puzzle', 'number_of_pieces', 'age_range', 'category','is_available')
    # form_excluded_columns = ('picture_of_puzzle', 'picture_of_box') # this is how you hide a field from the admin

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(UserView(Puzzle, db.session))
    admin.add_view(ModelView(Order, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session)) 