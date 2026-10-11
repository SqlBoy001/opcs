import content from "./content.json";
import { Enter, headline, palette, SceneShell } from "./visuals";
export function Takeaway() {
  const v = content.scenes[3].visual;
  return (
    <SceneShell scene={content.scenes[3]}>
      <Enter>
        <div style={{ fontSize: 38, color: palette.muted, marginBottom: 28 }}>
          {v.eyebrow}
        </div>
        <h1 style={{ ...headline, whiteSpace: "pre-line" }}>{v.heading}</h1>
      </Enter>
      <Enter
        delay={v.stepAtSeconds![0]}
        style={{
          position: "absolute",
          top: 490,
          fontSize: 78,
          fontWeight: 850,
        }}
      >
        <span style={{ color: palette.accent }}>01</span> {v.steps![0]}
      </Enter>
      <Enter
        delay={v.stepAtSeconds![1]}
        style={{
          position: "absolute",
          top: 680,
          fontSize: 78,
          fontWeight: 850,
        }}
      >
        <span style={{ color: palette.accent }}>02</span> {v.steps![1]}
      </Enter>
      <Enter
        delay={v.stepAtSeconds![2]}
        style={{
          position: "absolute",
          top: 870,
          fontSize: 78,
          fontWeight: 850,
        }}
      >
        <span style={{ color: palette.accent }}>03</span> {v.steps![2]}
      </Enter>
    </SceneShell>
  );
}
