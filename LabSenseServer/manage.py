#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LabSenseServer.settings")

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(PROJECT_ROOT, "LabSenseServer"))
    sys.path.append(os.path.join(PROJECT_ROOT, "LabSenseServer/chat"))
    sys.path.append(os.path.join(PROJECT_ROOT, "LabSenseServer/LabSenseApp"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
