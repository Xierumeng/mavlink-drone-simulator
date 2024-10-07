"""
For renaming downloaded files.
"""


class DownloadNameMap:
    """
    Remote name to local name map.
    """

    __create_key = object()

    @classmethod
    def create(cls, remote_name: str, local_name: str) -> "tuple[bool, DownloadNameMap | None]":
        """
        remote_name: Filename on the server.
        local_name: Filename on the client.
        """
        if remote_name == "":
            return False, None

        if local_name == "":
            return False, None

        return True, DownloadNameMap(cls.__create_key, remote_name, local_name)

    def __init__(self, class_private_create_key: object, remote_name: str, local_name: str) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DownloadNameMap.__create_key, "Use create() method"

        self.remote_name = remote_name
        self.local_name = local_name
