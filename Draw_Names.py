# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] id="view-in-github" colab_type="text"
# <a href="https://colab.research.google.com/github/tylerlum/DrawNames/blob/master/Draw_Names.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %% [markdown] id="SbXNYzQ1nBZw" colab_type="text"
# # Draw Names
#
# Customizable Secret Santa Name List Generator
#
# ## Overview
#
# The purpose of this script is to:
#
# * Assign each buyer a list of gift receivers for Secret Santa events. The user can specify the number of presents that each buyer should be buying, and the program will ensure that no buyer draws the same name twice.
#
# * Send emails to all Secret Santa participants telling them who to buy a present for.
#
# * Draw a Christmas tree and include it in the email for festivity. The Christmas tree is a String of the following characters: [, ], =, ~.
#
# ## How To Use
#
# * The easiest way to use this code is to use a Jupyter Notebook on a local machine (may encounter issues sending emails from a Google Colab notebook).
#
# * Then you can customize `NAME_TO_EMAIL_DICT` and `NAME_TO_NICKNAME_DICT` to have the emails and nicknames you want (make sure they all have the same real names).
#
# * Next, you will need to have an email used to send the gift assignments out. If this is a gmail account, this account will need an app password, as gmail has updated its security guidelines. Instructions to get an app password can be found [here](https://support.google.com/mail/answer/185833?hl=en-GB) or by searching "Sign in using app passwords" on Google.
#
# * Lastly, run all cells and input the email and app password when prompted.

# %% [markdown] id="Gr8bZSVpm-Ru" colab_type="text"
# ## Dependencies and Functions
#
#

# %% id="WhL5kNkRm4Km" colab_type="code" colab={}
import random
from copy import deepcopy
import smtplib
import datetime


# %% [markdown] id="Fs9Q8t1ynU1m" colab_type="text"
# ### Low Level Functions for Drawing Names

# %% id="3W7Qe3qek1IO" colab_type="code" colab={}
def is_valid_assignment(buyer_to_recipient_dicts):
    """Check if assignments are valid.

    Assignments are valid if (for every buyer), (their recipients are unique, no repeats)
    If buyer_to_recipient_dicts is empty, returns True
    """
    first_buyer_to_recipient_dict = buyer_to_recipient_dicts[0]
    buyers = list(first_buyer_to_recipient_dict.keys())
    for buyer in buyers:
        recipients = [buyer_to_recipient_dict[buyer] for buyer_to_recipient_dict in buyer_to_recipient_dicts]
        if any(recipients.count(recipient) > 1 for recipient in recipients):
            return False
    return True


def convert_key_to_val_dicts_into_key_to_vals_dict(key_to_val_dicts):
    """
    convert_key_to_val_dicts_into_key_to_vals_dict
    list(dict(key, val)) => dict(key, list(vals))
    """
    # Empty list => empty dict
    if len(key_to_val_dicts) == 0:
        return {}

    # Ensure that all dicts have the same keys
    keys = list(key_to_val_dicts[0].keys())
    for key_to_val_dict in key_to_val_dicts:
        assert(set(keys) == set(key_to_val_dict.keys()))

    # Create new dict
    key_to_vals_dict = {}
    for key in keys:
        key_to_vals_dict[key] = [key_to_val_dict[key]
                                 for key_to_val_dict in key_to_val_dicts]
    return key_to_vals_dict


def add_one_new_recipient_per_buyer(buyer_to_recipient_dicts, full_name_list):
    """Create a new buyer_to_recipient_dict, with no repeats.

    No repeats means that a buyer won't buy for the same person more than once
    """
    MAX_NUM_TRIES = 1000
    for _ in range(MAX_NUM_TRIES):
        # Create new dict
        new_buyer_to_recipient_dict = draw_names_one_recipient_per_buyer(full_name_list)

        # Check if it worked
        new_buyer_to_recipient_dicts = deepcopy(buyer_to_recipient_dicts)
        new_buyer_to_recipient_dicts.append(new_buyer_to_recipient_dict)
        if (is_valid_assignment(new_buyer_to_recipient_dicts)):
            # Worked, add to list
            buyer_to_recipient_dicts.append(new_buyer_to_recipient_dict)
            return

    raise ValueError("Unable to add one new recipient per buyer after {0} tries".format(MAX_NUM_TRIES))


# %% [markdown] id="FPmEjmktnaqF" colab_type="text"
# ### High Level Functions for Drawing Names

# %% id="I5fefJkXndPJ" colab_type="code" colab={}
def try_draw_names_one_recipient_per_buyer(full_name_list):
    """Try to assign each buyer one recipient

    Returns empty dict if unsuccessful
    """
    recipient_list = list(full_name_list)
    assignment_dict = {}

    for buyer in full_name_list:
        # If no available recipients, then failed
        available_recipients = [name for name in recipient_list if name != buyer]
        if (len(available_recipients) == 0):
            return {}

        # Get random available recipient
        recipient = random.choice(available_recipients)

        # Remove recipient from recipient list
        recipient_list.remove(recipient)

        # Add buyer -> recipient pair
        assignment_dict[buyer] = recipient
    return assignment_dict


