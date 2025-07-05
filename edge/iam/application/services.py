import secrets
import random

from iam.infrastructure.models import Device


def generate_mac_like_code() -> str:
    return ":".join(["{:02X}".format(random.randint(0, 255)) for _ in range(6)])


class AuthApplicationService:
    def register_rfid(self):

        rfid_code = generate_mac_like_code()

        while Device.select().where(Device.rfid_code == rfid_code).exists():
            rfid_code = generate_mac_like_code()

        # Genera api_key única
        api_key = secrets.token_hex(16)

        device = Device.create(
            rfid_code=rfid_code,
            api_key=api_key
        )
        return device

    def get_device_by_code_and_key(self, rfid_code: str, api_key: str):
        return Device.get_or_none(Device.rfid_code == rfid_code, Device.api_key == api_key)

