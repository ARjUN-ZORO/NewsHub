from .db import mon_db
from wtforms import form, fields
from flask_admin.contrib.sqla import ModelView

class pages(form.Form):
    article_id = fields.StringField(50)
    title = fields.StringField(50)


class pagesView(ModelView):
    column_list = ('article_id','title')
    column_sortable_list = ('article_id','title')

    form = pages
