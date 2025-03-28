#!/usr/bin/env python3

import argparse
import json
import sys
import yaml
from uvicorn.importer import import_from_string
from pathlib import PurePath

parser = argparse.ArgumentParser(prog="extract-openapi.py")
parser.add_argument("app",       help='App import string. Eg. "main:app"', nargs='*')
parser.add_argument("-o", "--out-dir", help="Output directory", default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    for f in args.app:
        if ':' not in f:
            out_file = f.rsplit('.', 1)[0] + '.yaml'
            import_file = f.rsplit('.', 1)[0] + ':app'
            import_file = import_file.replace('/', '.')
        else:
            out_file = args.app.split(':')[0] + '.yaml'
            import_file = f

        print(f"importing app from {import_file}")
        app = import_from_string(import_file)
        openapi = app.openapi()
        version = openapi.get("openapi", "unknown version")
        print(f"writing openapi spec v{version}")

        if args.out_dir:
            out_file = PurePath(args.out_dir) / PurePath(out_file).name

        with open(out_file, "w") as f:
            yaml.dump(openapi, f, sort_keys=False)

        print(f"spec written to {out_file}\n")
