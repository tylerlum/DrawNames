from DrawNames import (
    draw_names,
    is_valid_drawn_names,
    EmailSender,
    make_tree,
    show_dict,
    str_with_ands_between,
)

import datetime
from tap import Tap
from typing import Dict, Optional
from getpass import getpass


class ArgumentParser(Tap):
    name_to_email_dict: Dict[str, str] = {
        "Tyler": "tylergwlum@gmail.com",
        "OtherTyler": "pythoncoderdude@gmail.com",
    }
    name_to_nickname_dict: Dict[str, str] = {
        "Tyler": "Tygertron",
        "OtherTyler": "SwoleDude",
    }
    n_recipients_per_buyer: int = 1
    email_subject_line: str = (
        f"Sibling Secret Santa Draw {datetime.datetime.now().year}"
    )
    email_used_to_send: Optional[str] = "pythoncoderdude@gmail.com"


def run_example_usage() -> None:
    EXAMPLE_NAMES = ["Ben", "Aaron", "Joel", "Angela", "Zoe", "Ken"]
    EXAMPLE_RECIPIENTS_PER_BUYER = 3

    EXAMPLE_BUYER_TO_RECIPIENTS_DICT = draw_names(
        EXAMPLE_NAMES, EXAMPLE_RECIPIENTS_PER_BUYER
    )

    print(f"Example drawn names: {EXAMPLE_BUYER_TO_RECIPIENTS_DICT}\n")
    print(
        f"Is this a valid assignment? {is_valid_drawn_names(EXAMPLE_BUYER_TO_RECIPIENTS_DICT, EXAMPLE_RECIPIENTS_PER_BUYER)}"
    )


def main() -> None:
    args = ArgumentParser().parse_args()
    print("=" * 80)
    print(f"args = {args}")
    print("=" * 80 + "\n")

    # Setup email
    email_used_to_send = args.email_used_to_send
    if email_used_to_send is None:
        email_used_to_send = input(
            "Enter the email address you will use to send gift assignments: "
        )

    # Get app password
    print("-" * 80)
    print(
        f"Reminder: to send emails, {email_used_to_send} must have app password set up."
    )
    print(
        "If not set up, refer to https://support.google.com/mail/answer/185833?hl=en-GB or search for 'Sign in using app passwords'"
    )
    print("-" * 80 + "\n")
    app_password = getpass(prompt=f"Enter the app password for {email_used_to_send}: ")
    email_sender = EmailSender(user=email_used_to_send, password=app_password)

    # Get assignment
    names = list(args.name_to_email_dict.keys())
    buyer_to_recipients_dict = draw_names(names, args.n_recipients_per_buyer)
    print("Names have been drawn!\n")
    print(
        f"Is this a valid assignment? {is_valid_drawn_names(buyer_to_recipients_dict, args.n_recipients_per_buyer)}"
    )

    # Send emails
    for buyer, recipients in buyer_to_recipients_dict.items():
        # Get nicknames
        buyer_nickname = args.name_to_nickname_dict[buyer]
        recipient_nicknames = [
            args.name_to_nickname_dict[recipient] for recipient in recipients
        ]

        # Write email body
        email_body = f"Hi {buyer_nickname}! You will be buying a lovely present for: {str_with_ands_between(recipient_nicknames)}. :)"

        # From statement
        email_body += "\n\n-Tyler Bot"

        # Nickname explanation
        email_body += f"\n\nNICKNAMES:\n{show_dict(args.name_to_nickname_dict)}"

        # Add tree
        email_body += "\n\n" + make_tree(11, 3)

        print(email_body)
        email_sender.send_email(
            to=[args.name_to_email_dict[buyer]],
            subject=args.email_subject_line,
            body=email_body,
        )

    # Send email of actual draw to email used to send
    email_sender.send_email(
        to=[email_used_to_send],
        subject=f"{args.email_subject_line} (Real List)",
        body=f"{buyer_to_recipients_dict}",
    )


if __name__ == "__main__":
    main()
