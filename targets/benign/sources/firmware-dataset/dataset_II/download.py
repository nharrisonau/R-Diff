import os
import re
import argparse
import requests
import pandas as pd
import subprocess
from concurrent.futures import ThreadPoolExecutor


def main(firmware_data_path_or_dir, save_path):
    """Main function to download all firmware samples from CSV file(s) and unpack them."""
    if os.path.isdir(firmware_data_path_or_dir):
        download_firmware_from_directory(firmware_data_path_or_dir, save_path)
    elif os.path.isfile(firmware_data_path_or_dir) and firmware_data_path_or_dir.endswith('.csv'):
        download_firmware(firmware_data_path_or_dir, save_path)
    else:
        print(f"Invalid input: {firmware_data_path_or_dir} is neither a directory nor a CSV file.")
        return


def download_firmware_from_directory(firmware_data_dir, save_path):
    """Download firmware files from all CSV files in the specified directory."""
    os.makedirs(save_path, exist_ok=True)  # Create the output folder if it doesn't exist

    # Iterate over each CSV file in the firmware_data_dir
    for root, _, files in os.walk(firmware_data_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                download_firmware(csv_path, save_path)


def download_firmware(firmware_data_path, save_path):
    """Download all firmware files from URLs in a CSV and unpack them per product."""
    # Load firmware URLs from the CSV file
    data = pd.read_csv(firmware_data_path)
    urls = data['url'].tolist()

    # Get the product name from the CSV file name
    product_name = os.path.splitext(os.path.basename(firmware_data_path))[0]

    # Create a directory for the product name within the save path
    product_save_path = os.path.join(save_path, product_name)
    os.makedirs(product_save_path, exist_ok=True)

    # Download each file sequentially
    for url in urls:
        download_file(url, product_save_path, product_name)

    # Unpack the firmware files for this product
    unpack_firmware_files(product_save_path)


def download_file(url, save_path, product_name):
    """Download a single firmware file from a URL."""
    try:
        # Extract the version from the URL
        filename = os.path.basename(url)
        match = re.search(r'v(\d{1,2}\.\d{1,2}\.\d{1,2})', url)
        if match:
            version = match.group(1)
        else:
            version = "unknown_version"

        # Create a directory for the product-version
        product_version_dir = f"{version}"
        full_save_path = os.path.join(save_path, product_version_dir)
        os.makedirs(full_save_path, exist_ok=True)

        # Set the full path to save the firmware file
        full_path = os.path.join(full_save_path, filename)

        # Make the request and save the file in chunks
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Write only if chunk is not empty
                    file.write(chunk)
        print(f"Downloaded: {full_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


def unpack_file(file_path, root):
    """Unpack a single file using binwalk."""
    try:
        subprocess.run(['binwalk', '-Mre', '--directory', root, file_path], check=True)
        print(f"Unpacked: {file_path}")
    except subprocess.CalledProcessError:
        pass  # Ignore errors for now


def unpack_firmware_files(product_save_path, max_workers=4):
    """Unpack firmware files in the specified product directory using binwalk, multithreaded."""
    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(product_save_path):
            for file in files:
                file_path = os.path.join(root, file)
                tasks.append(executor.submit(unpack_file, file_path, root))

    # Optionally wait for all tasks to complete
    for task in tasks:
        task.result()  # This will raise exceptions if any task failed


if __name__ == '__main__':
    # Argument parsing for command-line usage
    parser = argparse.ArgumentParser(description="Download and unpack all firmware files from a CSV file or directory of CSV files.")
    parser.add_argument('firmware_data_path_or_dir', type=str, help='Path to the CSV file or directory containing CSV files with firmware URLs')
    parser.add_argument('save_path', type=str, help='Directory to save downloaded firmware files')

    args = parser.parse_args()

    main(args.firmware_data_path_or_dir, args.save_path)
