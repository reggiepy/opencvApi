# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/7/16 18:19

import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field
import sqlmodel


def convert_datetime(dt: datetime.datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')


class BaseDateTime(SQLModel):
    create_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    update_time: datetime.datetime = Field(
        sa_column=sqlmodel.Column(sqlmodel.DATETIME(), onupdate=sqlmodel.func.now()),
        default_factory=datetime.datetime.now,
    )

    class Config:
        json_encoders = {
            datetime.datetime: convert_datetime
        }


class DataTableRequest(BaseModel):
    sEcho: int = Field(...)
    iDisplayStart: int = Field(..., gt=0)
    iDisplayLength: int = Field(..., gt=0)


class DataTableResponse(BaseModel):
    sEcho: int = Field(...)
    iTotalRecords: int = Field(...)
    iTotalDisplayRecords: int = Field(...)
    aaData: dict = Field(...)
