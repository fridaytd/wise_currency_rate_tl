import os
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Self
from gspread.worksheet import Worksheet
from gspread.auth import service_account

from app.shared.exceptions import SheetError
from app.shared.consts import COL_META_FIELD_NAME
from app.utils.paths import ROOT_PATH


class ColSheetModel(BaseModel):
    # Model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

    worksheet: Worksheet = Field(exclude=True)
    index: int

    @classmethod
    def mapping_fields(cls) -> dict:
        mapping_fields = {}
        for field_name, field_info in cls.model_fields.items():
            if hasattr(field_info, "metadata"):
                for metadata in field_info.metadata:
                    if COL_META_FIELD_NAME in metadata:
                        mapping_fields[field_name] = metadata[COL_META_FIELD_NAME]
                        break

        return mapping_fields

    @classmethod
    def get(
        cls,
        worksheet: Worksheet,
        index: int,
    ) -> Self:
        mapping_dict = cls.mapping_fields()

        query_value = []

        for _, v in mapping_dict.items():
            query_value.append(f"{v}{index}")

        model_dict = {
            "index": index,
            "worksheet": worksheet,
        }

        query_results = worksheet.batch_get(query_value)
        count = 0
        for k, _ in mapping_dict.items():
            model_dict[k] = query_results[count].first()
            if isinstance(model_dict[k], str):
                model_dict[k] = model_dict[k].strip()
            count += 1
        return cls.model_validate(model_dict)

    @classmethod
    def batch_get(
        cls,
        worksheet: Worksheet,
        indexes: list[int],
    ) -> list[Self]:
        mapping_dict = cls.mapping_fields()

        result_list: list[Self] = []

        query_value = []
        for index in indexes:
            for _, v in mapping_dict.items():
                query_value.append(f"{v}{index}")

        query_results = worksheet.batch_get(query_value)

        count = 0

        for index in indexes:
            model_dict = {
                "index": index,
                "worksheet": worksheet,
            }

            for k, _ in mapping_dict.items():
                model_dict[k] = query_results[count].first()
                if isinstance(model_dict[k], str):
                    model_dict[k] = model_dict[k].strip()
                count += 1

            result_list.append(cls.model_validate(model_dict))
        return result_list

    @classmethod
    def batch_update(
        cls,
        list_object: list[Self],
    ) -> None:
        mapping_dict = cls.mapping_fields()
        update_batch = []

        for object in list_object:
            model_dict = object.model_dump(mode="json")

            for k, v in mapping_dict.items():
                update_batch.append(
                    {
                        "range": f"{v}{object.index}",
                        "values": [[model_dict[k]]],
                    }
                )

        if len(list_object) > 0:
            list_object[0].worksheet.batch_update(update_batch)

    def update(
        self,
    ) -> None:
        mapping_dict = self.mapping_fields()
        model_dict = self.model_dump(mode="json")

        update_batch = []
        for k, v in mapping_dict.items():
            update_batch.append(
                {
                    "range": f"{v}{self.index}",
                    "values": [[model_dict[k]]],
                }
            )

        self.worksheet.batch_update(update_batch)


class GCurrencyRate(ColSheetModel):
    # highlight: Annotated[str, {COL_META_FIELD_NAME: "A"}]
    UPDATE_AT: Annotated[str | None, {COL_META_FIELD_NAME: "B"}] = None
    SOURCE: Annotated[str | None, {COL_META_FIELD_NAME: "C"}] = None
    TARGET: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    RATE: Annotated[float | None, {COL_META_FIELD_NAME: "E"}] = None
