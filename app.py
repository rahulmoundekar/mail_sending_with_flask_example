import mimetypes
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'asrtarstaursdlarsn'
app.config.from_object('settings.Config')
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "PDF"]
mail = Mail(app)


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def compose_attachments():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        message = request.form['message']
        image = request.files["file"]

        if image.filename == "":
            flash('Please Upload Image file', "danger")
            return redirect(request.url)
        if allowed_image(image.filename):
            try:
                msg = Message(subject=subject, sender=app.config.get("MAIL_USERNAME"), body=message, recipients=[to])

                filename = secure_filename(image.filename)
                ctype = mimetypes.MimeTypes().guess_type(filename)[0]
                if ctype is None:
                    ctype = 'application/octet-stream'
                f_data = image.read()

                msg.attach(filename, ctype, f_data)
                mail.send(msg)
                flash('Mail Sent Successfully!..check out you inbox', "success")
            except Exception as e:
                print(e)
                flash('Something went wrong please try again later', "danger")
                return redirect(request.url)
        else:
            flash('That file extension is not allowed', "danger")
            return redirect(request.url)
    return render_template('index.html')


@app.route('/simple', methods=['GET', 'POST'])
def compose_mail():
    if request.method == 'POST':
        to = request.form['to']
        subject = request.form['subject']
        message = request.form['message']
        try:
            msg = Message(subject=subject, sender=app.config.get("MAIL_USERNAME"), body=message, recipients=[to])
            mail.send(msg)
            flash('Mail Sent Successfully!..check out you inbox', "success")
        except Exception as e:
            flash('Something went wrong please try again later', "danger")
            return redirect(request.url)

    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# run always put in last statement or put after all @app.route
if __name__ == '__main__':
    app.run(host='localhost')
