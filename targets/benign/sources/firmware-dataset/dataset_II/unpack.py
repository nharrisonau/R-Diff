from multiprocessing import Pool
import os
import argparse
import subprocess

def unpack_firmware_files(save_path):
    """Unpack firmware files in the specified directory using binwalk."""
    firmware_files = []

    # Collect all firmware file paths
    for root, _, files in os.walk(save_path):
        for file in files:
            firmware_files.append(os.path.join(root, file))
    
    # Use Pool to parallelize the unpacking process
    with Pool() as pool:
        pool.map(run_binwalk, firmware_files)

def run_binwalk(file_path):
    """Run binwalk to unpack a single firmware file."""
    try:
        print(file_path)
        subprocess.run(['binwalk', '-Mre', '--directory', os.path.dirname(file_path), file_path], check=True)
    except subprocess.CalledProcessError:
        pass  # Handle any errors gracefully

if __name__ == '__main__':
    # Argument parsing for command-line usage
    parser = argparse.ArgumentParser(description="Unpack all firmware files in a directory.")
    parser.add_argument('path', type=str, help='Directory to unpack firmware files')

    args = parser.parse_args()

    unpack_firmware_files(args.path)
