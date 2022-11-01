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
# Customize-able Secret Santa Name List Generator
#
# The purpose of this script is to:
#
# * Assign buyers and receivers for Secret Santa events. The user can specify the number of presents that each buyer should be buying, and the program will ensure that no buyer draws the same name twice.
#
# * Send emails to all Secret Santa participants telling them who to buy a present for.
#
# * Draw a Christmas tree and include it in the email for festivity. The Christmas tree is a String of the following characters: [, ], =, ~.
#
#
# How to Use: The easiest way to use this code is to use Jupyter Notebook or Google Colab notebook. Then you can customize the email settings and names and then run all!

# %% [markdown] id="Gr8bZSVpm-Ru" colab_type="text"
# ## Dependencies and Functions
#
#

# %% id="WhL5kNkRm4Km" colab_type="code" colab={}
import random
from copy import deepcopy, copy
import smtplib
import datetime


# %% [markdown] id="Fs9Q8t1ynU1m" colab_type="text"
# ### Low Level Functions for Drawing Names

# %% id="3W7Qe3qek1IO" colab_type="code" colab={}
def remove_name_from_list(name_list, remove_name):
    """Return deep copy of name_list with remove_name removed

    If remove_names not in name_list, returns a deepcopy of name_list
    """
    shortened_list = deepcopy(name_list)
    if remove_name in shortened_list:
        shortened_list.remove(remove_name)
    return shortened_list


def is_valid_assignment(recipient_by_buyer_list):
    """Check if assignments are valid.

    Assignments are valid if (for every buyer), (their recipients are unique, no repeats)
    If recipient_by_buyer_list is empty, returns True
    """
    for buyer in recipient_by_buyer_list[0]:
        recipients = [recipient_by_buyer_list[i][buyer] for i in range(len(recipient_by_buyer_list))]
        if any(recipients.count(recipient) > 1 for recipient in recipients):
            return False
    return True


def convert_recipient_by_buyer_list_to_recipients_by_buyer(recipient_by_buyer_list):
    """convert_recipient_by_buyer_list_to_recipients_by_buyer
    list(dict(buyer, recipient)) => dict(buyer, list(recipient))

    Requires: recipient_by_buyer_list not empty
    """
    # Setup final dict and first assignment
    recipients_by_buyer = {}

    # Combine the recipients of each buyer
    for buyer in recipient_by_buyer_list[0]:
        recipients = []
        for recipient_by_buyer in recipient_by_buyer_list:
            recipients.append(recipient_by_buyer[buyer])
        recipients_by_buyer[buyer] = recipients
    return recipients_by_buyer


def get_one_new_recipient_per_buyer(recipient_by_buyer_list, full_name_list):
    """Create a new recipient_by_buyer, with no repeats.

    No repeats means that a buyer won't buy for the same person more than once
    """
    while(True):
        new_recipient_by_buyer = draw_names_one_recipient_per_buyer(full_name_list)
        new_recipient_by_buyer_list = deepcopy(recipient_by_buyer_list)
        new_recipient_by_buyer_list.append(new_recipient_by_buyer)
        if (is_valid_assignment(new_recipient_by_buyer_list)):
            return new_recipient_by_buyer


# %% [markdown] id="FPmEjmktnaqF" colab_type="text"
# ### High Level Functions for Drawing Names

# %% id="I5fefJkXndPJ" colab_type="code" colab={}
def try_draw_names_one_recipient_per_buyer(full_name_list, assignment_dict):
    """Try to assign each buyer one recipient

    Modifies assignment_dict

    Returns True if successful, otherwise returns False
    """
    recipient_list = deepcopy(full_name_list)

    for buyer in full_name_list:
        # If no available recipients, then failed
        available_recipients = remove_name_from_list(recipient_list, buyer)
        if (len(available_recipients) == 0):
            assignment_dict = {}
            return False

        # Get random available recipient
        recipient = random.choice(available_recipients)

        # Remove recipient from recipient list
        recipient_list.remove(recipient)

        # Add buyer -> recipient pair
        assignment_dict[buyer] = recipient
    return True


def draw_names_one_recipient_per_buyer(full_name_list):
    """Assign each buyer one recipient"""
    success = False
    while (not success):
        assignment_dict = {}
        success = try_draw_names_one_recipient_per_buyer(full_name_list, assignment_dict)
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
    recipient_by_buyer_list = []
    while (len(recipient_by_buyer_list) < recipients_per_buyer):
        new_recipient_by_buyer = get_one_new_recipient_per_buyer(recipient_by_buyer_list, full_name_list)
        recipient_by_buyer_list.append(new_recipient_by_buyer)

    # Put Assignments together
    recipients_by_buyer = convert_recipient_by_buyer_list_to_recipients_by_buyer(recipient_by_buyer_list)

    return recipients_by_buyer


# %% [markdown] id="OqDcGBocn-TE" colab_type="text"
# ### Function for sending emails

