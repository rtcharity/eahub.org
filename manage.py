import os
import sys

from django.core import management

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "eahub.config.settings"
    management.execute_from_command_line(sys.argv)
