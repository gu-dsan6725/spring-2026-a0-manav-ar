import logging
from typing import Optional

import requests


# Configure logging with basicConfig
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,p%(process)s,{%(filename)s:%(lineno)d},%(levelname)s,%(message)s",
)

logger = logging.getLogger(__name__)

EC2_METADATA_URL = "http://169.254.169.254"
EC2_METADATA_TOKEN_TTL = "21600"


def _get_ec2_metadata_token() -> Optional[str]:
    """Fetch IMDSv2 token for EC2 metadata access."""
    try:
        response = requests.put(
            f"{EC2_METADATA_URL}/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": EC2_METADATA_TOKEN_TTL},
            timeout=2,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.warning(f"Failed to get EC2 metadata token: {e}")
        return None


def _get_ec2_metadata(
    token: str,
    path: str,
) -> Optional[str]:
    """Fetch a specific EC2 metadata value."""
    try:
        response = requests.get(
            f"{EC2_METADATA_URL}/latest/meta-data/{path}",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.warning(f"Failed to get EC2 metadata for {path}: {e}")
        return None


def fetch_all_ec2_metadata() -> dict:
    """Fetch all relevant EC2 instance metadata."""
    metadata = {}

    token = _get_ec2_metadata_token()
    if not token:
        logger.info("Not running on EC2 or metadata service unavailable")
        return metadata

    metadata_paths = [
        ("instance_id", "instance-id"),
        ("instance_type", "instance-type"),
        ("availability_zone", "placement/availability-zone"),
        ("region", "placement/region"),
        ("private_ip", "local-ipv4"),
        ("public_ip", "public-ipv4"),
        ("ami_id", "ami-id"),
        ("hostname", "hostname"),
    ]

    for key, path in metadata_paths:
        value = _get_ec2_metadata(token, path)
        if value:
            metadata[key] = value

    return metadata


def print_ec2_metadata(
    metadata: dict,
) -> None:
    """Print EC2 instance metadata."""
    print("\n" + "=" * 80)
    print("EC2 INSTANCE METADATA:")
    print("=" * 80)

    if not metadata:
        print("Not running on EC2 or metadata unavailable")
    else:
        for key, value in metadata.items():
            display_key = key.replace("_", " ").title()
            print(f"{display_key}: {value}")

    print("=" * 80)
