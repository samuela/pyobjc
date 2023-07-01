# This file is generated by objective.metadata
#
# Last update: Sat Jul  1 14:00:35 2023
#
# flake8: noqa

import objc, sys
from typing import NewType

if sys.maxsize > 2**32:

    def sel32or64(a, b):
        return b

else:

    def sel32or64(a, b):
        return a


if objc.arch == "arm64":

    def selAorI(a, b):
        return a

else:

    def selAorI(a, b):
        return b


misc = {}
constants = """$kSMDomainSystemLaunchd$kSMDomainUserLaunchd$kSMErrorDomainFramework$kSMErrorDomainIPC$kSMErrorDomainLaunchd$kSMInfoKeyAuthorizedClients$kSMInfoKeyPrivilegedExecutables$"""
enums = """$SMAppServiceStatusEnabled@1$SMAppServiceStatusNotFound@3$SMAppServiceStatusNotRegistered@0$SMAppServiceStatusRequiresApproval@2$kSMErrorAlreadyRegistered@12$kSMErrorAuthorizationFailure@4$kSMErrorInternalFailure@2$kSMErrorInvalidPlist@10$kSMErrorInvalidSignature@3$kSMErrorJobMustBeEnabled@9$kSMErrorJobNotFound@6$kSMErrorJobPlistNotFound@8$kSMErrorLaunchDeniedByUser@11$kSMErrorServiceUnavailable@7$kSMErrorToolNotValid@5$"""
misc.update(
    {
        "enum (unnamed at /Users/ronald/Applications/Xcode-beta.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.0.sdk/System/Library/Frameworks/ServiceManagement.framework/Headers/SMErrors.h:58:1)": NewType(
            "enum (unnamed at /Users/ronald/Applications/Xcode-beta.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.0.sdk/System/Library/Frameworks/ServiceManagement.framework/Headers/SMErrors.h:58:1)",
            int,
        ),
        "SMAppServiceStatus": NewType("SMAppServiceStatus", int),
    }
)
misc.update({})
misc.update(
    {
        "kSMRightModifySystemDaemons": b"com.apple.ServiceManagement.daemons.modify",
        "kSMRightBlessPrivilegedHelper": b"com.apple.ServiceManagement.blesshelper",
    }
)
functions = {
    "SMJobBless": (
        b"Z^{__CFString=}^{__CFString=}^{AuthorizationOpaqueRef=}^^{__CFError}",
        "",
        {
            "arguments": {
                3: {
                    "already_cfretained": True,
                    "type_modifier": "o",
                    "null_accepted": True,
                }
            }
        },
    ),
    "SMJobRemove": (
        b"Z^{__CFString=}^{__CFString=}^{AuthorizationOpaqueRef=}Z^^{__CFError}",
        "",
        {
            "arguments": {
                4: {
                    "already_cfretained": True,
                    "type_modifier": "o",
                    "null_accepted": True,
                }
            }
        },
    ),
    "SMJobCopyDictionary": (
        b"^{__CFDictionary=}^{__CFString=}^{__CFString=}",
        "",
        {"retval": {"already_cfretained": True}},
    ),
    "SMJobSubmit": (
        b"Z^{__CFString=}^{__CFDictionary=}^{AuthorizationOpaqueRef=}^^{__CFError}",
        "",
        {
            "arguments": {
                3: {
                    "already_cfretained": True,
                    "type_modifier": "o",
                    "null_accepted": True,
                }
            }
        },
    ),
    "SMLoginItemSetEnabled": (b"Z^{__CFString=}Z",),
    "SMCopyAllJobDictionaries": (
        b"^{__CFArray=}^{__CFString=}",
        "",
        {"retval": {"already_cfretained": True}},
    ),
}
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(
        b"SMAppService",
        b"registerAndReturnError:",
        {"retval": {"type": b"Z"}, "arguments": {2: {"type_modifier": b"o"}}},
    )
    r(
        b"SMAppService",
        b"unregisterAndReturnError:",
        {"retval": {"type": b"Z"}, "arguments": {2: {"type_modifier": b"o"}}},
    )
    r(
        b"SMAppService",
        b"unregisterWithCompletionHandler:",
        {
            "arguments": {
                2: {
                    "callable": {
                        "retval": {"type": b"v"},
                        "arguments": {0: {"type": b"^v"}, 1: {"type": b"@"}},
                    }
                }
            }
        },
    )
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
