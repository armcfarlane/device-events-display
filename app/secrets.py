from typing import Any

import boto3

VALID_SECRET_FLAVORS: list[str] = ["secretsmanager"]


class Secret:
    def __init__(
        self, flavor: str = "secretsmanager", secret_client: Any = None
    ) -> None:
        if flavor not in VALID_SECRET_FLAVORS:
            raise ValueError(
                f'Dealing with "{flavor}" secrets has not yet been implemented.  Valid "flavor" values: {", ".join(VALID_SECRET_FLAVORS)}'
            )

        if secret_client:
            self.secret_client = secret_client
            if flavor == "secretsmanager":
                self.secret_client = boto3.client(flavor)
        else:
            self.secret_client = secret_client
