#  Copyright (c) Kuba Szczodrzyński 2023-9-6.

from upk2esphome import Opts, YamlResult
from upk2esphome.datapoints import Datapoint
from upk2esphome.datapoints.utils import (
    add_filter,
    get_mapping,
    get_str_mapping,
    get_unit,
)


def process_ro(yr: YamlResult, opts: Opts, dp: Datapoint, mapping: dict) -> bool:
    match dp.spec.type:
        case Datapoint.Spec.Type.BOOL:
            binary = {
                "platform": "tuya",
                "sensor_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
            }
            yr.binary(binary)
            yr.found = True
            return True

        case Datapoint.Spec.Type.VALUE:
            sensor = {
                "platform": "tuya",
                "sensor_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
                **get_unit(yr, opts, dp, mapping),
            }
            if dp.spec.scale:
                sensor["accuracy_decimals"] = dp.spec.scale
                add_filter(sensor, "multiply", 10**-dp.spec.scale)
            yr.sensor(sensor)
            yr.found = True
            return True

        case Datapoint.Spec.Type.ENUM:
            text_id = f"tuya_{dp.code}"
            text = {
                "platform": "template",
                "id": text_id,
                **get_mapping(yr, opts, dp, mapping),
            }
            on_update = {
                "sensor_datapoint": dp.id,
                "datapoint_type": "enum",
                "then": [
                    {
                        "text_sensor.template.publish": {
                            "id": text_id,
                            "state": '!lambda "return std::to_string(x);"',
                        },
                    },
                ],
            }
            if dp.spec.range:
                options = {
                    k: get_str_mapping(mapping, v).title()
                    for k, v in enumerate(dp.spec.range)
                }
                add_filter(text, "map", [f"{k} -> {v}" for k, v in options.items()])
            yr.text_sensor(text)
            yr.tuya_on_datapoint_update(on_update)
            yr.found = True
            return True

        case Datapoint.Spec.Type.BITMAP:
            return False

        case Datapoint.Spec.Type.STRING:
            text = {
                "platform": "tuya",
                "sensor_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
            }
            yr.text_sensor(text)
            yr.found = True
            return False

        case Datapoint.Spec.Type.RAW:
            return False


def process_rw(yr: YamlResult, opts: Opts, dp: Datapoint, mapping: dict) -> bool:
    match dp.spec.type:
        case Datapoint.Spec.Type.BOOL:
            switch = {
                "platform": "tuya",
                "switch_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
            }
            yr.switch(switch)
            yr.found = True
            return True

        case Datapoint.Spec.Type.VALUE:
            number = {
                "platform": "tuya",
                "number_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
                **get_unit(yr, opts, dp, mapping),
            }
            if dp.spec.min is not None:
                number["min_value"] = dp.spec.min
            if dp.spec.max is not None:
                number["max_value"] = dp.spec.max
            if dp.spec.step is not None:
                number["step"] = dp.spec.step
            yr.number(number)
            yr.found = True
            return True

        case Datapoint.Spec.Type.ENUM:
            select = {
                "platform": "tuya",
                "enum_datapoint": dp.id,
                **get_mapping(yr, opts, dp, mapping),
                "optimistic": True,
            }
            if dp.spec.range:
                options = {
                    k: get_str_mapping(mapping, v).title()
                    for k, v in enumerate(dp.spec.range)
                }
                select["options"] = options
            yr.select(select)
            yr.found = True
            return True

        case Datapoint.Spec.Type.BITMAP:
            return False
        case Datapoint.Spec.Type.STRING:
            return False
        case Datapoint.Spec.Type.RAW:
            return False
