# S3 example

This example shows how to interact with the CESNET S3-compatible object storage using boto3.

Follow the [repository quick start](../README.md#quick-start) to prepare the Python
environment, install the dependencies, and configure `s3/.env`.

## Usage

Create the bucket configured in `.env`:

- `python s3/create_bucket.py`

Bucket names must be unique within the shared CESNET S3 endpoint. A generic name
such as `test-bucket` may already belong to another user, so use a distinctive
name such as `<username>-<project>-test`. If creation reports that the bucket
already exists and uploading returns `AccessDenied`, choose another name and
create a new bucket.

Upload the demo objects:

- `python s3/upload.py`
- `python s3/upload.py --dry-run` to preview the planned uploads without sending data

Read the private object with the configured credentials, then read the public
object and print its public URL:

- `python s3/read.py`

Open `s3/read.html` in a browser to load the public example without making a
cross-origin `fetch` request. Update `publicUrl` in the file if the configured
endpoint, group, or bucket name changes. CESNET's anonymous public URLs use the
tenant-qualified bucket name `<GROUP>:<BUCKET>`, even though authenticated S3
operations use only `<BUCKET>`.

## Reference links

- General documentation: https://docs.du.cesnet.cz/en/docs/object-storage-s3/s3-service
- Credentials and endpoint management: https://gatekeeper.du.cesnet.cz/#/
