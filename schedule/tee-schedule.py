import schedule
import time
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

def job():
    logging.info("I'm working...")

schedule.every(10).seconds.do(job)
#schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

logging.warning("Starting...")

while True:
    schedule.run_pending()
    time.sleep(1)