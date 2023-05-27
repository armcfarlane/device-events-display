import netaddr
import pydantic

VALID_MAC_ADDRESS_DIALECTS: list[str] = [
    str(x) for x in netaddr.__dict__.keys() if x.startswith("mac_")
]
VALID_MAC_ADDRESS_FORMAT_CASES: list[str] = ["upper", "lower"]


class MacAddress(str):
    """
    Mac address class with validation.
    """

    @classmethod
    def __get_validators__(cls):
        """
        One or more validators will be yielded...called in order to validate the inpuyt.
        Each validator will receive as an input the value returned from the previous
        validator.
        """
        yield cls.validate_mac_address

    @classmethod
    def validate_mac_address(cls, mac_address: str) -> str:
        if netaddr.valid_mac(mac_address):
            return mac_address
        else:
            raise ValueError(f'The value "{mac_address}" is not a valid mac address')

    def __init__(self, mac_address) -> None:
        if not netaddr.valid_mac(mac_address):
            raise ValueError(f'The value "{mac_address}" is not a valid mac address')
        self.eui = netaddr.EUI(mac_address)

    def __repr__(self):
        return f"MacAddress({super().__repr__()})"

    def valid_cases() -> list[str]:
        return ["upper", "lower"]

    def format(self, dialect="mac_unix_expanded", case="lower") -> str:
        if dialect.lower() not in VALID_MAC_ADDRESS_DIALECTS:
            raise ValueError(
                f'The dialect "{dialect}" is not valid.  Valid dialects: {", ".join(VALID_MAC_ADDRESS_DIALECTS)}'
            )

        if case.lower() not in VALID_MAC_ADDRESS_FORMAT_CASES:
            raise ValueError(
                f'The case "{case}" is not valid.  Valid cases: {", ".join(VALID_MAC_ADDRESS_FORMAT_CASES)}'
            )

        self.eui.dialect = getattr(netaddr, dialect)

        return getattr(str(self.eui), case)()
