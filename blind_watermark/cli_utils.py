import sys
import os
import json
import secrets

def print_error_and_exit(msg):
    """Print a clean error message and exit."""
    print(f"\033[91mError: {msg}\033[0m")
    sys.exit(1)

def print_warning(msg):
    """Print a warning message."""
    print(f"\033[93mWarning: {msg}\033[0m")

def print_success(msg):
    """Print a success message."""
    print(f"\033[92m{msg}\033[0m")

def suppress_opencv_warnings():
    """Attempt to suppress OpenCV C-level warnings (like fallback depth)."""
    os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

def generate_password():
    """Generate a random 4-6 digit password."""
    return secrets.randbelow(900000) + 100000  # 6-digit random number

def save_metadata(output_path, password, wm_shape, metadata_path=None):
    """Save metadata to a JSON file."""
    if not metadata_path:
        base_name, _ = os.path.splitext(output_path)
        metadata_path = f"{base_name}.json"

    metadata = {
        "password": password,
        "wm_shape": wm_shape
    }
    try:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)
        print_success(f"Metadata saved successfully to {metadata_path}")
    except Exception as e:
        print_error_and_exit(f"Failed to save metadata to {metadata_path}: {e}")

def load_metadata(image_path, metadata_path=None):
    """Load metadata from a JSON file."""
    if not metadata_path:
        base_name, _ = os.path.splitext(image_path)
        metadata_path = f"{base_name}.json"

    if not os.path.exists(metadata_path):
        print_error_and_exit(
            f"Metadata file not found: {metadata_path}\n"
            "Please specify the correct metadata path using '-m <metadata_path>' "
            "or ensure it exists in the same directory as the image."
        )

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata, metadata_path
    except Exception as e:
        print_error_and_exit(f"Failed to load metadata from {metadata_path}: {e}")
