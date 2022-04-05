# Oh365 User Finder

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

<p align="center">
  <img src="https://github.com/dievus/Oh365UserFinder/blob/main/images/oh365userfinder1.jpg" />
</p>

Oh365UserFinder is used for identifying valid o365 accounts and domains without the risk of account lockouts.  The tool parses responses to identify the "IfExistsResult" flag is null or not, and responds appropriately if the user is valid.  The tool will attempt to identify false positives based on response, and either automatically create a waiting period to allow the throttling value to reset, or warn the user to increase timeouts between attempts.  

Oh365UserFinder can also easily identify if a domain exists in o365 using the -d or --domain flag.  This saves the trouble of copying the url from notes and entering it into the URL bar with the target domain.

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

```-t, --timeout - Sets a pause between attempts in seconds (ex. -t 60)```

```-w, --write - Writes valid emails to a text document (ex. -w validemails.txt)```

```-c, --csv - Writes valid emails to a CSV file (ex. -c validemails.csv)```

```-d, --domain - Checks if the listed domain is valid or not (ex. -d mayorsec.com)```

```--verbose - Outputs test verbosely```

```-ps, --pwspray' - Password sprays a list of accounts using RST```

```-p, --password - Password to be tested```

```-el, --elist - Emails to be tested```

```-gs, --gspray - sword sprays a list of accounts using GRAPH instead of RST```


### Examples Commands

##### ---Validate a Domain Name in O365---
```python3 Oh365Finder.py -d mayorsec.com```

##### ---Validate a single email---
```python3 Oh365UserFinder.py -e test@test.com```

##### ---Validate a list of emails and write to file---
```python3 Oh365UserFinder.py -r testemails.txt -w valid.txt```

##### ---Validate a list of emails, write to file and timeout between requests---
```python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30```

##### ---Validate a list of emails and write to CSV---
```python3 Oh365UserFinder.py -r emails.txt -c validemails.csv -t 30```

### ---Password Spray a list of emails---
```python3 Oh365UserFinder.py -r -p <password> --pwspray --elist <listname>```

##### ---Password Spray a list of emails using GRAPH instead of RST---
```python3 Oh365UserFinder.py -r -p <password> --gspray --elist <listname>```

### Notes
Make note that Microsoft does have some defense in place that can, from time to time, provide false positives in feedback.  If you suspect that this is occurring take a pause in testing, and return and increase the duration between attempts using the -t flag.

### Acknowledgements
This started as a port over from Python2 to Python3 of a tool named o365Creeper developed by Korey Mckinley, and it quickly spiraled into what it is now.
