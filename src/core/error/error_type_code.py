from enum import Enum


class EXCEPTION_TYPE(Enum):
    ERROR_200 = {"code": "200", "message": "OK"}
    ERROR_201 = {"code": "201", "message": "CREATED"}
    ERROR_202 = {"code": "202", "message": "ACCEPTED"}
    ERROR_204 = {"code": "204", "message": "NO_CONTENT"}
    ERROR_400 = {"code": "400", "message": "BAD_REQUEST"}
    ERROR_401 = {"code": "401", "message": "UNAUTHORIZED"}
    ERROR_402 = {"code": "402", "message": "TOKEN_HAS_EXPIRED"}
    ERROR_403 = {"code": "403", "message": "FORBIDDEN"}
    ERROR_404 = {"code": "404", "message": "NOT_FOUND"}
    ERROR_405 = {"code": "405", "message": "METHOD_NOT_ALLOWED"}
    ERROR_406 = {"code": "406", "message": "NOT_ACCEPTABLE"}
    ERROR_408 = {"code": "408", "message": "REQUEST_TIMEOUT"}
    ERROR_409 = {"code": "409", "message": "CONFLICT"}
    ERROR_410 = {"code": "410", "message": "GONE"}
    ERROR_411 = {"code": "411", "message": "LENGTH_REQUIRED"}
    ERROR_412 = {"code": "412", "message": "PRECONDITION_FAILED"}
    ERROR_413 = {"code": "413", "message": "REQUEST_ENTITY_TOO_LARGE"}
    ERROR_414 = {"code": "414", "message": "REQUEST_URI_TOO_LONG"}
    ERROR_415 = {"code": "415", "message": "UNSUPPORTED_MEDIA_TYPE"}
    ERROR_416 = {"code": "416", "message": "REQUESTED_RANGE_NOT_SATISFIABLE"}
    ERROR_417 = {"code": "417", "message": "EXPECTATION_FAILED"}
    ERROR_422 = {"code": "422", "message": "UNPROCESSABLE_ENTITY"}
    ERROR_423 = {"code": "423", "message": "LOCKED"}
    ERROR_424 = {"code": "424", "message": "FAILED_DEPENDENCY"}
    ERROR_428 = {"code": "428", "message": "PRECONDITION_REQUIRED"}
    ERROR_429 = {"code": "429", "message": "TOO_MANY_REQUESTS"}
    ERROR_431 = {"code": "431", "message": "REQUEST_HEADER_FIELDS_TOO_LARGE"}
    ERROR_451 = {"code": "451", "message": "UNAVAILABLE_FOR_LEGAL_REASONS"}
    ERROR_500 = {"code": "500", "message": "INTERNAL_SERVER_ERROR"}
    ERROR_501 = {"code": "501", "message": "NOT_IMPLEMENTED"}
    ERROR_502 = {"code": "502", "message": "BAD_GATEWAY"}
    ERROR_503 = {"code": "503", "message": "SERVICE_UNAVAILABLE"}
    ERROR_504 = {"code": "504", "message": "GATEWAY_TIMEOUT"}
    ERROR_505 = {"code": "505", "message": "DATA_NOT_FOUND"}

    @classmethod
    def find_by_code(cls, code):
        for enum_type in cls:
            if enum_type.name.split("_")[1] == str(code):
                return enum_type
        return cls.ERROR_500

