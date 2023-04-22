#  Copyright (c) Kuba Szczodrzyński 2023-4-22.

if __name__ == "__main__":
    from glob import glob
    from os.path import dirname, join

    from .generator import generate_yaml

    for file in glob(join(dirname(__file__), "tests", "*.txt")):
        with open(file, "r") as f:
            d = f.read().strip()
        print(file)
        yr = generate_yaml(d)
        print("\n".join(yr.logs))
        print("\n".join(yr.warnings))
        print(yr.text)
        print("-" * 80)
