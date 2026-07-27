from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_PATH = SCRIPT_DIR / ".env"

UPLOADS = (
    ("uploaded_example/PUBLIC.md", "Public hello world", "public-read"),
    ("uploaded_example/PRIVATE.md", "Private hello world", "private"),
)


@dataclass(frozen=True)
class S3Config:
    bucket: str
    endpoint_url: str | None
    access_key: str
    secret_key: str
    region: str | None = None
    group: str | None = None


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def config_from_env(path: Path) -> S3Config:
    env_file = parse_env(path)

    def setting(*names: str) -> str | None:
        for name in names:
            value = os.environ.get(name) or env_file.get(name)
            if value:
                return value
        return None

    bucket = setting("BUCKET", "S3_BUCKET", "AWS_BUCKET")
    access_key = setting("ACCESS_KEY", "AWS_ACCESS_KEY_ID")
    secret_key = setting("SECRET_KEY", "AWS_SECRET_ACCESS_KEY")
    endpoint_url = setting("ENDPOINT", "S3_ENDPOINT", "AWS_ENDPOINT_URL")
    region = setting("REGION", "AWS_DEFAULT_REGION")
    group = setting("GROUP", "S3_TENANT")

    missing = [
        label
        for label, value in (
            ("BUCKET", bucket),
            ("ACCESS_KEY", access_key),
            ("SECRET_KEY", secret_key),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing required S3 setting(s): {', '.join(missing)}")

    return S3Config(
        bucket=bucket,
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        region=region,
        group=group,
    )


def build_client(config: S3Config):
    try:
        import boto3
    except ImportError as exc:
        raise SystemExit("Missing dependency: install boto3 before uploading.") from exc

    return boto3.client(
        "s3",
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key,
        aws_secret_access_key=config.secret_key,
        region_name=config.region,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload one public and one private test file to S3."
    )
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the upload plan without sending files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = config_from_env(args.env_file)
    client = None if args.dry_run else build_client(config)

    for key, contents, acl in UPLOADS:
        print(
            f"{'DRY ' if args.dry_run else ''}UPLOAD "
            f"s3://{config.bucket}/{key} ({acl})"
        )
        if client is not None:
            client.put_object(
                Bucket=config.bucket,
                Key=key,
                Body=contents.encode("utf-8"),
                ContentType="text/markdown",
                ACL=acl,
            )

    print("Planned 2 objects." if args.dry_run else "Uploaded 2 objects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
