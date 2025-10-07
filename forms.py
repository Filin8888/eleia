from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, MultipleFileField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Контент", validators=[DataRequired()])
    images = MultipleFileField("Зображення")  # <- додано для кількох файлів
    main_image_index = StringField("Головне зображення")  # можна передавати індекс головного з фронту
    submit = SubmitField("Зберегти")




class CommentForm(FlaskForm):
    content = TextAreaField('Коментар', validators=[DataRequired()])
    submit = SubmitField('Відправити')

