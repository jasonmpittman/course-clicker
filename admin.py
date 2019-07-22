from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask import session, redirect, url_for, request
from models import Users
from datetime import datetime

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'
    
        self.column_formatters = dict(typefmt.BASE_FORMATTERS)
        self.column_formatters.update({
            type(None): typefmt.null_formatter,
            datetime: self.date_format,
        })

        self.column_type_formatters = self.column_formatters
    
    def date_format(self, view, value):
        return value.strftime('%B-%m-%Y %I:%M:%p')

    def is_accessible(self):
        if 'user' in session:
            user = Users.query.filter_by(username=session['user']).first()
            return user.role == 'faculty'
    
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('home', next=request.url))

