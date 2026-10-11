import content from "./content.json";
import { Enter, headline, palette, SceneShell } from "./visuals";
export function Cost() {
  const v = content.scenes[2].visual;
  return (
    <SceneShell scene={content.scenes[2]}>
      <Enter>
        <h1 style={{ ...headline, whiteSpace: "pre-line" }}>{v.heading}</h1>
      </Enter>
      <Enter
        delay={0.15}
        style={{
          position: "absolute",
          top: 380,
          fontSize: 48,
          color: palette.muted,
        }}
      >
        {v.scope}
      </Enter>
      <Enter
        delay={0.27}
        style={{
          position: "absolute",
          top: 450,
          display: "flex",
          alignItems: "baseline",
          gap: 22,
        }}
      >
        <span style={{ fontSize: 90 }}>{v.qualifier}</span>
        <span
          style={{
            fontSize: 300,
            fontWeight: 900,
            letterSpacing: -18,
            color: palette.accent,
          }}
        >
          {v.number}
        </span>
        <span style={{ fontSize: 80 }}>{v.unit}</span>
      </Enter>
      <div
        style={{
          position: "absolute",
          top: 920,
          height: 3,
          width: "100%",
          background: palette.ink,
        }}
      />
      <Enter
        delay={0.5}
        style={{ position: "absolute", top: 980, fontSize: 48 }}
      >
        {v.footer}
      </Enter>
    </SceneShell>
  );
}
