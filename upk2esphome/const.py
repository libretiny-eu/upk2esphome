#  Copyright (c) Kuba Szczodrzyński 2023-9-4.

DISCLAIMER_TEXT = """
While the author has taken care to write the converter as well as possible, keep in mind that this might not be 100% accurate!

There may be some errors, such as missing components (unsupported types) or incorrect readings.

This serves mostly as a kickstart config, rather than a production-ready file. Make sure to review the output before uploading it to the device.

**We do not take responsibility for using this tool and the generated configs.**
"""

TUYAMCU_MESSAGE = """
This device has a TuyaMCU secondary processor.

Additional schema information is required, in order to build ESPHome components for it.

Pressing OK will open the 'Schema Download' application, which will let you download the necessary data.
Pressing Cancel will let you write components manually.

For more information, visit:
https://esphome.io/components/tuya
"""

SCHEMA_PULL_URL = "https://schema.upk.libretiny.eu/pullSchema"
