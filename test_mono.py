from time import sleep
from tabulate import tabulate
import logging
from datetime import date
from monobank import Client, TooManyRequests
from typing import List, Callable, Any
from _types import make_account, Account, make_statement, Statement
from dateutils import datetime_range_steps, get_quarters_for_year


logging.basicConfig(filename="info.log", level=logging.INFO)


def send_request(request: Callable) -> Any:
    while True:
        try:
            return request()
        except TooManyRequests:
            sleep(1)
        else:
            break


def get_statements(
    client: Client, account_id: str, from_date: date, to_date: date
) -> List[Statement]:
    statements: List[Statement] = []
    for left, right in datetime_range_steps(from_date, to_date, 29):
        stmts = send_request(lambda: client.get_statements(account_id, left, right))
        statements += [make_statement(**st) for st in stmts]
        logging.info(f"Done for {left} - {right}")

    return sorted(statements, key=lambda s: s.time)


def print_statements(statements: List[Statement], currency: str) -> None:
    stmts = [
        (
            f"{st.amount:.2f}",
            st.time.strftime("%Y-%m-%d %H:%M:%S"),
            currency,
            st.description,
        )
        for st in statements
        if st.amount > 0
    ]
    print(tabulate(stmts, headers=["Amount", "Time", "Currency", "Description"]))


def get_token() -> str:
    with open("token") as f:
        return f.read().strip("\n")


mono = Client(get_token())
accounts: List[Account] = [
    make_account(**a) for a in send_request(mono.get_client_info)["accounts"]
]
fops = [a for a in accounts if a.type == "fop"]

quarters = get_quarters_for_year(2021)

for fop in fops:
    print(f"Enterpreneur account for {fop.currency.name}")

    year_sum = 0
    for num, quarter in enumerate(quarters):
        stmts = get_statements(mono, fop.id, *quarter)
        print(f"Q{num + 1}: \n")
        print_statements(stmts, fop.currency.alpha_3)
        quarter_sum = sum(st.amount for st in stmts if st.amount > 0)
        year_sum += quarter_sum
        print(f"\nSum: {quarter_sum:.2f}")
        print(f"Accumulated sum: {year_sum:.2f}", end="\n\n")
