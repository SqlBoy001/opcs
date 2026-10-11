import { useCurrentFrame, useVideoConfig } from "remotion";
import content from "./content.json";
import { Enter, headline, palette, Picture, SceneShell } from "./visuals";
export function Failure() {
  const v = content.scenes[1].visual;
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shackles = f / fps > v.detailAtSeconds!;
  return (
    <SceneShell scene={content.scenes[1]}>
      <Enter>
        <h1 style={{ ...headline, whiteSpace: "pre-line" }}>{v.heading}</h1>
      </Enter>
      <Enter
        delay={0.12}
        style={{
          position: "absolute",
          top: 285,
          width: "100%",
          height: 740,
          display: "flex",
          gap: 22,
        }}
      >
        <div style={{ width: "50%", position: "relative", overflow: "hidden" }}>
          <Picture
            file={v.beforeImage!}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
              background: "#EAE6DE",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: 0,
              bottom: 0,
              width: "100%",
              background: palette.ink,
              color: palette.paper,
              padding: 18,
              fontSize: 38,
              textAlign: "center",
            }}
          >
            {v.beforeLabel}
          </div>
        </div>
        <div style={{ width: "50%", position: "relative", overflow: "hidden" }}>
          <Picture
            file={shackles ? v.detailImage! : v.afterImage!}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
              background: "#EAE6DE",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: 0,
              bottom: 0,
              width: "100%",
              background: palette.accent,
              color: palette.paper,
              padding: 18,
              fontSize: 38,
              textAlign: "center",
            }}
          >
            {shackles ? v.detailLabel : v.afterLabel}
          </div>
        </div>
      </Enter>
      <div
        style={{
          position: "absolute",
          top: 1080,
          fontSize: 38,
          color: palette.muted,
        }}
      >
        {v.footer}
      </div>
    </SceneShell>
  );
}
