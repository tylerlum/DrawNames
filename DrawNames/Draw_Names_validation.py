from typing import List, Dict


def is_valid_drawn_names(
    buyer_to_recipients_dict: Dict[str, List[str]], n_recipients_per_buyer: int
) -> bool:
    return (
        buyer_has_unique_recipients(buyer_to_recipients_dict)
        and each_person_gets_equal_number_of_gifts(
            buyer_to_recipients_dict, n_recipients_per_buyer
        )
        and each_buyer_buys_correct_number_of_gifts(
            buyer_to_recipients_dict, n_recipients_per_buyer
        )
        and no_buyer_buys_for_themselves(buyer_to_recipients_dict)
    )


def buyer_has_unique_recipients(buyer_to_recipients_dict: Dict[str, List[str]]) -> bool:
    for recipients in buyer_to_recipients_dict.values():
        if any(recipients.count(recipient) > 1 for recipient in recipients):
            return False
    return True


def each_person_gets_equal_number_of_gifts(
    buyer_to_recipients_dict: Dict[str, List[str]], n_recipients_per_buyer: int
) -> bool:
    names = buyer_to_recipients_dict.keys()
    for name in names:
        num_gifts = 0
        for recipients in buyer_to_recipients_dict.values():
            if name in recipients:
                num_gifts += 1
        if not num_gifts == n_recipients_per_buyer:
            return False
    return True


def each_buyer_buys_correct_number_of_gifts(
    buyer_to_recipients_dict: Dict[str, List[str]], n_recipients_per_buyer: int
) -> bool:
    for recipients in buyer_to_recipients_dict.values():
        if not len(recipients) == n_recipients_per_buyer:
            return False
    return True


def no_buyer_buys_for_themselves(
    buyer_to_recipients_dict: Dict[str, List[str]]
) -> bool:
    for buyer in buyer_to_recipients_dict:
        if buyer in buyer_to_recipients_dict[buyer]:
            return False
    return True
