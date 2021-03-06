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
import email_time
import get_prop

EMAIL_PASSWORD = get_prop.get_prop("EMAIL_PASSWORD", "s")
EMAIL_NAME = get_prop.get_prop("EMAIL_NAME", "s")
CHART_FILE = get_prop.get_prop("CHART_FILE", "s") + ".png"
CHECK_FILE = get_prop.get_prop("EMAIL_CHECK_FILE", "s")

EMAILS = get_prop.get_prop("EMAILS", "s")
SEND_TIMES = get_prop.get_prop("SEND_TIMES", "s")
RESET_TIME = get_prop.get_prop("RESET_TIME", "s")
FREQUENCY = get_prop.get_prop("TIME_CHECK_FREQUENCY", "n")

# runner(): void
def runner():
    logger.log_event("Email_sender runner started...")
    times_array = []
    for x in SEND_TIMES:
        times_array.append(email_time.email_time(x))

    while(check_run()):
        logger.log_event("Looping through again...")
        curtime = time.strftime("%H:%M", time.localtime())
        if(curtime == RESET_TIME):
            for x in times_array:
                x.set_passed(False)

        for x in times_array:
            logger.log_event("time is " + str(curtime) + ". Waiting for " + x.get_time())
            if(curtime == x.get_time() and x.has_passed() == False):
                x.set_passed(True)
                try:
                    send_email()

                except:
                    logger.log_error("Couldn't send email")
        time.sleep(FREQUENCY)

    logger.log_event("Email_sender runner() exiting")



# get_str_from_file(filename: String): String
def get_str_from_file(filename):
        file_handle = None
        file_content = None

        try:
            check_file_handle = open(filename)
            file_handle = open(filename, 'r')
            file_content = file_handle.readline()

        except:
            logger.log_error("Couldn't read from " + filename)
            return None

        if(check_file_handle != None):
            check_file_handle.close()

        return file_content

def send_email():
    port = 465

    levels, datetimes = database_wrapper.get_24h_records()
    smooth_levels = data_comp_wrapper.get_smooth_levels(levels)

    inc, dec = data_comp_wrapper.get_inc_dec(smooth_levels)
    inc = round(data_comp_wrapper.percent_to_gallon(inc), 1)
    dec = round(data_comp_wrapper.percent_to_gallon(dec), 1)

    cur_level = round(database_wrapper.get_newest_entry()[0], 1)

    data_comp_wrapper.create_chart(levels, datetimes)
    logger.log_event("Collected data for email")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Well Manager Daily Report " + time.strftime("%b-%d-%Y", time.localtime())
    message["From"] = EMAIL_NAME

    html = f"""\
    <html>
        <body>
            <p>Current Level: {cur_level}%</p>
            <p>Water brought in: {inc} gallons</p>
            <p>Water used: {dec} gallons</p>
        </body>
    </html>
    """
    
    part = MIMEText(html, "html")
    message.attach(part)
    fp = open(CHART_FILE, "rb")
    image = MIMEImage(fp.read())
    fp.close()
    message.attach(image)
    send = smtplib.SMTP_SSL("smtp.gmail.com", port) # start connection
    send.login(EMAIL_NAME, EMAIL_PASSWORD) # login

    for x in EMAILS:
        send.sendmail(EMAIL_NAME, x, message.as_string()) # send message

    send.quit()

def check_run():
    file_text = get_str_from_file(CHECK_FILE)
    if(file_text == "run" or file_text == "run\n"):
        return True
    return False

if(__name__ == "__main__"):
    runner()
    logger.log_event("Email_sender exiting")
