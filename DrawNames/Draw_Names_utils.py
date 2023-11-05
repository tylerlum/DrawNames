import random
from typing import List, Dict, Optional


def try_draw_names_one_recipient_per_buyer(full_name_list: List[str]) -> Dict[str, str]:
    """Try to assign each buyer one recipient

    Returns empty dict if unsuccessful
    """
    recipient_list = list(full_name_list)
    assignment_dict = {}

    for buyer in full_name_list:
        # If no available recipients, then failed
        available_recipients = [name for name in recipient_list if name != buyer]
        if len(available_recipients) == 0:
            return {}

        # Get random available recipient
        recipient = random.choice(available_recipients)

        # Remove recipient from recipient list
        recipient_list.remove(recipient)

        # Add buyer -> recipient pair
        assignment_dict[buyer] = recipient
    return assignment_dict


def draw_names_one_recipient_per_buyer(full_name_list: List[str]) -> Dict[str, str]:
    """Assign each buyer one recipient"""
    MAX_NUM_TRIES = 1000
    for _ in range(MAX_NUM_TRIES):
        assignment_dict = try_draw_names_one_recipient_per_buyer(full_name_list)
        if len(assignment_dict) != 0:
            return assignment_dict
    raise ValueError(f"Unable to draw names after {MAX_NUM_TRIES} tries")


# %% id="3W7Qe3qek1IO" colab_type="code" colab={}
def add_one_new_recipient_per_buyer(
    buyer_to_recipients_dict: Dict[str, List[str]], full_name_list: List[str]
) -> None:
    """Create a new buyer_to_recipient_dict, with no repeats.

    No repeats means that a buyer won't buy for the same person more than once
    """
    MAX_NUM_TRIES = 1000
    for _ in range(MAX_NUM_TRIES):
        # Create new dict
        new_buyer_to_recipient_dict = draw_names_one_recipient_per_buyer(full_name_list)

        # Check if it worked
        if all(
            new_recipient not in buyer_to_recipients_dict[buyer]
            for (buyer, new_recipient) in new_buyer_to_recipient_dict.items()
        ):
            # Worked, add to list
            for buyer, new_recipient in new_buyer_to_recipient_dict.items():
                buyer_to_recipients_dict[buyer].append(new_recipient)
            return

    raise ValueError(
        f"Unable to add one new recipient per buyer after {MAX_NUM_TRIES} tries"
    )


def draw_names(
    full_name_list: List[str], n_recipients_per_buyer: int, seed: Optional[int] = None,
) -> Dict[str, List[str]]:
    """Assign each buyer n distinct recipients (n = n_recipients_per_buyer)

    Done such that each person gets n gifts.

    Requires n > 0
    """
    random.seed(seed)

    # Check valid input
    if not 0 < n_recipients_per_buyer < len(full_name_list):
        raise ValueError(f"Invalid n_recipients_per_buyer = {n_recipients_per_buyer}")

    # Continuously draw names, getting one more recipient per buyer each loop
    buyer_to_recipients_dict = {name: [] for name in full_name_list}
    for _ in range(n_recipients_per_buyer):
        add_one_new_recipient_per_buyer(buyer_to_recipients_dict, full_name_list)

    return buyer_to_recipients_dict
