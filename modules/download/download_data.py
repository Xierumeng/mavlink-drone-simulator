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


class BaseUrlAndFilenames:
    """
    Information to download files from base URL.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, base_url: str, names: list[DownloadNameMap]
    ) -> "tuple[bool, BaseUrlAndFilenames | None]":
        """
        base_url: URL to download from. Adds suffix / if not there already.
        files: List of files to download.
        """
        if base_url == "":
            return False, None

        if len(names) == 0:
            return False, None

        base_url_suffix_slash = base_url if base_url.endswith("/") else (base_url + "/")

        return True, BaseUrlAndFilenames(cls.__create_key, base_url_suffix_slash, names)

    def __init__(
        self, class_private_create_key: object, base_url: str, names: list[DownloadNameMap]
    ) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is BaseUrlAndFilenames.__create_key, "Use create() method"

        self.base_url = base_url
        self.names = names
