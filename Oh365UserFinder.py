#!/usr/bin/python3
import requests as o365request
import argparse
import time
import re
import textwrap
import sys
from datetime import datetime
from requests.api import request

def banner():
    print("   ____  __   _____ _____ ______   __  __                  _______           __         ")
    print("  / __ \/ /_ |__  // ___// ____/  / / / /_______  _____   / ____(_)___  ____/ /__  _____")
    print(" / / / / __ \ /_ </ __ \/___ \   / / / / ___/ _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/")
    print("/ /_/ / / / /__/ / /_/ /___/ /  / /_/ (__  )  __/ /     / __/ / / / / / /_/ /  __/ /    ")
    print("\____/_/ /_/____/\____/_____/   \____/____/\___/_/     /_/   /_/_/ /_/\__,_/\___/_/     \n")
    print("                                   Version 1.0.0                                        ")
    print("                               A project by The Mayor                                   ")
    print("                        Oh365UserFinder.py -h to get started                            \n")                                                                                    
    print("-" * 90)
    print(f'\n[info] Starting Oh365 User Finder at {time.ctime()}\n')

opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
    '''Example: python3 Oh365UserFinder.py -e test@test.com
Example: python3 Oh365UserFinder.py -r testemails.txt -w valid.txt --verbose
Example: python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30 --verbose
Example: python3 Oh365UserFinder.py -r emails.txt -c validemails.csv -t 30
Example: python3 Oh365Finder.py -d mayorsec.com
'''))
opt_parser.add_argument(
    '-e', '--email', help='Runs o365UserFinder against a single email')
opt_parser.add_argument('-r', '--read', help='Reads email addresses from file')
opt_parser.add_argument(
    '-t', '--timeout', help='Set timeout between checks to avoid false positives')
opt_parser.add_argument(
    '-w', '--write', help='Writes valid emails to text file')
opt_parser.add_argument(
    '-c', '--csv', help='Writes valid emails to a .csv file')
opt_parser.add_argument('-d', '--domain', help='Validate if a domain exists')
opt_parser.add_argument(
    '-v', '--verbose', help='Prints output verbosely', action='store_true')

args = opt_parser.parse_args()
ms_url = 'https://login.microsoftonline.com/common/GetCredentialType'


def main():
    if args.timeout is not None:
        print(
            f'[info] Timeout set to {args.timeout} seconds between requests.\n')
    counter = 0
    t1 = datetime.now()
    if args.email is not None:
        email = args.email
        s = o365request.session()
        body = '{"Username":"%s"}' % email
        request = o365request.post(ms_url, data=body)
        response = request.text
        valid_response = re.search('"IfExistsResult":0,', response)
        valid_response5 = re.search('"IfExistsResult":5,', response)
        valid_response6 = re.search('"IfExistsResult":6,', response)
        invalid_response = re.search('"IfExistsResult":1,', response)
        if args.verbose:
            print('\n', email, s, body, request, response, valid_response,
                  valid_response5, valid_response6, invalid_response, '\n')
        if invalid_response:
            a = email
            b = " Result - Invalid Email Found! [-]"
            print(f"[-] {a:51} {b}")
        if valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result - Valid Email Found! [+]"
            print(f"[+] {a:53} {b}")
        if args.timeout is not None:
            time.sleep(int(args.timeout))

    elif args.read is not None:
        with open(args.read) as input_emails:
            for line in input_emails:
                s = o365request.session()
                email_line = line.split()
                email = ' '.join(email_line)
                body = '{"Username":"%s"}' % email
                request = o365request.post(ms_url, data=body)
                response = request.text
                valid_response = re.search('"IfExistsResult":0,', response)
                valid_response5 = re.search('"IfExistsResult":5,', response)
                valid_response6 = re.search('"IfExistsResult":6,', response)
                invalid_response = re.search('"IfExistsResult":1,', response)
                if args.verbose:
                    print('\n', email, s, email_line, body, request, response, valid_response,
                          valid_response5, valid_response6, invalid_response, '\n')
                if invalid_response:
                    a = email
                    b = " Result - Invalid Email Found! [-]"
                    print(f"[-] {a:51} {b}")
                if valid_response or valid_response5 or valid_response6:
                    a = email
                    b = " Result -   Valid Email Found! [+]"
                    print(f"[+] {a:51} {b}")
                    counter = counter + 1
                    if args.write is not None:
                        a = email
                        with open(args.write, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")
                    elif args.csv is not None:
                        a = email
                        with open(args.csv, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")

                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print('\n[-] There were no valid logins found. [-]\n')
                print(f'\n[info] Scan completed at {time.ctime()}')
            elif counter == 1:
                print(
                    '\n[info] Oh365 User Finder discovered one valid login account.')
                print(f'\n[info] Scan completed at {time.ctime()}')
            else:
                print(
                    f'\n[info] Oh365 User Finder discovered {counter} valid login accounts.\n')
                print(f'\n[info] Scan completed at {time.ctime()}')

    elif args.domain is not None:
        domain_name = args.domain
        print(f"[info] Checking if the {domain_name} exists...\n")
        url = (
            f"https://login.microsoftonline.com/getuserrealm.srf?login=user@{domain_name}")
        request = o365request.get(url)
        response = request.text
        valid_response = re.search('"NameSpaceType":"Managed",', response)
        if args.verbose:
            print(domain_name, request, response, valid_response)
        if valid_response:
            print(f"[success] The listed domain {domain_name} exists.")
        else:
            print(f"[info] The listed domain {domain_name} does not exist.")
        print(f'[info] Scan completed at {time.ctime()}')
    else:
        sys.exit()


if __name__ == "__main__":
    try:
        banner()
        main()

    except KeyboardInterrupt:
        print("\nYou either fat fingered this, or meant to do it. Either way, goodbye!")
        quit()