# %% id="N77u5tKOk1Ic" colab_type="code" colab={}
########### Sending Email ##########
def send_email(TO, SUBJECT, BODY, USER="learningpython640@gmail.com", PASSWORD="ilearnpython"):

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
    except:
        print("Something went wrong")


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
                    tree = tree + "_"
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
    dict_output = ""
    for key in dict:
        dict_output = dict_output + "{0}: {1}\n".format(key, dict[key])
    return dict_output


# %% id="Z7jvqBEX7ywo" colab_type="code" colab={}
def str_with_ands_between(names):
    return_value = ""
    for i, name in enumerate(names):
        return_value += name
        if i != len(names) - 1:
            return_value += " and "
    return return_value


# %% [markdown] id="mrxEwSLvzoZg" colab_type="text"
# ## Testing

# %% [markdown] id="ASVVOdN55Lk3" colab_type="text"
# ### Testing Methods

# %% id="KN6BuJELzn7D" colab_type="code" colab={}
def is_valid_drawn_names(recipients_by_buyer, recipients_per_buyer):
    return (buyer_has_unique_recipients(recipients_by_buyer) and each_person_gets_equal_number_of_gifts(recipients_by_buyer, recipients_per_buyer)
            and each_buyer_buys_correct_number_of_gifts(recipients_by_buyer, recipients_per_buyer) and no_buyer_buys_for_themselves(recipients_by_buyer))


def buyer_has_unique_recipients(recipients_by_buyer):
    for buyer, recipients in recipients_by_buyer.items():
        if any(recipients.count(recipient) > 1 for recipient in recipients):
            return False
    return True


def each_person_gets_equal_number_of_gifts(recipients_by_buyer, recipients_per_buyer):
    names = recipients_by_buyer.keys()
    for name in names:
        num_gifts = 0
        for buyer, recipients in recipients_by_buyer.items():
            if name in recipients:
                num_gifts += 1
        if not num_gifts == recipients_per_buyer:
            return False
    return True


def each_buyer_buys_correct_number_of_gifts(recipients_by_buyer, recipients_per_buyer):
    for buyer, recipients in recipients_by_buyer.items():
        if not len(recipients) == recipients_per_buyer:
            return False
    return True


def no_buyer_buys_for_themselves(recipients_by_buyer):
    for buyer in recipients_by_buyer:
        if buyer in recipients_by_buyer[buyer]:
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

EXAMPLE_RECIPIENTS_BY_BUYER = draw_names(EXAMPLE_NAMES, EXAMPLE_RECIPIENTS_PER_BUYER)

print("Example drawn names: {}\n".format(EXAMPLE_RECIPIENTS_BY_BUYER))
print("Is this a valid assignment? {}".format(is_valid_drawn_names(
    EXAMPLE_RECIPIENTS_BY_BUYER, EXAMPLE_RECIPIENTS_PER_BUYER)))

# %% [markdown] id="SHoNnMZzmrjQ" colab_type="text"
# ## Main Program
#
# Steps:
#
# 1. Fill in EMAILS_BY_NAME and NICKNAMES_BY_NAME
#
# 2. Fill in RECIPIENTS_PER_BUYER
#
# Run both cells

# %% id="uELDFFEcqjXS" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 69} outputId="624ab317-37b8-4c40-dc05-f237d2b4787e"
# Setup emails and names
EMAILS_BY_NAME = {"Tyler": "tylergwlum@gmail.com", 'ExampleName': "example@email.com"}
NICKNAMES_BY_NAME = {"Tyler": "Tygertron", 'ExampleName': 'Cookiedude'}
NAMES = list(EMAILS_BY_NAME.keys())
RECIPIENTS_PER_BUYER = 1

# Get assignment
recipients_by_buyer = draw_names(NAMES, RECIPIENTS_PER_BUYER)
print("Names have been drawn!\n")
print("Is this a valid assignment? {}".format(is_valid_drawn_names(recipients_by_buyer, RECIPIENTS_PER_BUYER)))

# %% id="Jj_Nx8RVk1I9" colab_type="code" colab={}
# Send emails
for buyer in recipients_by_buyer:
    recipients = recipients_by_buyer[buyer]

    # Get nicknames
    buyer_nickname = NICKNAMES_BY_NAME[buyer]
    recipient_nicknames = [NICKNAMES_BY_NAME[recipient] for recipient in recipients]

    # Write email body
    email_body = "Hi {0}! You will be buying a lovely present for: {1}. :)".format(
        buyer_nickname, str_with_ands_between(recipient_nicknames))

    # From statement
    email_body = email_body + "\n\n-Tyler Bot"

    # Nickname explanation
    email_body = email_body + "\n\nNICKNAMES:\n{0}".format(show_dict(NICKNAMES_BY_NAME))

    # Add tree
    email_body = email_body + "\n\n" + make_tree(11, 3)

    # Subject
    subject = "Sibling Secret Santa Draw {}".format(datetime.datetime.now().year)

    print(email_body)
    send_email([EMAILS_BY_NAME[buyer]], subject, email_body)

# Send email of actual draw to hidden email
send_email(["learningpython640@gmail.com"],
           "Sibling Secret Santa Real List {0}", "{1}".format(datetime.datetime.now().year, recipients_by_buyer))
