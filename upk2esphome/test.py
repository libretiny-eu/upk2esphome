#  Copyright (c) Kuba Szczodrzyński 2023-4-22.

if __name__ == "__main__":
    import json
    import sys
    from glob import glob
    from os.path import basename, dirname, isfile, join

    from .generator import upk2esphome
    from .opts import Opts

    opts = Opts(
        esphome_block=False,
        common=False,
        web_server=False,
        restart=False,
        uptime=False,
        lt_version=False,
    )

    mask = "*.txt"

    errors = []

    argv = list(sys.argv)
    if "-w" in argv:
        write_expected = True
        argv.remove("-w")
    else:
        write_expected = False

    for file in glob(join(dirname(__file__), "tests", mask)):
        if len(argv) == 2 and argv[1] not in file:
            continue
        with open(file, "r") as f:
            d = f.read().strip()
        print(file)
        extras_file = file.replace(".txt", ".json")
        if isfile(extras_file):
            print(extras_file)
            with open(extras_file, "r", encoding="utf-8") as f:
                extras = json.load(f)
        else:
            extras = None
        yr = upk2esphome(d, opts, extras)
        print("\n".join(f"I: {s}" for s in yr.logs))
        print("\n".join(f"W: {s}" for s in yr.warnings))
        print("\n".join(f"E: {s}" for s in yr.errors))
        print(yr.text)
        print("-" * 80)

        expected = join(
            dirname(__file__), "tests", "expected_output", basename(file)
        ).replace(".txt", ".yaml")
        if not isfile(expected):
            if write_expected:
                with open(expected, "w") as f:
                    f.write(yr.text)
                continue
            errors.append(
                f"missing expected output for {basename(file)}, run with -w to write"
            )
            continue
        with open(expected, "r") as f:
            expected_yaml = f.read()
            if expected_yaml.strip() != yr.text.strip():
                errors.append(f"content of {expected} was not as expected")

    if errors:
        print("got errors:")
        print("\n".join(errors))
        sys.exit(1)
