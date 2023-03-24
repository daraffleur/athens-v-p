import os
import requests

from flask import render_template, request, Blueprint, flash, redirect

from app.forms import ApplicantForm
from app.models import Applicant
from app.logger import log


main_blueprint = Blueprint("main", __name__)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_applicant_to_telegram_chat(text):
    method = "sendMessage"
    token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ApplicantForm(request.form)
    if form.validate_on_submit():
        applicant = f"NEW APPLICATION \n\nFirst Name: {form.first_name.data}\nLast Name: {form.last_name.data}\n \nEmail: {form.email.data}\nPhone Number: {form.phone.data}"
        send_applicant_to_telegram_chat(applicant)
        applicant = Applicant(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        applicant.save()
        flash(
            "Your application has been sent successfully! We will call you soon!",
            "success",
        )
        log(
            log.DEBUG,
            "Your application has been sent successfully! We will call you soon!",
        )
        # return redirect("http://46.101.167.8/#registration")
        return redirect("http://127.0.0.1:5000/#registration")
    
    elif form.is_submitted():
        for error in form.errors:
            for msg in form.errors[error]:
                log(log.ERROR, "Save application(): %s", msg)
                flash(
                    "Something went wrong... Please reload the page and try submitting an application again. ",
                    "danger",
                )
                return redirect("http://127.0.0.1:5000/#registration")
                # return redirect("http://46.101.167.8/#registration")
    return render_template("index.html", form=form)
