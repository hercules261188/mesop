import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ButtonComponent as ButtonComponentProto } from "optic/optic/components/button/button_ts_proto_pb/optic/components/button/button_pb";
import { ChannelService } from "../../../web/src/services/channel_service";
import { MatButtonModule } from "@angular/material/button";

@Component({
  selector: "app-button",
  templateUrl: "button.html",
  standalone: true,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input() data!: pb.ComponentData;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  getConfig(): ButtonComponentProto {
    return ButtonComponentProto.deserializeBinary(
      this.data.getValue() as Uint8Array,
    );
  }

  handleClick(event: any) {
    const userAction = new pb.UserAction();
    userAction.setClick(new pb.Click());
    userAction.setHandlerId(this.getConfig().getOnClickHandlerId()!);
    this.channelService.dispatch(userAction);
  }
}
