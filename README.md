# Draw Names

Customizable Secret Santa Name List Generator

## Overview

The purpose of this script is to:

- Assign each buyer a list of gift receivers for Secret Santa events. The user can specify the number of presents that each buyer should be buying, and the program will ensure that no buyer draws the same name twice.

- Send emails to all Secret Santa participants telling them who to buy a present for.

- Draw a Christmas tree and include it in the email for festivity. The Christmas tree is a String of the following characters: [, ], =, ~.

An example of what the email would look like:

![image](https://user-images.githubusercontent.com/26510814/199185652-82c5feb2-423e-4337-8310-5dd4d7824c68.png)

## Installation

```
git clone https://github.com/tylerlum/DrawNames.git
cd DrawNames
pip install -e .
```

## How To Use

```
python run_draw.py --help
usage: run_draw.py [--name_to_email_dict NAME_TO_EMAIL_DICT]
                   [--name_to_nickname_dict NAME_TO_NICKNAME_DICT]
                   [--n_recipients_per_buyer N_RECIPIENTS_PER_BUYER]
                   [--email_subject_line EMAIL_SUBJECT_LINE]
                   [--email_used_to_send EMAIL_USED_TO_SEND] [-h]

optional arguments:
  --name_to_email_dict NAME_TO_EMAIL_DICT
                        (Dict[str, str], default={'Tyler':
                        'tylergwlum@gmail.com', 'OtherTyler':
                        'pythoncoderdude@gmail.com'}) Tyler
  --name_to_nickname_dict NAME_TO_NICKNAME_DICT
                        (Dict[str, str], default={'Tyler': 'Tygertron',
                        'OtherTyler': 'SwoleDude'}) Tyler
  --n_recipients_per_buyer N_RECIPIENTS_PER_BUYER
                        (int, default=1)
  --email_subject_line EMAIL_SUBJECT_LINE
                        (str, default=Sibling Secret Santa Draw 2023)
  --email_used_to_send EMAIL_USED_TO_SEND
                        (Union[str, NoneType],
                        default=pythoncoderdude@gmail.com)
  -h, --help            show this help message and exit
```

Note:

* It is much easier to modify the default arguments in `run_draw.py` than it is to use the command line directly.

* Most users will need to modify most of the arguments to their specific use case

* Make sure `name_to_nickname_dict` and `name_to_email_dict` have the same keys

- To send an email from a gmail account, this account will need an app password, as gmail has updated its security guidelines. Instructions to get an app password can be found [here](https://support.google.com/mail/answer/185833?hl=en-GB) or by searching "Sign in using app passwords" on Google. Enter this app password when prompted.

### Correct Password

```
python run_draw.py
================================================================================
args = {'email_subject_line': 'Sibling Secret Santa Draw 2023',
 'email_used_to_send': 'pythoncoderdude@gmail.com',
 'n_recipients_per_buyer': 1,
 'name_to_email_dict': {'OtherTyler': 'pythoncoderdude@gmail.com',
                        'Tyler': 'tylergwlum@gmail.com'},
 'name_to_nickname_dict': {'OtherTyler': 'SwoleDude', 'Tyler': 'Tygertron'}}
================================================================================

--------------------------------------------------------------------------------
Reminder: to send emails, pythoncoderdude@gmail.com must have app password set up.
If not set up, refer to https://support.google.com/mail/answer/185833?hl=en-GB or search for 'Sign in using app passwords'
--------------------------------------------------------------------------------

Enter the app password for pythoncoderdude@gmail.com:
Thank you. Password was correct.
Names have been drawn!

Is this a valid assignment? True
Hi Tygertron! You will be buying a lovely present for: SwoleDude. :)

-Tyler Bot

NICKNAMES:
Tyler: Tygertron
OtherTyler: SwoleDude

           []
          [~]
         [~~]
        [~~~]
       [~~~~]
      [~~~~~]
     [~~~~~~]
    [~~~~~~~]
   [~~~~~~~~]
  [~~~~~~~~~]
 [~~~~~~~~~~]
           []
           []
           []

Email sent

Hi SwoleDude! You will be buying a lovely present for: Tygertron. :)

-Tyler Bot

NICKNAMES:
Tyler: Tygertron
OtherTyler: SwoleDude

           []
          [~]
         [~~]
        [~~~]
       [~~~~]
      [~~~~~]
     [~~~~~~]
    [~~~~~~~]
   [~~~~~~~~]
  [~~~~~~~~~]
 [~~~~~~~~~~]
           []
           []
           []

Email sent

Email sent
```

### Wrong Password

```
python run_draw.py
================================================================================
args = {'email_subject_line': 'Sibling Secret Santa Draw 2023',
 'email_used_to_send': 'pythoncoderdude@gmail.com',
 'n_recipients_per_buyer': 1,
 'name_to_email_dict': {'OtherTyler': 'pythoncoderdude@gmail.com',
                        'Tyler': 'tylergwlum@gmail.com'},
 'name_to_nickname_dict': {'OtherTyler': 'SwoleDude', 'Tyler': 'Tygertron'}}
================================================================================

--------------------------------------------------------------------------------
Reminder: to send emails, pythoncoderdude@gmail.com must have app password set up.
If not set up, refer to https://support.google.com/mail/answer/185833?hl=en-GB or search for 'Sign in using app passwords'
--------------------------------------------------------------------------------

Enter the app password for pythoncoderdude@gmail.com:
Traceback (most recent call last):
  File "run_draw.py", line 115, in <module>
    main()
  File "run_draw.py", line 69, in main
    email_sender = EmailSender(user=email_used_to_send, password=app_password)
  File "<string>", line 5, in __init__
  File "/home/tylerlum/github_repos/DrawNames/DrawNames/email_utils.py", line 38, in __post_init__
    self.passwordcheck()
  File "/home/tylerlum/github_repos/DrawNames/DrawNames/email_utils.py", line 33, in passwordcheck
    server.login(self.user, self.password)
  File "/home/tylerlum/miniconda3/envs/rlgpu/lib/python3.7/smtplib.py", line 735, in login
    raise last_exception
  File "/home/tylerlum/miniconda3/envs/rlgpu/lib/python3.7/smtplib.py", line 726, in login
    initial_response_ok=initial_response_ok)
  File "/home/tylerlum/miniconda3/envs/rlgpu/lib/python3.7/smtplib.py", line 647, in auth
    raise SMTPAuthenticationError(code, resp)
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials ju17-20020a170903429100b001c0a4146961sm4804704plb.19 - gsmtp')
```
