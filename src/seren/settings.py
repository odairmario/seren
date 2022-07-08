"""
File: settings.py
Author: Odair M.
Email: odairmario45@gmail.com
Github: https://github.com/odairmario/seren
Description: Settings from the project
"""
import logging

LICENSE = "MIT"
AUTHOR = "Odair M."
COPYRIGHT = "Odair M."
GITHUB = "https://github.com/odairmario/seren"

logs_level = "DEBUG"
# logs_directory = logs_conf.get("directory","")
# logs_output = os.path.join(logs_directory,logs_conf.get("path","experiment.log"))
# logs_output_rotation = os.path.join(
#        logs_directory,
#        logs_conf.get("file_rotation","experiment.old.log")
#        )
# logs_handles = [
#    FileHandler(
#        filename=logs_output,
#        encoding='utf-8'
#    ),
#    RotatingFileHandler(
#    logs_output_rotation,
#    backupCount=logs_conf.get("backups_count",5),
#    maxBytes=logs_conf.get("max_size",2**20),
#    encoding="utf-8"
#    ),
#    StreamHandler()
# ]

logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.getLevelName(logs_level),
    # handlers=logs_handles
)
