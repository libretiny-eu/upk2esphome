#  Copyright (c) Kuba Szczodrzyński 2023-9-4.

DISCLAIMER_TEXT = """
While the author has taken care to write the converter as well as possible, keep in mind that this might not be 100% accurate!

There may be some errors, such as missing components (unsupported types) or incorrect readings.

This serves mostly as a kickstart config, rather than a production-ready file. Make sure to review the output before uploading it to the device.

**We do not take responsibility for using this tool and the generated configs.**
"""

MESSAGE_TUYAMCU = """
This device has a TuyaMCU secondary processor.

Additional schema information is required, in order to build ESPHome components for it.

Pressing OK will open the 'Schema Download' application, which will let you download the necessary data.
Pressing Cancel will let you write components manually.

For more information, visit:
https://esphome.io/components/tuya
"""

MESSAGE_SCHEMA_MISSING_MODEL = """
Missing schema model description

The API response doesn't include the schema model.
Please inspect the response data and report an error to the LibreTiny developers.
"""

MESSAGE_FETCHED_SCHEMA_MODEL = """
Fetched schema model

The schema model for TuyaMCU has been downloaded.

Press OK to continue setting up your ESPHome config.
"""

MESSAGE_SCHEMA_INCORRECT_MODEL = """
Incorrect device schema model

UPK2ESPHome couldn't generate TuyaMCU config based on the provided schema model.

If you think that's an error, report it to the LibreTiny developers.
Otherwise, try downloading the schema again.
"""

SCHEMA_PULL_URL = "https://schema.upk.libretiny.eu/pullSchema"
SCHEMA_URL_PREFIX = "https://schema.upk.libretiny.eu/schemas/"
