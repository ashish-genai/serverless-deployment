from datetime import datetime
import babel.numbers

def format_datetime(value: datetime, format: str = "medium") -> str:
    """Format a datetime object for display"""
    if not value:
        return ""
    return babel.dates.format_datetime(value, format)

def format_currency(value: float) -> str:
    """Format a number as currency"""
    if value is None:
        return "$0.00"
    return babel.numbers.format_currency(value, "USD")