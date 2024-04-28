"""
Python mapping for the ClassKit framework.

This module does not contain docstrings for the wrapped code, check Apple's
documentation for details on how to use these functions and classes.
"""


def _setup():
    import sys

    import Foundation
    import objc
    from . import _metadata, _ClassKit

    dir_func, getattr_func = objc.createFrameworkDirAndGetattr(
        name="ClassKit",
        frameworkIdentifier="com.apple.ClassKit",
        frameworkPath=objc.pathForFramework(
            "/System/Library/Frameworks/ClassKit.framework"
        ),
        globals_dict=globals(),
        inline_list=None,
        parents=(
            _ClassKit,
            Foundation,
        ),
        metadict=_metadata.__dict__,
    )

    globals()["__dir__"] = dir_func
    globals()["__getattr__"] = getattr_func

    for cls, sel in (
        ("CLSObject", b"init"),
        ("CLSObject", b"new"),
        ("CLSContext", b"init"),
        ("CLSContext", b"new"),
        ("CLSDataStore", b"init"),
        ("CLSDataStore", b"new"),
        ("CLSActivityItem", b"init"),
        ("CLSActivityItem", b"new"),
    ):
        objc.registerUnavailableMethod(cls, sel)

    del sys.modules["ClassKit._metadata"]


globals().pop("_setup")()
