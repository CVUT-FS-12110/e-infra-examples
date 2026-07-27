from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import quote

from botocore.exceptions import ClientError

from upload import DEFAULT_ENV_PATH, build_client, config_from_env

PRIVATE_KEY = "uploaded_example/PRIVATE.md"
PUBLIC_KEY = "uploaded_example/PUBLIC.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read the private and public objects uploaded by upload.py."
    )
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_PATH)
    return parser.parse_args()


def read_text_object(client, bucket: str, key: str) -> str:
    try:
        response = client.get_object(Bucket=bucket, Key=key)
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "Unknown")
        message = error.get("Message") or "The S3 service did not provide details."
        raise SystemExit(f"Could not read s3://{bucket}/{key}: {code}: {message}") from exc

    body = response.get("Body")
    if body is None:
        raise SystemExit(f"Object '{key}' did not contain a body.")
    return body.read().decode("utf-8")


def build_public_url(
    endpoint_url: str | None, group: str | None, bucket: str, key: str
) -> str:
    if not endpoint_url:
        return f"s3://{bucket}/{key}"
    public_bucket = f"{group}:{bucket}" if group else bucket
    encoded_key = quote(key, safe="/")
    return f"{endpoint_url.rstrip('/')}/{quote(public_bucket, safe=':')}/{encoded_key}"


def main() -> int:
    args = parse_args()
    config = config_from_env(args.env_file)
    client = build_client(config)

    private_contents = read_text_object(client, config.bucket, PRIVATE_KEY)
    public_contents = read_text_object(client, config.bucket, PUBLIC_KEY)

    print("Private object (read with configured credentials):")
    print(private_contents)
    print("\nPublic object:")
    print(public_contents)
    print("\nPublic URL:")
    print(build_public_url(config.endpoint_url, config.group, config.bucket, PUBLIC_KEY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
