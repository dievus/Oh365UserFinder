import requests as o365request
import argparse
import time
import re
import textwrap
import sys
from datetime import datetime

print("-" * 60)
print("                MayorSec Oh365 User Finder              ")
print("                       Version 1.0.0                    ")
print("                   A project by The Mayor               ")
print("           Oh365UserFinder.py -h to get started         ")
print("-" * 60)
opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
    '''Example: python3 Oh365UserFinder.py -e test@test.com
Example: python3 Oh365UserFinder.py -r testemails.txt -w valid.txt --verbose
Example: python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30 --verbose
Example: python3 Oh365UserFinder.py -r emails.txt -c validemails.csv -t 30
'''))
opt_parser.add_argument(
    '-e', '--email', help='Runs o365UserFinder against a single email')
opt_parser.add_argument('-r', '--read', help='Reads email addresses from file')
opt_parser.add_argument('-t', '--timeout',
                        help='Set timeout between checks to avoid false positives')
opt_parser.add_argument(
    '-w', '--write', help='Writes valid emails to text file')
opt_parser.add_argument(
    '-c', '--csv', help='Writes valid emails to a .csv file')
opt_parser.add_argument(
    '--verbose', help='Prints output verbosely', action='store_true')
args = opt_parser.parse_args()
ms_url = 'https://login.microsoftonline.com/common/GetCredentialType'

print(f'[info] Starting Oh365 User Finder at {time.ctime()}\n')


def main():
    if args.timeout is not None:
        print(
            f'\n[info] Timeout set to {args.timeout} seconds between requests.\n')
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
            print(s, email, body, request, response, valid_response,
                  valid_response5, valid_response6, invalid_response, '\n')
        if invalid_response:
            a = email
            b = " Result - Invalid Email Found! [-]"
            print(f"[-] {a:20} {b}")
        if valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result - Valid Email Found! [+]"
            print(f"[+] {a:20} {b}")
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
                    print(s, email_line, email, body, request, response, valid_response,
                          valid_response5, valid_response6, invalid_response, '\n')
                if invalid_response:
                    a = email
                    b = " Result - Invalid Email Found! [-]"
                    print(f"[-] {a:30} {b}")
                if valid_response or valid_response5 or valid_response6:
                    a = email
                    b = " Result - Valid Email Found! [+]"
                    print(f"[+] {a:30} {b}")
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

    else:
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nYou either fat fingered this, or meant to do it. Either way, goodbye!")
        quit()
