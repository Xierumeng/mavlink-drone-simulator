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

    @staticmethod
    def create_from_config(
        base_url: str, name_pairs: list[tuple[str, str]]
    ) -> "tuple[bool, BaseUrlAndFilenames | None]":
        """
        base_url: URL to download from. Suffix doesn't matter.
        name_pairs: List of files to download in the form [remote_name, local_name] .
        """
        names = []
        for name_pair in name_pairs:
            if len(name_pair) != 2:
                print(f"ERROR: Expected pair: {name_pair}")
                return False, None

            remote_name, local_name = name_pair
            result, download_name_map = DownloadNameMap.create(remote_name, local_name)
            if not result:
                print(f"ERROR: Failed to create DownloadNameMap with: {name_pair}")
                return False, None

            # Get Pylance to stop complaining
            assert download_name_map is not None

            names.append(download_name_map)

        return BaseUrlAndFilenames.create(base_url, names)

    @classmethod
    def create(
        cls, base_url: str, names: list[DownloadNameMap]
    ) -> "tuple[bool, BaseUrlAndFilenames | None]":
        """
        base_url: URL to download from. Adds suffix / if not there already.
        names: List of files to download.
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
