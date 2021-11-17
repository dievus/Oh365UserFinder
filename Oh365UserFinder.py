import requests as o365request
import argparse
import time
import re
import textwrap
import sys

print("-" * 60)
print("                MayorSec Oh365 User Finder              ")
print("                       Version 1.0.0                    ")
print("                   A project by The Mayor               ")
print("-" * 60)
opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
    '''Example: python3 Oh365UserFinder.py -e test@test.com
Example: python3 Oh365UserFinder.py -r testemails.txt -w valid.txt -v y
Example: python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30 -v y
'''))
opt_parser.add_argument(
    '-e', '--email', help='Runs o365UserFinder against a single email')
opt_parser.add_argument('-r', '--read', help='Reads email addresses from file')
opt_parser.add_argument('-t', '--threading',
                        help='Set threading between checks')
opt_parser.add_argument('-w', '--write', help='Writes valid emails to file')
opt_parser.add_argument('-v', '--verbose', help='Prints output verbosely - use y or n options', metavar=['y', 'n'])
args = opt_parser.parse_args()
ms_url = 'https://login.microsoftonline.com/common/GetCredentialType'


def main():
    if args.email is not None:
        email = args.email
        s = o365request.session()
        body = '{"Username":"%s"}' % email
        request = o365request.post(ms_url, data=body)
        response = request.text
        valid_response = re.search('"IfExistsResult":0,', response)
        invalid_response = re.search('"IfExistsResult":1,', response)
        if invalid_response:
            print("[-] " + email + " - Invalid Email [-]")
        if valid_response:
            print("[+] " + email + " - Valid Email Found! [+]")
        if args.threading is not None:
            time.sleep(int(args.threading))

    elif args.read is not None:
        with open(args.read) as input_emails:
            for line in input_emails:
                s = o365request.session()
                if args.verbose == 'y':
                    print(s)
                email_line = line.split()
                if args.verbose == 'y':
                    print(email_line)
                email = ' '.join(email_line)
                if args.verbose == 'y':
                    print(email)
                body = '{"Username":"%s"}' % email
                if args.verbose == 'y':
                    print(body)
                request = o365request.post(ms_url, data=body)
                if args.verbose == 'y':
                    print(request)
                response = request.text
                if args.verbose == 'y':
                    print(response)
                valid_response = re.search('"IfExistsResult":0,', response)
                if args.verbose == 'y':
                    print(valid_response)
                invalid_response = re.search('"IfExistsResult":1,', response)
                if args.verbose == 'y':
                    print(invalid_response)
                if invalid_response:
                    print("[-] " + email + " - Invalid Email [-]")
                if valid_response:
                    print("[+] " + email + " - Valid Email Found! [+]")
                    if args.write is not None:
                        with open(args.write, 'a+') as valid_emails_file:
                            valid_emails_file.write(email+'\n')
                if args.threading is not None:
                    time.sleep(int(args.threading))
    else:
        sys.exit()


if __name__ == "__main__":
    main()