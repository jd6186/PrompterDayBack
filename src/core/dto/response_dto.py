from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from ..error.error_type_code import EXCEPTION_TYPE
from ...core.util import core_util


class ResponseDTO(BaseModel):
    result_data: object = Field(
        default="Success", title="Response Data"
    )
    timestamp: str = Field(
        default=("{:%Y%m%d %H:%M:%S}".format(core_util.get_seoul_time())), title="Response Time", max_length=100
    )
    status_code: str = Field(
        default=EXCEPTION_TYPE.ERROR_200.value["code"], title="Response Status Code", max_length=4
    )
    status_message: str = Field(
        default=EXCEPTION_TYPE.ERROR_200.value["message"], title="Response Status Message", max_length=1000
    )

    def of(self, result_data):
        self.result_data = result_data
        self.timestamp = core_util.get_seoul_datetime_format()
        self.status_code = EXCEPTION_TYPE.ERROR_200.value["code"]
        self.status_message = EXCEPTION_TYPE.ERROR_200.value["message"]
        return JSONResponse(content=self.dict())