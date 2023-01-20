# Status Logger for Divera 24/7
This small project has been build to detect if an alarm is currently active and if so it will save how many users responded to the alarm.

## Functionality
The program will send an HTTPS request to the Divera API with the url and accesskey provided in the config file <br>
every minute to check if there is an active alarm. If so, the system will be paused for 10 minutes and will then collect the information <br>
of the alarm, so that the responses of all the users are included too. After that the system is put to sleep again for 2 hours, <br>
because after this time Divera automatically close the alarm and now the program can run normally, without detecting the same alarm twice. <br>
If you have configured Divera to already close the alarm after for example 1 hour, feel free to adapt to code to your needs.

## Installation
1. Download the repository 
2. Execute the setup.sh with  `sudo sh ./setup.sh`
3. Change the config file and add your accesskey
4. Execute the python file `python3 divera_alarm_checker.py`

## Config File
The config file contains the data that is needed to send requests to the Web API. 
```
{
    "url":"https://app.divera247.com/api/last-alarm?accesskey=",
    "accesskey":"YOUR_ACCESSKEY"
}
```

## Log File
When the system is up and running, a log file will be generated in the log directory, 
where you can see the current status of the program.

## Output File
The collected data will be stored in a json file with the name `YYYY-MM-DD_HH-MM.json` (for example `2023-01-20_22-21.json`)
The file contains the following list of information:
- id
- title
- text
- address
- alarmed vehicles
- responses of all users

## Legal Advice
Because of the data protection laws in Germany the program will __NOT__ save any information about the users, 
e.g. to how many alarm one user has responded. The system will __ONLY__ save the number of users in your unit that responded to the alarm.<br>
Furthermore, I would recommend to inform all users about the collection of these 
information or even get their approval.

## Documentation
- Divera 24/7 Web API: https://www.divera247.com/funktionen/datenaustausch-alarmierung/web-api.html
- Python requests: https://www.geeksforgeeks.org/get-post-requests-using-python/