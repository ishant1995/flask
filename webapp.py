from __future__ import unicode_literals
import traceback
import os
from urllib.parse import urlparse
import time
import logging
from flask import Flask, request, render_template
from werkzeug import secure_filename

path = os.getcwd()
app = Flask(__name__, template_folder='templates')
logger = logging.getLogger(__name__)

#logging.basicConfig(
#    filename='logs/webapp_log_' + str(time.strftime("%d-%b-%Y")) + '.log',
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    level=logging.INFO
#)

UPLOAD_FOLDER = 'E:\\doc\\'


@app.route('/demo_site')
def home_page_form():
    os.chdir(path)
    return render_template('priority_home.html')


@app.route('/demo_site', methods=['POST'])
def thankyou_page():
    f_AR_list = []
    f_AR_names = []

    #print(request.files.getlist('Docfile_AR'))

    logger.info("Accessing the account name form POST request")
    try:
        account_name = request.form['AccountName']
    except Exception as e:
        logger.error("Account Name not found in POST request")
        return render_template('error.html', error_message="Account Name not found")

    logger.info("Accessing the email address form POST request")
    try:
        email_list = request.form['Email'].split(',')
    except Exception as e:
        logger.error("Email address not found in POST request")
        return render_template('error.html', error_message="Email Address not found")

    logger.info("Accessing the AR files from POST request")
    try:
        f_AR_list = request.files.getlist('Docfile_AR')
        f_AR_names = [secure_filename(f.filename) for f in f_AR_list]
    except Exception as e:
        print(e)
        logger.warning("AR File not found")

    try:
        print("DEF")
        logger.info("Saving the AR uploaded files")
        if not os.path.exists(str(UPLOAD_FOLDER)):
            os.makedirs(str(UPLOAD_FOLDER))
        save_files(f_AR_list, "AR")

        return render_template('thankyou-page.html', unique_id="016ffkane0023793ghas")
    except Exception as e:
        logger.error("Unable to save files")
        return render_template('error.html',
                                error_message="Something wrong with saving files.")

def save_files(file_list, file_type):
    for file in file_list:
        file_name = secure_filename(file.filename)
        file_path = os.path.join(str(UPLOAD_FOLDER) + file_type)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file.save(os.path.join(file_path, file_type + "_" + file_name))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
