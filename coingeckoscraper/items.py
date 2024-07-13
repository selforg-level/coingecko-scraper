from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True, eq=True, repr=True)
class GeckoCoin:
    rating: Optional[int | str] = field(default="-")
    name: Optional[str] = field(default=None)
    price: Optional[str] = field(default=None)
    daily_volume: Optional[str] = field(default=None)
    market_capital: Optional[str] = field(default=None)
    portfolio_updates: Optional[str] = field(default=None)
    hour_change: Optional[str] = field(default=None)
    day_change: Optional[str] = field(default=None)
    week_change: Optional[str] = field(default=None)
    two_weeks_change: Optional[str] = field(default=None)
    month_change: Optional[str] = field(default=None)
    year_change: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
