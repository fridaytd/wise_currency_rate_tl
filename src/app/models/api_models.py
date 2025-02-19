from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel


class CurrencyRate(BaseModel):
    rate: float
    source: str
    target: str
    time: str

    def to_formated_time(
        self,
    ) -> str:
        time = datetime.fromisoformat(self.time)
        vn_timezone_time = time.astimezone(ZoneInfo("Etc/GMT+7"))
        formatted_date = vn_timezone_time.strftime("%d/%m/%Y %H:%M:%S")
        return formatted_date
