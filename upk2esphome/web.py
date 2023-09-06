#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from js import jQuery, onPyscriptReady

from upk2esphome import Opts, upk2esphome


def on_pyscript_ready():
    onPyscriptReady(Opts().__dict__)


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

    def fix_br(s: str) -> str:
        return s.replace("\n", "<br>")

    input_data = jQuery("#input").val()
    yr = upk2esphome(input_data, opts)
    jQuery("#output").val(yr.text)
    jQuery("#logs").html("<pre>" + "<br>".join(yr.logs) + "</pre>")
    jQuery("#warnings").html(
        "".join(
            f'<div class="alert alert-danger" role="alert">{fix_br(e)}</div>'
            for e in yr.errors
        )
        + "".join(
            f'<div class="alert alert-warning" role="alert">{fix_br(w)}</div>'
            for w in yr.warnings
        )
    )
