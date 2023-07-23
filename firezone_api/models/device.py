"""
Модель устройства
"""
from pydantic import BaseModel, validator

from firezone_api.models.string_datetime_view import StringDatetime


class Device(BaseModel):
    allowed_ips: list[str]
    description: str | None
    dns: list[str]
    endpoint: str
    id: str
    inserted_at: str
    ipv4: str
    ipv6: str
    latest_handshake: StringDatetime | None
    mtu: int
    name: str
    persistent_keepalive: int
    preshared_key: str
    public_key: str
    remote_ip: str | None
    rx_bytes: int | None
    server_public_key: str
    tx_bytes: int | None
    updated_at: StringDatetime | None
    use_default_allowed_ips: bool
    use_default_dns: bool
    use_default_endpoint: bool
    use_default_mtu: bool
    use_default_persistent_keepalive: bool
    user_id: str

    class Config:
        arbitrary_types_allowed = True

    @validator("updated_at",
               "latest_handshake",
               pre=True)
    def parse_date(value: str | None) -> StringDatetime | None:
        if value is None:
            return
        value = value.split('.')[0]
        return StringDatetime(value)
