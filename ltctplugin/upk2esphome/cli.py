#  Copyright (c) Kuba Szczodrzyński 2023-8-28.

import json
from logging import error, info, warning

import click
import inquirer

from ltctplugin.upk2esphome.common import (
    cloudcutter_get_device,
    cloudcutter_list_devices,
)
from ltctplugin.upk2esphome.work import UpkThread
from upk2esphome import Opts, upk2esphome


def add_options():
    options = [
        click.option(
            "-o",
            "--output",
            type=click.File("w"),
            help="Output .yaml file (default: stdout)",
        ),
    ]

    default_opts = Opts()
    for key, value in Opts.FLAGS.items():
        short = key[0]
        long = key.replace("_", "-")
        default = getattr(default_opts, key)
        options.append(
            click.option(
                f"-{short}/-{short.upper()}",
                f"--{long}/--no-{long}",
                help=f"{value} (default: {default})",
                default=default,
            )
        )
    for key, value in Opts.INPUTS.items():
        short = key[0]
        long = key.replace("_", "-")
        if long.startswith("wifi"):
            # use s/p for ssid and password
            short = key[5]
        default = getattr(default_opts, key)
        options.append(
            click.option(
                f"-{short.upper()}",
                f"--{long}",
                help=f"{value} (default: '{default}')",
                default=default,
            )
        )

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
def cli():
    """
    ${DESCRIPTION}

    \b
    Three modes of operation are available:
    - kickstart - Grab from ESPHome Kickstart
        (If you have flashed Kickstart to a device)
    - cloudcutter - Build from Cloudcutter device profile
        (If your device has a matching manufacturer/model profile)
    - firmware - Analyze firmware dump
        (If you read a firmware .BIN with ltchiptool or bk7231tools)

    Run the command of choice to learn more.
    """


@cli.command()
@click.argument("URL", type=str, required=False)
@add_options()
@click.option("--storage-only", help="Dump storage data only (no YAML)", is_flag=True)
def kickstart(url: str, output: click.File, **kwargs):
    """
    Grab from ESPHome Kickstart

    Use this to read UPK from a device running ESPHome-Kickstart.

    The device must be connected to the same Wi-Fi network.
    """

    if not url:
        print("Enter URL (or IP address) of Kickstart dashboard:")
        question = inquirer.Text(
            "url",
            message="Kickstart URL",
        )
        answer = inquirer.prompt([question])
        if not answer:
            return
        url = answer["url"]

    work = UpkThread(
        url=url,
        on_storage=lambda data: write_upk(data, output, **kwargs),
        on_error=error,
    )
    work.start()


@cli.command()
@click.argument("PROFILE", type=str, required=False)
@add_options()
def cloudcutter(profile: str, output: click.File, **kwargs):
    """
    Build from Cloudcutter device profile

    Use this to generate ESPHome config based on a Cloudcutter device profile.
    """

    if not profile:
        devices_slug, devices_name = cloudcutter_list_devices()

        print("Choose a Cloudcutter profile, that matches your particular device:")
        question = inquirer.List(
            "device_name",
            message="Cloudcutter profile",
            choices=devices_name,
            validate=True,
        )
        answer = inquirer.prompt([question])
        if not answer:
            return
        selection = devices_name.index(answer["device_name"])
        profile = devices_slug[selection]

    device = cloudcutter_get_device(profile)
    write_upk(device, output, **kwargs)


@cli.command()
@click.argument("FILE", type=click.File("rb"))
@add_options()
@click.option("--storage-only", help="Dump storage data only (no YAML)", is_flag=True)
def firmware(file: click.File, output: click.File, **kwargs):
    """
    Analyze firmware dump

    Use this to parse Storage Data from a full (2 MiB) firmware dump (.BIN).
    """

    work = UpkThread(
        file=file.name,
        on_storage=lambda data: write_upk(data, output, **kwargs),
        on_error=error,
    )
    work.start()


def write_upk(data: dict, output: click.File, storage_only: bool = False, **kwargs):
    if storage_only:
        text = json.dumps(data, indent="\t")
    else:
        opts = Opts(**kwargs)
        yr = upk2esphome(data, opts)
        for line in yr.logs:
            info(f"UPK: {line}")
        for line in yr.warnings:
            warning(line)
        for line in yr.errors:
            error(line)
        text = yr.text

    if output:
        with output as f:
            f.write(text)
            print(f"Saved as '{output.name}'")
    else:
        print(text)