def draw_names_one_recipient_per_buyer(full_name_list):
    """Assign each buyer one recipient"""
    assignment_dict = {}
    while len(assignment_dict) == 0:
        assignment_dict = try_draw_names_one_recipient_per_buyer(full_name_list)
    return assignment_dict


def draw_names(full_name_list, recipients_per_buyer):
    """Assign each buyer n distinct recipients (n = recipients_per_buyer)

    Done such that each person gets n gifts.

    Requires n > 0
    """

    # Check valid input
    if recipients_per_buyer >= len(full_name_list):
        print("Too many recipients per buyer")
        return
    if recipients_per_buyer < 1:
        print("Too few recipients per buyer")
        return

    # Continuously draw names, getting one more recipient per buyer each loop
    buyer_to_recipient_dicts = []
    while (len(buyer_to_recipient_dicts) < recipients_per_buyer):
        add_one_new_recipient_per_buyer(buyer_to_recipient_dicts, full_name_list)

    # Put Assignments together
    buyer_to_recipients_dict = convert_key_to_val_dicts_into_key_to_vals_dict(buyer_to_recipient_dicts)

    return buyer_to_recipients_dict


# %% [markdown] id="OqDcGBocn-TE" colab_type="text"
# ### Function for sending emails

# %% id="N77u5tKOk1Ic" colab_type="code" colab={}
########### Sending Email ##########
def send_email(TO, SUBJECT, BODY, USER, PASSWORD):

    email_text = """\
From: %s  
To: %s  
Subject: %s

%s
""" % (USER, ", ".join(TO), SUBJECT, BODY)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(USER, PASSWORD)
        server.sendmail(USER, TO, email_text)
        server.close()

        print("Email sent")
    except Exception as e:
        print("Something went wrong")
        print(e)


# %% [markdown] id="bu1_4XF7oIU1" colab_type="text"
# ### Function for making trees

# %% id="BKl50YJsk1In" colab_type="code" colab={}
def make_tree(n, s):
    """Returns string representing a tree"""
    tree = ""
    for i in range(n):
        for a in range(n-i):
            tree = tree + " "
        tree = tree + "["
        # Added reduce length to half the width (didn't look good on email)
        reduce_length = 0
        for l in range(i << 1):
            if i == n-1:
                reduce_length = reduce_length + 1
                if reduce_length % 2 == 0:
                    # tree = tree + "_"  # This leads to inconsistent sizing in some emails
                    tree = tree + "~"
            else:
                reduce_length = reduce_length + 1
                if reduce_length % 2 == 0:
                    tree = tree + "~"
        tree = tree + "]\n"
    for o in range(s):
        for i in range(n):
            tree = tree + " "
        tree = tree + "[]\n"
    return tree


# %% [markdown] id="AjN9rU8F6JYD" colab_type="text"
# ### Helper print function

# %% id="imdCu36Ok1Iy" colab_type="code" colab={}
def show_dict(dict):
    """Output Dictionary Content into String"""
    return "\n".join(["{0}: {1}".format(key, value) for key, value in dict.items()])


# %% id="Z7jvqBEX7ywo" colab_type="code" colab={}
def str_with_ands_between(names):
    return " and ".join(names)


# %% [markdown] id="mrxEwSLvzoZg" colab_type="text"
# ## Testing

# %% [markdown] id="ASVVOdN55Lk3" colab_type="text"
# ### Testing Methods

# %% id="KN6BuJELzn7D" colab_type="code" colab={}
def is_valid_drawn_names(buyer_to_recipients_dict, recipients_per_buyer):
    return (buyer_has_unique_recipients(buyer_to_recipients_dict) and each_person_gets_equal_number_of_gifts(buyer_to_recipients_dict, recipients_per_buyer)
            and each_buyer_buys_correct_number_of_gifts(buyer_to_recipients_dict, recipients_per_buyer) and no_buyer_buys_for_themselves(buyer_to_recipients_dict))


def buyer_has_unique_recipients(buyer_to_recipients_dict):
    for recipients in buyer_to_recipients_dict.values():
        if any(recipients.count(recipient) > 1 for recipient in recipients):
            return False
    return True


def each_person_gets_equal_number_of_gifts(buyer_to_recipients_dict, recipients_per_buyer):
    names = buyer_to_recipients_dict.keys()
    for name in names:
        num_gifts = 0
        for recipients in buyer_to_recipients_dict.values():
            if name in recipients:
                num_gifts += 1
        if not num_gifts == recipients_per_buyer:
            return False
    return True


def each_buyer_buys_correct_number_of_gifts(buyer_to_recipients_dict, recipients_per_buyer):
    for recipients in buyer_to_recipients_dict.values():
        if not len(recipients) == recipients_per_buyer:
            return False
    return True


def no_buyer_buys_for_themselves(buyer_to_recipients_dict):
    for buyer in buyer_to_recipients_dict:
        if buyer in buyer_to_recipients_dict[buyer]:
            return False
    return True


# %% [markdown] id="HtuVziko2uSm" colab_type="text"
# ### Run Validation Tests

