from __future__ import annotations

import argparse
from pathlib import Path

from botocore.exceptions import ClientError

from upload import DEFAULT_ENV_PATH, build_client, config_from_env


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create the S3 bucket defined in the environment file.")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument("--region", default=None, help="Optional region override for bucket creation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = config_from_env(args.env_file)
    client = build_client(config)

    create_kwargs = {"Bucket": config.bucket}
    if args.region:
        create_kwargs["CreateBucketConfiguration"] = {"LocationConstraint": args.region}

    try:
        client.create_bucket(**create_kwargs)
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
            print(f"Bucket s3://{config.bucket} already exists.")
        else:
            raise
    else:
        print(f"Created bucket s3://{config.bucket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
