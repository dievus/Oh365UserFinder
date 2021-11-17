# Oh365UserFinder

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

![Oh365UserFinder](/images/Oh365UserFinder.png)

Oh365UserFinder is used for identifying valid o365 accounts without the risk of account lockouts.  The tool parses responses to identify the "IfExistsResult" flag is null or not, and responds appropriately if the user is valid.  

## Usage
Installing Oh365UserFinder
```git clone https://github.com/dievus/Oh365UserFinder.git```

Change directories to Oh365UserFinder and run:
```pip3 install -r requirements.txt```
This will run the install script to add necessary dependencies to your system.

```python3 Oh365UserFinder.py -h```
This will output the help menu, which contains the following flags:
```-h, --help - Lists the help options```
```-e, --email - Required for running Oh365UserFinder against a single email account```
```-r, --read - Reads from a text file containing emails (ex. -r emails.txt)```
```-w, --write - Writes valid emails to a text document (ex. -w validemails.txt)```
```-t, --threading - Sets a pause between attempts in seconds (ex. -t 60)```
```-v, --verbose - Outputs test verbosely; note that you must use y to run verbosely (ex. -v y)```

Examples of full commands include:
```python3 o365UserFinder.py -e example@test.com```
```python3 Oh365UserFinder.py -r emails.txt -w validemails.txt```
```python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30 -v y```



### Acknowledgements
This project is based on a previous tool named o365Creeper developed by Korey Mckinley that was last supported in 2019, and developed in Python2.  
