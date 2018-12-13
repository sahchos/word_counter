from wtforms.fields.html5 import URLField
from wtforms.validators import url
from wtforms_tornado import Form


class WordCounterForm(Form):
    url = URLField(validators=[url()])
