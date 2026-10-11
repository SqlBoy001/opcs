import { Composition, Folder } from "remotion";
import content from "./content.json";
import { Pilot } from "./Composition";
import { Opening } from "./Opening";
import { Failure } from "./Failure";
import { Cost } from "./Cost";
import { Takeaway } from "./Takeaway";
export const RemotionRoot = () => (
  <>
    <Composition
      id="OPC-Pilot"
      component={Pilot}
      durationInFrames={content.durationFrames}
      fps={30}
      width={1080}
      height={1920}
    />
    <Folder name="Reusable-Scenes">
      <Composition
        id="Opening"
        component={Opening}
        durationInFrames={content.scenes[0].durationFrames}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Failure"
        component={Failure}
        durationInFrames={content.scenes[1].durationFrames}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Cost"
        component={Cost}
        durationInFrames={content.scenes[2].durationFrames}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="Takeaway"
        component={Takeaway}
        durationInFrames={content.scenes[3].durationFrames}
        fps={30}
        width={1080}
        height={1920}
      />
    </Folder>
  </>
);
