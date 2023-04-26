#  Copyright (c) Kuba Szczodrzyński 2023-4-22.

if __name__ == "__main__":
    import sys
    from glob import glob
    from os.path import dirname, join

    from .generator import generate_yaml
    from .opts import Opts

    for file in glob(join(dirname(__file__), "tests", "*.txt")):
        if len(sys.argv) == 2 and sys.argv[1] not in file:
            continue
        with open(file, "r") as f:
            d = f.read().strip()
        print(file)
        yr = generate_yaml(d, Opts())
        print("\n".join(yr.logs))
        print("\n".join(yr.warnings))
        print("\n".join(yr.errors))
        print(yr.text)
        print("-" * 80)
