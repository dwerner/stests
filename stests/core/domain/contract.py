import dataclasses
import typing

from stests.core.domain.enums import ContractType



@dataclasses.dataclass
class Contract:
    """A contract associated with an account.
    
    """
    # Numerical index to distinguish between multiple accounts.
    account_index: int

    # Hash of contract - relevant when deploying using --session-hash.
    hash: typing.Optional[str]

    # Name of contract - relevant when deploying using --session-name.
    name: typing.Optional[str]

    # Associated network.
    network: str
    
    # Numerical index to distinguish between multiple runs of the same generator.
    run_index: typing.Optional[int]

    # Type of generator, e.g. WG-100 ...etc.
    run_type: typing.Optional[str]

    # Type of client contract.
    typeof: ContractType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    @property
    def hash_as_bytes(self):
        return bytes.fromhex(self.hash)    

    @property
    def label_account_index(self):
        return f"A-{str(self.account_index).zfill(6)}"

    @property
    def label_run_index(self):
        return f"R-{str(self.run_index).zfill(3)}"