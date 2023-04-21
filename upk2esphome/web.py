#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from js import jQuery

from upk2esphome import generate_yaml, parse_input


def on_run_click():
    data = jQuery("#input").val()
    try:
        config = parse_input(data)
    except Exception as e:
        jQuery("#warnings").html(
            f'<div class="alert alert-danger" role="alert">{e}</div>'
        )
        return
    yr = generate_yaml(config)
    jQuery("#output").val(yr.text)
    jQuery("#logs").html("<pre>" + "<br>".join(yr.logs) + "</pre>")
    jQuery("#warnings").html(
        "".join(
            f'<div class="alert alert-warning" role="alert">{w}</div>'
            for w in yr.warnings
        )
    )
