from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


@app.route("/")
def my_home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    email, subject, message = data.values()
    message = message.replace("\n", "<br>")
    try:
        with open('database.txt', mode='a') as db:
            file = db.write(
                f'{email},{subject},{message}' + '\n')
    except FileNotFoundError as e:
        print('File not available')


def write_to_csv(data):
    email, subject, message = data.values()
    message = message.replace("\n", "<br>")
    try:
        with open('database.csv', mode='a') as db:
            csv_writer = csv.writer(
                db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email, subject, message])
    except FileNotFoundError as e:
        print('CSV File not available')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Error while saving to DB.'
    else:
        return 'Something went wrong dio musso!'