# %% id="wXjV9BEK2t9Y" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 34} outputId="b673b60e-b801-4818-a89d-fe8d6c8a09fd"
TEST_NUM_TESTS = 20
TEST_NAMES = ['Ben', 'Aaron', 'Joel', 'Angela', 'Zoe', 'Ken']
TEST_RECIPIENTS_PER_BUYER_MIN = 1
TEST_RECIPIENTS_PER_BUYER_MAX = 4
passed = True
for recipients_per_buyer in range(TEST_RECIPIENTS_PER_BUYER_MIN, TEST_RECIPIENTS_PER_BUYER_MAX):
    for test_num in range(TEST_NUM_TESTS):
        test_results = draw_names(TEST_NAMES, recipients_per_buyer)
        if not is_valid_drawn_names(test_results, recipients_per_buyer):
            passed = False
            print("FAILED TEST {0} with {1} recipients_per_buyer.".format(test_num, recipients_per_buyer))

if passed:
    print("Passed {0} tests :)".format(TEST_NUM_TESTS *
          (TEST_RECIPIENTS_PER_BUYER_MAX - TEST_RECIPIENTS_PER_BUYER_MIN + 1)))

# %% [markdown] id="_eqqPVSM4gX6" colab_type="text"
# ## Example Usage

# %% id="KOr58qgo5c1e" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 89} outputId="8f62b922-7a47-4422-860f-80ddafafb364"
EXAMPLE_NAMES = ['Ben', 'Aaron', 'Joel', 'Angela', 'Zoe', 'Ken']
EXAMPLE_RECIPIENTS_PER_BUYER = 3

EXAMPLE_BUYER_TO_RECIPIENTS_DICT = draw_names(EXAMPLE_NAMES, EXAMPLE_RECIPIENTS_PER_BUYER)

print("Example drawn names: {}\n".format(EXAMPLE_BUYER_TO_RECIPIENTS_DICT))
print("Is this a valid assignment? {}".format(is_valid_drawn_names(
    EXAMPLE_BUYER_TO_RECIPIENTS_DICT, EXAMPLE_RECIPIENTS_PER_BUYER)))

# %% [markdown] id="SHoNnMZzmrjQ" colab_type="text"
# ## Main Program
#
# Steps:
#
# 1. Fill in NAME_TO_EMAIL_DICT and NAME_TO_NICKNAME_DICT
#
# 2. Fill in RECIPIENTS_PER_BUYER
#
# Run both cells

# %% id="uELDFFEcqjXS" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 69} outputId="624ab317-37b8-4c40-dc05-f237d2b4787e"
# Setup emails and names
NAME_TO_EMAIL_DICT = {"Tyler": "tylergwlum@gmail.com",
                      'OtherTyler': "pythoncoderdude@gmail.com", }
NAME_TO_NICKNAME_DICT = {"Tyler": "Tygertron",
                         'OtherTyler': 'SwoleDude', }
EMAIL_USED_TO_SEND = input("Enter the email address you will use to send gift assignments: ")
APP_PASSWORD = input("Enter the app password for {0}: ".format(EMAIL_USED_TO_SEND))
NAMES = list(NAME_TO_EMAIL_DICT.keys())
RECIPIENTS_PER_BUYER = 1

# Get assignment
buyer_to_recipients_dict = draw_names(NAMES, RECIPIENTS_PER_BUYER)
print("Names have been drawn!\n")
print("Is this a valid assignment? {}".format(is_valid_drawn_names(buyer_to_recipients_dict, RECIPIENTS_PER_BUYER)))

# %% id="Jj_Nx8RVk1I9" colab_type="code" colab={}
# Send emails
for buyer in buyer_to_recipients_dict:
    recipients = buyer_to_recipients_dict[buyer]

    # Get nicknames
    buyer_nickname = NAME_TO_NICKNAME_DICT[buyer]
    recipient_nicknames = [NAME_TO_NICKNAME_DICT[recipient] for recipient in recipients]

    # Write email body
    email_body = "Hi {0}! You will be buying a lovely present for: {1}. :)".format(
        buyer_nickname, str_with_ands_between(recipient_nicknames))

    # From statement
    email_body = email_body + "\n\n-Tyler Bot"

    # Nickname explanation
    email_body = email_body + "\n\nNICKNAMES:\n{0}".format(show_dict(NAME_TO_NICKNAME_DICT))

    # Add tree
    email_body = email_body + "\n\n" + make_tree(11, 3)

    # Subject
    subject = "Sibling Secret Santa Draw {}".format(datetime.datetime.now().year)

    print(email_body)
    send_email([NAME_TO_EMAIL_DICT[buyer]], subject, email_body, EMAIL_USED_TO_SEND, APP_PASSWORD)

# Send email of actual draw to email used to send
send_email([EMAIL_USED_TO_SEND],
           "Sibling Secret Santa Real List {0}".format(datetime.datetime.now().year),
           "{0}".format(buyer_to_recipients_dict),
           EMAIL_USED_TO_SEND, APP_PASSWORD)

# %%
