#!/usr/bin/python3
import requests as o365request
import argparse
import time
import re
import textwrap
import sys
import os
from datetime import datetime
def sysID():
    if sys.platform.startswith('win32'):
        global k
        from ctypes import windll
        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)

def banner():
    print("\033[33;1m")
    print("    ____  __   _____ _____ ______   __  __                  _______           __          ")
    print(f"  / __ \/ /_ |__  // ___// ____/  / / / /_______  _____   / ____(_)___  ____/ /__  _____")
    print(" / / / / __ \ /_ </ __ \/___ \   / / / / ___/ _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/ ")
    print("/ /_/ / / / /__/ / /_/ /___/ /  / /_/ (__  )  __/ /     / __/ / / / / / /_/ /  __/ /     ")
    print("\____/_/ /_/____/\____/_____/   \____/____/\___/_/     /_/   /_/_/ /_/\__,_/\___/_/     \n")
    print("                                   Version 1.0.1                                         ")
    print("                               A project by The Mayor                                    ")
    print("                        Oh365UserFinder.py -h to get started                            \x1b[0m\n")
    print("-" * 90)
    print(f'\n\033[33;1m[info] Starting Oh365 User Finder at {time.ctime()}\n\x1b[0m')


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
            f'\033[33;1m[info] Timeout set to {args.timeout} seconds between requests.\x1b[0m\n')
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
        throttling = re.search('"ThrottleStatus":1', response)
        if args.verbose:
            print('\n', email,s, body, request, response, valid_response,
                  valid_response5, valid_response6, invalid_response, '\n')
        if invalid_response:
            a = email
            b = " Result - Invalid Email Found! [-]"
            print(f"\033[91m[-] {a:51} {b}\x1b[0m")
        if valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result - Valid Email Found! [+]"
            print(f"\033[92m[+] {a:53} {b} \x1b[0m")
        if throttling:
            print("\n\033[91m[warn] Results suggest o365 is responding with false positives. Restart scan and use the -t flag to slow request times.\x1b[0m")
            sys.exit()
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
                throttling = re.search('"ThrottleStatus":1', response)
                if args.verbose:
                    print('\n', s, email_line, email, body, request, response, valid_response,
                          valid_response5, valid_response6, invalid_response, '\n')
                if invalid_response:
                    a = email
                    b = " Result - Invalid Email Found! [-]"
                    print(f"\033[91m[-] {a:51} {b}\x1b[0m")
                if valid_response or valid_response5 or valid_response6:
                    a = email
                    b = " Result -   Valid Email Found! [+]"
                    print(f"\033[92m[+] {a:51} {b}\x1b[0m")
                    counter = counter + 1
                    if args.write is not None:
                        a = email
                        with open(args.write, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")
                    elif args.csv is not None:
                        a = email
                        with open(args.csv, 'a+') as valid_emails_file:
                            valid_emails_file.write(f"{a}\n")
                if throttling:
                    print("\n\033[91m[warn] Results suggest o365 is responding with false positives. Restart scan and use the -t flag to slow request times.\x1b[0m")
                    sys.exit()
                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print('\n\033[91m[-] There were no valid logins found. [-]\x1b[0m\n')
                print(f'\n\033[33;1m[info] Scan completed at {time.ctime()}\x1b[0m')
            elif counter == 1:
                print(
                    '\n\033[92m[info] Oh365 User Finder discovered one valid login account.\x1b[0m')
                print(f'\n\033[33;1m[info] Scan completed at {time.ctime()}')
            else:
                print(
                    f'\n\033[92m[info] Oh365 User Finder discovered {counter} valid login accounts.\x1b[0m\n')
                print(f'\n\033[33;1m[info] Scan completed at {time.ctime()}\x1b[0m')

    elif args.domain is not None:
        domain_name = args.domain
        print(f"\033[33;1m[info] Checking if the {domain_name} exists...\x1b[0m\n")
        url = (
            f"https://login.microsoftonline.com/getuserrealm.srf?login=user@{domain_name}")
        request = o365request.get(url)
        response = request.text
        valid_response = re.search('"NameSpaceType":"Managed",', response)
        if args.verbose:
            print(domain_name, request, response, valid_response)
        if valid_response:
            print(f"\n\033[92m[success] The listed domain {domain_name} exists.\n")
        else:
            print(f"\033[91m[info] The listed domain {domain_name} does not exist.\n")
        print(f'\033[33;1m[info] Scan completed at {time.ctime()}')
    else:
        sys.exit()


if __name__ == "__main__":
    try:
        sysID()
        banner()
        main()

    except KeyboardInterrupt:
        print("\nYou either fat fingered this, or meant to do it. Either way, goodbye!")
        quit()
