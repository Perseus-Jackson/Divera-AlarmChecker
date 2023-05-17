import requests
import json
import time
import datetime

import logging
logging.basicConfig(filename="./log/alarm_checker.log", level=logging.DEBUG, format='%(asctime)s %(name)s %(message)s')


def load_conf(file):
    logging.debug("Loading configuration")
    json_file = open(file)
    config_json = json.load(json_file)

    conf = {"url": config_json["url"], "accesskey": config_json["accesskey"]}
    logging.debug("Configuration:")
    logging.debug(conf)
    return conf


def write_json(data):
    logging.debug("Writing data to file")

    json_data = {"id": data["id"], "title": data["title"], "text": data["text"], "address": data["address"],
                 "vehicle": data["vehicle"], "answered": data["ucr_answered"],
                 "answeredcount": data["ucr_answeredcount"]}

    logging.debug("JSON Data: " + str(json_data))

    with open("./out/" + alarm_time.strftime("%Y-%m-%d_%H-%M") + ".json", "w") as outfile:
        json.dump(json_data, outfile)

    logging.debug("Writing finished")


def get_data():
    try:
        response = requests.get(config["url"] + config["accesskey"])
        data = json.loads(response.text)

        write_json(data["data"])
    except ConnectionError as e:
        raise e


def check_api(tries=None):
    if tries is None:
        tries = 1
        logging.debug("Calling api")
    else:
        logging.debug("Calling api at try " + str(tries))

    try:
        response = requests.get(config["url"] + config["accesskey"])

        if response.status_code == 200:
            #logging.debug("Code: " + str(response.status_code))
           # logging.debug("Call successfull")

            data = json.loads(response.text)
            if data["success"] and (data["data"]["title"] != "Test Alarmierung" or data["data"]["title"] != "Test Alarmierung"):
                logging.debug("Alarm detected, starting timer")
                global alarm_time
                alarm_time = datetime.datetime.now()
                return 1
            else:
                logging.debug("No Alarm detected")
                return 0
        elif tries <= 5:
            #logging.debug("Code: " + str(response.status_code))
            #logging.debug("ACall failed, retry")
            check_api(tries+1)
        else:
            #logging.debug("Code: " + str(response.status_code))
            logging.debug("Call failed 5th times, aborting")
            return 0
    except ConnectionError as e:
        raise e




def main():
    print("Alarm Checker is running...")
    logging.debug("Logging started")
    global config
    config = load_conf("config.json")
    while 1:
        try:
            alarm_exists = check_api()
            if alarm_exists:
                time.sleep(600)
                get_data()
                time.sleep(7200)
            else:
                time.sleep(60)
        except Exception as e:
            logging.debug("An Error occured: " + str(e))
            time.sleep(60)


if __name__ == "__main__":
    main()