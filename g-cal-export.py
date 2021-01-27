from icalendar import Calendar, Event, vDatetime
import ics
import argparse
import logging
import coloredlogs
from pathlib import Path

import rcal


DESCRIPTION = "Exports ics calendar to json file"
MODULE_NAME = Path(__file__).stem


class CmdOptions:
    def __init__(self, args):
        self.in_file: str = args.in_file

    def __str__(self):
        return f"in_file: '{self.in_file}'"

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser(description=DESCRIPTION)

        parser.add_argument(
            "--in-file",
            required=True,
            help="Path to input ics file")

        return CmdOptions(parser.parse_args())


def init_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    coloredlogs.install(level="DEBUG", milliseconds=True)
    return logger


def load_ics_content(in_file: str):
    with open(in_file, "r") as f:
        return f.read()


def map_status(ics_status: str) -> rcal.RTaskStatus:
    return {
        "CONFIRMED": rcal.RTaskStatus.NEW,
    }[ics_status.upper()]


def main():
    cmd_options = CmdOptions.parse()
    logger = init_logger(MODULE_NAME)
    logger.info(DESCRIPTION)
    logger.info(cmd_options)
    logger.info(f"Reading '{cmd_options.in_file}' file ...")
    ics_content = load_ics_content(cmd_options.in_file)
    logger.info(f"{len(ics_content)} characters read")

    logger.info(f"Parsing calendar events ...")
    cal = ics.Calendar(ics_content)

    for event in cal.events:
        task = rcal.RTask(
            event.name,
            due=event.begin.datetime,
            description=event.description,
            created=event.created.datetime,
            all_day=bool(event.all_day),
            status=map_status(event.status),
            extra=event.extra,

        )

        logger.info(f"{event}")
        logger.info(f"{task}")


if __name__ == "__main__":
    main()
