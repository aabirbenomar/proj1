from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '123e'
app.config['RECAPTCHA_PUBLIC_KEY'] = '50006'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'y7090'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    recaptcha = RecaptchaField()

def validate_recaptcha(recaptcha_response):
    data = {
        'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("20 per day", "5 per hour")
def index():
    form = MyForm()
    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')
        result = validate_recaptcha(recaptcha_response)

        if result['success']:
            ip_address = request.remote_addr
            return f"Thank you, {form.name.data}, for passing the human verification!"
        else:
            return "Failed human verification. Please try again."

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

