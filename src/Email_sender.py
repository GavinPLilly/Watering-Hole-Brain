# Module imports 
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time

# My imports
import logger
import database_wrapper
import data_comp_wrapper

FILE_STUB = "/home/gavin/well-man/WellFlex/Watering-Hole-Brain/files/"

EMAIL_PASSWORD_FILE = FILE_STUB + "email_password"
EMAIL_NAME_FILE = FILE_STUB + "email_name"
CHART_FILE_NAME = FILE_STUB + "chart"
CHECK_FILE = FILE_STUB + "Email_sender_check"

EMAILS = ["gavinlilly25@gmail.com", "gtlilly@hey.com"]
SEND_TIMES = ["18:00"]
RESET_TIME = ["00:00"]

# runner(): void
def runner():
    while(check_run):


# get_str_from_file(filename: String): String
def get_str_from_file(filename):
        file_handle = None
        file_content = None

        try:
            check_file_handle = open 
            file_handle = open(filename, 'r')
            file_content = file_handle.readline()

        except:
            logger.log_error("Couldn't read from " + filename)
            return None

        if(check_file_handle != None):
            check_file_handle.close()

        return file_content

def gen_send_email():
    email = get_str_from_file(EMAIL_PASSWORD_FILE)
    password = get_str_from_file(EMAIL_NAME_FILE)
    port = 465

    def send_email():
        levels, datetimes = database_wrapper.get_24h_records()
        smooth_levels = data_comp_wrapper.get_smooth_levels(levels)
        inc, dec = data_comp_wrapper.get_inc_dec(smooth_levels)
        cur_level = database_wrapper.get_newest_entry()
        chart = data_comp_wrapper.create_chart(levels, datetimes)

        message = MIMEMultipart("alternative")
        message["Subject"] = "Well Manager Daily Report " + time.strftime("%b-%d-%Y", time.localtime())
        message["From"] = email

        html = f"""\
        <html>
            <body>
                <p>Current Level: {cur_level}%</p>
                <p>Water brought in: {inc}%</p>
                <p>Water used: {dec}%</p>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        fp = open(chart, "rb")
        image = MIMEImage(fp.read())
        fp.close()
        message.attach(image)
        send = smtplib.SMTP_SSL("smtp.gmail.com", port) # start connection
        send.login(email, password) # login

        for x in EMAILS:
            send.sendmail(email, x, message.as_string()) # send message

        send.quit()

    error_message = ""
    if(email == None and password == None):
        error_message = "Couldn't get both email and email password from file"
    elif(email == None):
        error_message = "Couldn't get from email string from file"
    elif(password == None):
        error_message = "Couldn'nt get email password from file"

    def error_function():
        logger.log_error("Tried to send email. " + error_message)

    if(error_message != ""):
        return error_function

    return send_email

send_email = gen_send_email()

def check_run():
    file_text = get_str_from_file(CHECK_FILE)
    if(file_text == "run" or file_text == "run\n"):
        return True
    return False

