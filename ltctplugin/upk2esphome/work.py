#  Copyright (c) Kuba Szczodrzyński 2023-5-13.

from logging import debug, warning
from os import stat
from os.path import isfile
from pprint import pprint
from socket import gethostbyname
from time import sleep
from typing import Callable
from urllib.parse import urlparse

import requests
from bk7231tools.analysis.kvstorage import KVStorage
from ltchiptool.gui.work.base import BaseThread
from ltchiptool.util.flash import ClickProgressCallback


class UpkThread(BaseThread):
    def __init__(
        self,
        file: str = None,
        url: str = None,
        on_storage: Callable[[dict], None] = None,
    ):
        super().__init__()
        self.file = file
        self.url = url
        self.on_storage = on_storage

    def run_impl(self):
        if self.file is not None:
            self.run_file(self.file)
        if self.url is not None:
            self.run_url(self.url)

    # noinspection HttpUrlsUsage
    def run_url(self, url: str):
        # grab storage data from Kickstart API
        if not url.startswith("http"):
            url = "http://" + url
        url = urlparse(url)
        url = url.netloc
        if not url:
            raise ValueError(f"Invalid URL: {url}")

        offset = 0x1E0000
        start = 0x1E0000 - offset
        end = 0x200000 - offset
        init_size = 1024
        block_size = 2048
        buffer = bytearray(end - start)

        with ClickProgressCallback(length=end - start) as bar:
            bar.on_message(f"Resolving {url}...")
            try:
                ip = gethostbyname(url)
            except Exception:
                raise ConnectionError(f"Couldn't find hostname: {url}")

            url = f"http://{ip}/hub/flash_read"
            params = dict(offset=0, length=init_size)

            bar.on_message(f"Connecting to {ip}...")
            with requests.get(url, params, timeout=5.0) as r:
                data = r.content
                if len(data) != init_size:
                    raise RuntimeError(
                        f"Incomplete response read: {len(data)}/{init_size}\n\n"
                        f"Is the chip running Kickstart firmware?"
                    )

            while start < end and self.should_run():
                bar.on_message(f"Reading from 0x{offset + start:06X}")
                read_size = min(block_size, end - start)
                params["offset"] = offset + start
                params["length"] = read_size
                sleep(0.05)
                with requests.get(url, params, timeout=5.0) as r:
                    data = r.content
                    if len(data) != read_size:
                        warning(f"Incomplete response read: {len(data)}/{read_size}")
                        sleep(0.2)
                        continue
                    bar.on_update(read_size)
                    buffer[start : start + read_size] = data
                    start += read_size

        if not self.should_run():
            return

        self.run_data(buffer)

    def run_file(self, file: str):
        # read storage from file
        if not isfile(file):
            raise FileNotFoundError(f"File '{file}' not found")
        size = stat(file).st_size
        if size > 0x400000:
            # file too large
            raise RuntimeError(f"File larger than 4 MiB ({size}), refusing to load!")
        if size == 0x200000:
            # probably full flash dump
            with open(file, "rb") as f:
                # seek to approx. storage start (plus a fix for BkWriter etc.)
                f.seek(0x1E0000 - 0x11000)
                data = f.read()
            self.run_data(data)
            return
        # try to search the entire file
        with open(file, "rb") as f:
            data = f.read()
        self.run_data(data)

    def run_data(self, data: bytes):
        # parse raw storage
        result = KVStorage.find_storage(data)
        if not result:
            raise ValueError("File doesn't contain known storage area")

        _, data = result
        try:
            kvs = KVStorage.decrypt_and_unpack(data)
        except Exception:
            raise RuntimeError("Couldn't unpack storage data - see program logs")

        keys = list(kvs.indexes.keys())
        debug(f"Found {len(keys)} keys! {keys}")
        if not keys:
            # noinspection PyBroadException
            try:
                pprint(kvs)
            except Exception:
                pass
            raise RuntimeError("No keys found in storage! Is the data corrupt?")

        try:
            storage = kvs.read_all_values_parsed()
        except Exception:
            # noinspection PyBroadException
            try:
                pprint(kvs)
            except Exception:
                pass
            raise RuntimeError("Couldn't parse storage data - see program logs")

        self.on_storage(storage)

    def stop(self):
        super().stop()
