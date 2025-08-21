import os, sys, shutil, logging
from typing import Tuple, List

file_name = os.path.basename(__file__)

def retrieve_dirs_to_backup() -> Tuple[List[str], List[str]]: ### Change it to the JSON config file
    """
    Retrieve directories to backup and destination paths from command-line arguments.

    Returns:
        A tuple containing two lists: backup directories and destination paths.
    """
    if len(sys.argv) < 3:
        sys.exit(
            f"\033[91mUsage: python {file_name} <file_with_dirs_to_backup> <file_with_backup_dests>\033[0m\n"
            "  \033[96m<file_with_dirs_to_backup>\033[0m : text file listing one directory path per line\n"
            "  \033[96m<file_with_backup_dests>\033[0m   : text file listing one destination path per line"
        )
    elif len(sys.argv) == 3:
        dir_list_file = sys.argv[1]
        with open(dir_list_file, "r") as f:
            backup_paths = f.read().splitlines()
        dest_list_file = sys.argv[2]
        with open(dest_list_file, "r") as f:
            dest_paths = f.read().splitlines()
        return backup_paths, dest_paths

def perform_backup(backup_paths, dest_paths) -> None:
    """
    Perform a backup of directories listed in the first file to destinations listed in the second file.

    Reads the list of directories to back up and the list of destination paths from the
    command-line arguments, then creates a ZIP archive of each directory in every valid
    destination path.

    Skips any non-existent source or destination paths and prints a warning for each.
    """
    existing_paths = []
    for path in dest_paths:
        if os.path.exists(path):
            existing_paths.append(path)
        else:
            logging.warning("Destination path does not exist: %s — skipping.", path)
            continue
    logging.info("Valid destination paths: %s", existing_paths)
    for path in backup_paths:
        if os.path.exists(path):
            dir_name = os.path.basename(path)
            for dest_path in existing_paths:
                archive_name = os.path.join(dest_path, dir_name)
                zip_path = archive_name + ".zip"

                # --- check existing archive freshness ---
                if os.path.exists(zip_path):
                    src_mtime = max(
                        (os.path.getmtime(root) for root, _, _ in os.walk(path)),
                        default=0
                    )
                    zip_mtime = os.path.getmtime(zip_path)
                    if src_mtime <= zip_mtime:
                        logging.info("Archive up-to-date: %s", zip_path)
                        continue

                # --- create archive ---
                print(f"\033[92mCreating\033[0m {zip_path}")
                old_mtime = os.path.getmtime(zip_path) if os.path.exists(zip_path) else None
                shutil.make_archive(archive_name, "zip", path)

                # --- verify freshness vs old archive ---
                new_mtime = os.path.getmtime(zip_path)
                if old_mtime is None:
                    logging.info("New archive created: %s", zip_path)
                elif new_mtime > old_mtime:
                    logging.info("Archive updated: %s", zip_path)
                else:
                    logging.warning("Archive NOT refreshed: %s", zip_path)
        else:
            logging.warning("Backup path does not exist: %s — skipping.", path)
            continue

def main():
    logging.info("Backup script started")
    backup_paths, dest_paths = retrieve_dirs_to_backup()
    perform_backup(backup_paths, dest_paths)

if __name__ == "__main__":
    main()
