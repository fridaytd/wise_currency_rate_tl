import time
from app import config
from app.utils.gsheet import worksheet
from app.processes.wise_api import WiseAPI
from app.models.gsheet_model import GCurrencyRate
from app.models.api_models import CurrencyRate
from app.utils.logger import logger
from app.utils.json_io import read_json
from app.utils.paths import APP_PATH

wise_api = WiseAPI()

logger.info("Get currency order")
currency_order = read_json(APP_PATH / "data" / "order.json")


def convert_rate_dict(rates: list[CurrencyRate]) -> dict[str, dict[str, CurrencyRate]]:
    rate_dict: dict[str, dict[str, CurrencyRate]] = {}
    for rate in rates:
        if rate.source not in rate_dict:
            rate_dict[rate.source] = {}

        rate_dict[rate.source][rate.target] = rate

    return rate_dict


def main():
    logger.info("Fetch API rate")
    api_rate_result = wise_api.rate()

    logger.info("Convert to rate dict")
    rate_dict = convert_rate_dict(api_rate_result)

    g_currency_rates: list[GCurrencyRate] = []

    index = config.START_INDEX
    for c_o in currency_order:
        rate = rate_dict[c_o[0]][c_o[1]]
        g_currency_rate = GCurrencyRate(
            worksheet=worksheet,
            index=index,
            UPDATE_AT=rate.to_formated_time(),
            SOURCE=rate.source,
            TARGET=rate.target,
            RATE=rate.rate,
        )
        g_currency_rates.append(g_currency_rate)
        index += 1

    logger.info("Update rate to sheet")
    GCurrencyRate.batch_update(g_currency_rates)

    logger.info(f"Sleep for {config.RELAX_TIME_EACH_ROUND}")
    time.sleep(float(config.RELAX_TIME_EACH_ROUND))


while True:
    main()
