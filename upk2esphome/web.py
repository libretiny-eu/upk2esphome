#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from js import jQuery

from upk2esphome import Opts, generate_yaml


def on_run_click():
    opts = {}
    options = jQuery("#options input")
    for i in range(options.length):
        el = options[i]
        el_id = el.id
        if not el_id.startswith("opts_"):
            continue
        el_value = el.value if el.type == "text" else el.checked
        opts[el_id[5:]] = el_value
    opts = Opts(**opts)

    config = jQuery("#input").val()
    yr = generate_yaml(config, opts)
    jQuery("#output").val(yr.text)
    jQuery("#logs").html("<pre>" + "<br>".join(yr.logs) + "</pre>")
    jQuery("#warnings").html(
        "".join(
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in yr.errors
        )
        + "".join(
            f'<div class="alert alert-warning" role="alert">{w}</div>'
            for w in yr.warnings
        )
    )
