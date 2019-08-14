import os

from swiftclient.service import SwiftService
import swiftclient.service


def getSwiftService(info):
    """Given a configuration object, prepare a Swift service.
    """
    swift_info = info["swift"]
    os.environ.update(swift_info["env"])
    # Note that swiftclient builds its options at import time.
    # We force repopulating them after setting the environment
    swiftclient.service._default_global_options = (
        swiftclient.service._build_default_global_options()
    )
    return SwiftService()
