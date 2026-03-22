import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="my-first-codex")
    parser.add_argument("--name", default="world", help="Name to greet")
    args = parser.parse_args()

    print(f"Hello, {args.name}!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
