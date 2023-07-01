# This file is generated by objective.metadata
#
# Last update: Sat Jul  1 14:04:21 2023
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
constants = """$MAMediaCharacteristicDescribesMusicAndSoundForAccessibility$MAMediaCharacteristicDescribesVideoForAccessibility$MAMediaCharacteristicTranscribesSpokenDialogForAccessibility$kMAAudibleMediaSettingsChangedNotification$kMACaptionAppearanceSettingsChangedNotification$kMADimFlashingLightsChangedNotification$"""
enums = """$kMACaptionAppearanceBehaviorUseContentIfAvailable@1$kMACaptionAppearanceBehaviorUseValue@0$kMACaptionAppearanceDisplayTypeAlwaysOn@2$kMACaptionAppearanceDisplayTypeAutomatic@1$kMACaptionAppearanceDisplayTypeForcedOnly@0$kMACaptionAppearanceDomainDefault@0$kMACaptionAppearanceDomainUser@1$kMACaptionAppearanceFontStyleCasual@5$kMACaptionAppearanceFontStyleCursive@6$kMACaptionAppearanceFontStyleDefault@0$kMACaptionAppearanceFontStyleMonospacedWithSerif@1$kMACaptionAppearanceFontStyleMonospacedWithoutSerif@3$kMACaptionAppearanceFontStyleProportionalWithSerif@2$kMACaptionAppearanceFontStyleProportionalWithoutSerif@4$kMACaptionAppearanceFontStyleSmallCapital@7$kMACaptionAppearanceTextEdgeStyleDepressed@3$kMACaptionAppearanceTextEdgeStyleDropShadow@5$kMACaptionAppearanceTextEdgeStyleNone@1$kMACaptionAppearanceTextEdgeStyleRaised@2$kMACaptionAppearanceTextEdgeStyleUndefined@0$kMACaptionAppearanceTextEdgeStyleUniform@4$"""
misc.update(
    {
        "MACaptionAppearanceDisplayType": NewType(
            "MACaptionAppearanceDisplayType", int
        ),
        "MACaptionAppearanceBehavior": NewType("MACaptionAppearanceBehavior", int),
        "MACaptionAppearanceFontStyle": NewType("MACaptionAppearanceFontStyle", int),
        "MACaptionAppearanceTextEdgeStyle": NewType(
            "MACaptionAppearanceTextEdgeStyle", int
        ),
        "MACaptionAppearanceDomain": NewType("MACaptionAppearanceDomain", int),
    }
)
misc.update({})
misc.update({})
functions = {
    "MACaptionAppearanceCopyFontDescriptorForStyle": (
        b"^{__CTFontDescriptor=}q^qq",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {1: {"null_accepted": True, "type_modifier": "o"}},
        },
    ),
    "MACaptionAppearanceCopyForegroundColor": (
        b"^{CGColor=}q^q",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {1: {"null_accepted": True, "type_modifier": "o"}},
        },
    ),
    "MACaptionAppearanceCopySelectedLanguages": (
        b"^{__CFArray=}q",
        "",
        {"retval": {"already_cfretained": True}},
    ),
    "MACaptionAppearanceCopyWindowColor": (
        b"^{CGColor=}q^q",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {1: {"null_accepted": True, "type_modifier": "o"}},
        },
    ),
    "MAImageCaptioningSetCaption": (
        b"B^{__CFURL=}^{__CFString=}^^{__CFError=}",
        "",
        {
            "arguments": {
                2: {
                    "null_accepted": True,
                    "already_cfretained": True,
                    "type_modifier": "o",
                }
            }
        },
    ),
    "MACaptionAppearanceCopyPreferredCaptioningMediaCharacteristics": (
        b"^{__CFArray=}q",
        "",
        {"retval": {"already_cfretained": True}},
    ),
    "MACaptionAppearanceGetDisplayType": (b"qq",),
    "MACaptionAppearanceGetWindowRoundedCornerRadius": (
        b"dq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
    "MACaptionAppearanceSetDisplayType": (b"vqq",),
    "MAAudibleMediaCopyPreferredCharacteristics": (
        b"^{__CFArray=}",
        "",
        {"retval": {"already_cfretained": True}, "variadic": False},
    ),
    "MACaptionAppearanceGetRelativeCharacterSize": (
        b"dq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
    "MAImageCaptioningCopyMetadataTagPath": (
        "@",
        "",
        {"retval": {"already_cfretained": True}},
    ),
    "MAImageCaptioningCopyCaption": (
        b"^{__CFString=}^{__CFURL=}^^{__CFError=}",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {
                1: {
                    "null_accepted": True,
                    "already_cfretained": True,
                    "type_modifier": "o",
                }
            },
        },
    ),
    "MACaptionAppearanceGetForegroundOpacity": (
        b"dq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
    "MACaptionAppearanceCopyBackgroundColor": (
        b"^{CGColor=}q^q",
        "",
        {
            "retval": {"already_cfretained": True},
            "arguments": {1: {"null_accepted": True, "type_modifier": "o"}},
        },
    ),
    "MADimFlashingLightsEnabled": (b"B",),
    "MACaptionAppearanceGetBackgroundOpacity": (
        b"dq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
    "MACaptionAppearanceGetTextEdgeStyle": (
        b"qq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
    "MACaptionAppearanceAddSelectedLanguage": (
        b"Bq^{__CFString=}",
        "",
        {"arguments": {1: {"null_accepted": True}}},
    ),
    "MACaptionAppearanceDidDisplayCaptions": (b"v^{__CFArray=}",),
    "MACaptionAppearanceGetWindowOpacity": (
        b"dq^q",
        "",
        {"arguments": {1: {"null_accepted": True, "type_modifier": "o"}}},
    ),
}
r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(b"MAFlashingLightsProcessor", b"canProcessSurface:", {"retval": {"type": b"Z"}})
    r(
        b"MAFlashingLightsProcessorResult",
        b"surfaceProcessed",
        {"retval": {"type": b"Z"}},
    )
finally:
    objc._updatingMetadata(False)
expressions = {}

# END OF FILE
