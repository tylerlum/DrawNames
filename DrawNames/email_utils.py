import smtplib
from typing import List
from dataclasses import dataclass


@dataclass
class EmailSender:
    """Class for sending emails."""

    user: str
    password: str

    def send_email(self, to: List[str], subject: str, body: str) -> None:
        email_text = "\n".join(
            [f"From: {self.user}", f"To: {to}", f"Subject: {subject}", "", body]
        )

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(self.user, self.password)
            server.sendmail(self.user, to, email_text)
            server.close()

            print("Email sent\n")
        except Exception as e:
            print("Something went wrong")
            print(e)

    def passwordcheck(self):
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(self.user, self.password)
        server.quit()
        print("Thank you. Password was correct.")

    def __post_init__(self):
        self.passwordcheck()
