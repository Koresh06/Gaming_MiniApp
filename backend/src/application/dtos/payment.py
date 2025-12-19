from dataclasses import dataclass


@dataclass
class InitPaymentDTO:
    invoice_link: str
