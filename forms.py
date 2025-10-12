from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, MultipleFileField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Контент", validators=[DataRequired()])


    main_image = StringField("Головне зображення")  # можна передавати індекс головного з фронту

    gallery_images = MultipleFileField('Додаткові фото')  # ← ось це нове

    submit = SubmitField("Зберегти")




class CommentForm(FlaskForm):
    content = TextAreaField('Коментар', validators=[DataRequired()])
    submit = SubmitField('Відправити')

