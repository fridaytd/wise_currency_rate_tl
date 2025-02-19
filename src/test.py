# from app.processes.wise_api import WiseAPI
# from app.models.gsheet_model import GCurrencyRate
# from app.utils.gsheet import worksheet
# from app.utils.paths import APP_PATH

# import json

# api = WiseAPI()

# l_gcr: list[GCurrencyRate] = []

# list_rate = api.rate()
# print(len(list_rate))

# count = 0

# source_currency: list[str] = []

# for rate in list_rate:
#     if rate.source not in source_currency:
#         source_currency.append(rate.source)
#     # g_rate = GCurrencyRate(
#     #     worksheet=worksheet,
#     #     index=count + 4,
#     #     UPDATE_AT=rate.to_formated_time(),
#     #     SOURCE=rate.source,
#     #     TARGET=rate.target,
#     #     RATE=rate.rate,
#     # )
#     # l_gcr.append(g_rate)
#     # count += 1

# source_currency.sort()

# order: list[tuple[str, str]] = []

# for s in source_currency:
#     for t in source_currency:
#         for rate in list_rate:
#             if rate.source == s and rate.target == t:
#                 g_rate = GCurrencyRate(
#                     worksheet=worksheet,
#                     index=count + 4,
#                     UPDATE_AT=rate.to_formated_time(),
#                     SOURCE=rate.source,
#                     TARGET=rate.target,
#                     RATE=rate.rate,
#                 )
#                 l_gcr.append(g_rate)
#                 count += 1
#                 order.append((s, t))

# with open(APP_PATH / "data" / "order.json", "w") as f:
#     json.dump(order, f)
# GCurrencyRate.batch_update(l_gcr)

from zoneinfo import ZoneInfo, available_timezones

print(available_timezones())
