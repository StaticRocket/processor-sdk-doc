#!/bin/python

"""Simple helper for renaming files and fixing up refs
"""

import argparse
import logging
import re
import subprocess
from multiprocessing import Pool
from pathlib import Path

logger = logging.getLogger(__name__)


def git_rename(source, destination, dryrun):
    """Wrapper and logger for git rename

    :param source: Pathlib path to source file
    :param destination: Pathlib path to destination file
    :param dryrun: Bool to toggle writing files
    """
    command = ["git", "mv"]
    if dryrun:
        command.append("--dry-run")
    command.extend([source, destination])
    result = subprocess.run(command, capture_output=True, check=True, text=True)
    for line in result.stdout.splitlines():
        logging.info("git:%s", line)


def update_file_contents(file, pattern, new, dryrun):
    """Update given file changing all instances of pattern to new string

    :param file: Pathlib path to source file
    :param pattern: Regex pattern to match against
    :param new: String to replace the regex expression with
    :param dryrun: Bool to toggle writing files
    """
    logging.debug("Reading:%s", file)
    text = file.read_text()
    log_str = "Would modify" if dryrun else "Modifying"
    for match in pattern.finditer(text):
        logging.info("%s:%s:%s:%s", log_str, file, match.group(0).strip(), new.strip())
    if dryrun:
        return
    pattern.sub(new)


def multiprocessing_handler(command, command_args, jobs):
    """Simple wrapper to handle job parallelization

    :param command: Function to execute in the pool
    :param command_args: Map of arguments for each execution
    :param jobs: Integer count of threads to use
    """
    with Pool(jobs) as pool:
        pool.starmap(command, command_args)


def update_includes(source, destination, dryrun, jobs):
    """Check all files for any old refs

    :param source: Pathlib path to source file
    :param destination: Pathlib path to destination file
    :param dryrun: Bool to toggle writing files
    :param jobs: Integer count of threads to use
    """
    file_list = [path for path in Path("source/").glob("**/*.rst") if path.is_file()]
    ref_destination = (
        ".. include:: "
        + Path("/").joinpath(destination.relative_to("source/")).as_posix()
        + "\n"
    )
    pattern = re.compile(r"(\.\. include::)(.*)(" + re.escape(source.name) + r")(\s|$)")
    logging.debug("config_pattern:%s", pattern)
    mapping = [(file, pattern, ref_destination, dryrun) for file in file_list]
    multiprocessing_handler(update_file_contents, mapping, jobs)


def update_configs(source, destination, dryrun, jobs):
    """Check all files for any old refs

    :param source: Pathlib path to source file
    :param destination: Pathlib path to destination file
    :param dryrun: Bool to toggle writing files
    :param jobs: Integer count of threads to use
    """
    file_list = [path for path in Path("configs/").glob("**/*.txt") if path.is_file()]
    file_list.extend(
        [path for path in Path("configs/").glob("**/*.py") if path.is_file()]
    )
    config_source = source.parent.relative_to("source/").joinpath(source.stem)
    config_destination = (
        destination.parent.relative_to("source/").joinpath(destination.stem).as_posix()
        + "\n"
    )
    pattern = re.compile(r"(" + re.escape(config_source.as_posix()) + r"){1}(\s+|$)")
    logging.debug("config_pattern:%s", pattern)
    mapping = [(file, pattern, config_destination, dryrun) for file in file_list]
    multiprocessing_handler(update_file_contents, mapping, jobs)


def rename(source, destination, dryrun, jobs):
    """Main processing context

    :param source: Pathlib path to source file
    :param destination: Pathlib path to destination file
    :param dryrun: Bool to toggle writing files
    :param jobs: Integer count of threads to use
    """
    if source.exists():
        git_rename(source, destination, dryrun)
        update_includes(source, destination, dryrun, jobs)
        update_configs(source, destination, dryrun, jobs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="rename.py", description="File rename helper for processor-sdk-doc"
    )

    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--no-dry-run", action="store_false")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-j", "--jobs", type=int, default=4)

    args = parser.parse_args()

    LOG_LEVEL = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=LOG_LEVEL)
    rename(args.source, args.destination, args.no_dry_run, args.jobs)
