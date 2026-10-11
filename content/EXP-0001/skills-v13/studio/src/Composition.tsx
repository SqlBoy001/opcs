import { Series, useVideoConfig } from "remotion";
import content from "./content.json";
import { Opening } from "./Opening";
import { Failure } from "./Failure";
import { Cost } from "./Cost";
import { Takeaway } from "./Takeaway";
export const Pilot = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      <Series.Sequence
        name="开场反差"
        durationInFrames={content.scenes[0].durationFrames}
        premountFor={fps}
      >
        <Opening />
      </Series.Sequence>
      <Series.Sequence
        name="真实错误对比"
        durationInFrames={content.scenes[1].durationFrames}
        premountFor={fps}
      >
        <Failure />
      </Series.Sequence>
      <Series.Sequence
        name="生成修改费用"
        durationInFrames={content.scenes[2].durationFrames}
        premountFor={fps}
      >
        <Cost />
      </Series.Sequence>
      <Series.Sequence
        name="经验总结"
        durationInFrames={content.scenes[3].durationFrames}
        premountFor={fps}
      >
        <Takeaway />
      </Series.Sequence>
    </Series>
  );
};
