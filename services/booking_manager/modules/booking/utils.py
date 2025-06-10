from datetime import datetime

def format_brl(value: float) -> str:
    val_str = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {val_str}"

def format_date_ptbr(date: datetime) -> str:
    mouths = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    return f"{date.day} de {mouths[date.month - 1]} de {date.year}"