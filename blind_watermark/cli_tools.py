import argparse
import os
import sys

from .blind_watermark import WaterMark
from .cli_utils import (
    print_error_and_exit,
    print_success,
    suppress_opencv_warnings,
    generate_password,
    save_metadata,
    load_metadata
)

def embed_command(args):
    password = args.password
    if password is None:
        password = generate_password()
    else:
        try:
            password = int(password)
        except ValueError:
            print_error_and_exit("Password (-p) must be an integer.")

    bwm = WaterMark(password_img=password)

    if not os.path.exists(args.origin_image):
        print_error_and_exit(f"Original image not found: {args.origin_image}")

    try:
        bwm.read_img(args.origin_image)
        bwm.read_wm(args.watermark_text, mode='str')
        bwm.embed(args.output_image)
    except Exception as e:
        print_error_and_exit(f"Failed to embed watermark: {e}")

    wm_shape = len(bwm.wm_bit)
    print_success(f"Embed succeed! File saved to: {args.output_image}")

    save_metadata(args.output_image, password, wm_shape, args.metadata_path)

def extract_command(args):
    if not os.path.exists(args.watermarked_image):
        print_error_and_exit(f"Watermarked image not found: {args.watermarked_image}")

    metadata, metadata_path = load_metadata(args.watermarked_image, args.metadata_path)

    password = args.password
    if password is None:
        if 'password' in metadata:
            password = metadata['password']
        else:
            print_error_and_exit("Password not found in metadata and not provided via '-p'.")

    try:
        password = int(password)
    except ValueError:
        print_error_and_exit("Password must be an integer.")

    if 'wm_shape' not in metadata:
        print_error_and_exit(f"Watermark shape ('wm_shape') not found in metadata file {metadata_path}.")

    wm_shape = metadata['wm_shape']

    bwm = WaterMark(password_img=password)

    try:
        wm_str = bwm.extract(filename=args.watermarked_image, wm_shape=wm_shape, mode='str')
    except Exception as e:
        print_error_and_exit(f"Failed to extract watermark: {e}")

    print_success("Extract succeed! The extracted watermark is:")
    print(wm_str)

def main():
    suppress_opencv_warnings()

    parser = argparse.ArgumentParser(
        description="Blind Watermark CLI - Embed and Extract digital watermarks from images."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
    subparsers.required = True

    # Embed command
    embed_parser = subparsers.add_parser(
        "embed",
        aliases=["i", "insert"],
        help="Embed a watermark into an image."
    )
    embed_parser.add_argument("origin_image", help="Path to the original image.")
    embed_parser.add_argument("watermark_text", help="Text to embed as watermark.")
    embed_parser.add_argument("output_image", help="Path to save the output watermarked image.")
    embed_parser.add_argument("-p", "--password", help="Optional password (integer). If omitted, one will be auto-generated.")
    embed_parser.add_argument("-m", "--metadata_path", help="Optional path to save metadata. If omitted, defaults to output_image path but with .json extension.")
    embed_parser.set_defaults(func=embed_command)

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract",
        aliases=["e"],
        help="Extract a watermark from an image."
    )
    extract_parser.add_argument("watermarked_image", help="Path to the watermarked image.")
    extract_parser.add_argument("-p", "--password", help="Optional password (integer). If omitted, it will be read from the metadata file.")
    extract_parser.add_argument("-m", "--metadata_path", help="Optional path to the metadata file. If omitted, it tries to find a .json file with the same name as the watermarked_image in the same directory.")
    extract_parser.set_defaults(func=extract_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
