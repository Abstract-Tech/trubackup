from datetime import datetime
import os

from pendulum.exceptions import ParserError
from swiftclient.service import SwiftService
import pendulum
import swiftclient.service


def getSwiftService(info):
    """Given a configuration object, prepare a Swift service.
    """
    os.environ.update(info.swift.env)
    # Note that swiftclient builds its options at import time.
    # We force repopulating them after setting the environment
    swiftclient.service._default_global_options = (
        swiftclient.service._build_default_global_options()
    )
    return SwiftService()


def get_timestamps(container, swift):
    """Return a list of 2-tuples (timestamp, original_dirname) of directories
    in the given container that parse to timestamps.
    """
    elements = []
    for res in swift.list(container, options=dict(prefix="", delimiter="/")):
        elements += [el["subdir"][:-1] for el in res["listing"] if "subdir" in el]
    timestamps = []
    for element in elements:
        try:
            # `element` includes a trailing slash
            pendulum_dt = pendulum.parse(element).timestamp()
            dt = datetime.fromtimestamp(pendulum_dt)
            timestamps.append((dt, element))
        except ParserError:
            pass
    return timestamps
