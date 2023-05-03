from typing import List, Union

from pydantic import BaseModel


class loginResponse(BaseModel):
    success: bool = False

    class Data(BaseModel):
        username: str
        phone: str
        roles: str
        accessToken: str
        refreshToken: str
        expires: str

    data: Union[Data, None] = None
