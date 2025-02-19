from httpx import Client

from .. import config
from ..models.api_models import CurrencyRate


class WiseAPI:
    def __init__(self) -> None:
        self.http_client = Client(
            base_url="https://api.wise.com",
            headers={"Authorization": f"Bearer {config.WISE_API_KEY}"},
        )

    def rate(
        self,
    ) -> list[CurrencyRate]:
        res = self.http_client.get("/v1/rates")

        res.raise_for_status()

        result: list[CurrencyRate] = []
        for r in res.json():
            result.append(CurrencyRate.model_validate(r))

        return result
