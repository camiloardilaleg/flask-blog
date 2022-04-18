from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    title_slug = StringField('Título slug', validators=[Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')

"""
Las clases que heredan de FlaskForm, permiten crear objetos que van a tener los atributos que nosotros necesitamos para rellenar formularios.
Estos atributos coinciden con los campos que nosotros hemos especificado en los formularios normales de HTML.

Para que se puedan usar estos objetos, debemos importar la clase FlaskForm en cada una de las vistas a traves de los decoradores @app.route.

Es importante notar que una vez importado el objeto de las clases que hemos creado en las vistas, ya no es necesario utilizar las etiquetas 
HTML para crear los formularios, sino los atributos de los objetos que hemos creado. 
"""