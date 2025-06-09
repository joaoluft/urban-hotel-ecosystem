import re
from dataclasses import dataclass

@dataclass
class CPFValidator:
    def is_valid(self, cpf: str) -> bool:
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calculate_digit(cpf_part: str, factor: int) -> int:
            total = sum(int(digit) * (factor - idx) for idx, digit in enumerate(cpf_part))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        digit1 = calculate_digit(cpf[:9], 10)
        digit2 = calculate_digit(cpf[:9] + str(digit1), 11)

        return cpf.endswith(f"{digit1}{digit2}")
    
def get_cpf_validator() -> CPFValidator:
    return CPFValidator()