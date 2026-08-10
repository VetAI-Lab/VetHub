from __future__ import annotations

import argparse

from . import build, discover, enrich, validate


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vethub",
        description="Veterinary open-resource registry and discovery engine",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("discover", help="Discover candidate GitHub repositories")
    sub.add_parser("enrich", help="Refresh GitHub metadata for known resources")
    sub.add_parser("build", help="Build machine-readable and website catalogs")
    sub.add_parser("validate", help="Validate registry integrity")
    sub.add_parser("refresh", help="Discover, enrich, validate, and rebuild")

    args = parser.parse_args()

    if args.command == "discover":
        discover.run()
    elif args.command == "enrich":
        enrich.run()
    elif args.command == "build":
        build.run()
    elif args.command == "validate":
        validate.run()
    elif args.command == "refresh":
        discover.run()
        enrich.run()
        validate.run()
        build.run()


if __name__ == "__main__":
    main()
