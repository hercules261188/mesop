import base64
import os
from flask import Flask, Response, request

import protos.ui_pb2 as pb

from optic.lib.runtime import runtime

app = Flask(__name__)


def render_loop():
    runtime.run_module_main()
    root_component = runtime.session().current_node()

    data = pb.UiResponse(
        render=pb.RenderEvent(
            root_component=root_component, state=runtime.session().current_state()
        )
    )

    encodedString = base64.b64encode(data.SerializeToString()).decode("utf-8")

    yield f"data: {encodedString}\n\n"
    yield "data: <stream_end>\n\n"


def generate_data(ui_request: pb.UiRequest):
    if ui_request.HasField("init"):
        runtime.load_module()
        return render_loop()
    if ui_request.HasField("user_action"):
        runtime.session().set_current_action(ui_request.user_action)
        runtime.session().set_current_state(ui_request.user_action.state)
        runtime.load_module()
        runtime.session().execute_current_action()
        return render_loop()
    else:
        raise Exception(f"Unknown request type: {ui_request}")


@app.route("/ui")
def ui_stream():
    runtime.reset_session()

    param = request.args.get("request", default=None)
    ui_request = pb.UiRequest(init=pb.InitRequest())
    if param is not None:
        ui_request = pb.UiRequest()
        ui_request.ParseFromString(base64.b64decode(param))

    return Response(generate_data(ui_request), content_type="text/event-stream")


port = int(os.environ.get("PORT", 8080))
