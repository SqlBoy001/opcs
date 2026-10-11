import content from "./content.json";
import { Enter, headline, palette, Picture, SceneShell } from "./visuals";
export function Opening() {
  const v = content.scenes[0].visual;
  return (
    <SceneShell scene={content.scenes[0]}>
      <Enter>
        <div style={{ fontSize: 44, color: palette.muted }}>{v.prefix}</div>
        <h1
          style={{
            ...headline,
            fontSize: 210,
            letterSpacing: -12,
            marginTop: 10,
          }}
        >
          {v.number}
          <span style={{ fontSize: 90, letterSpacing: 0 }}>{v.unit}</span>
        </h1>
      </Enter>
      <Enter
        delay={0.12}
        style={{ position: "absolute", top: 390, width: "100%", height: 620 }}
      >
        <Picture
          file={v.image!}
          style={{ width: "100%", height: "100%", borderRadius: 5 }}
        />
      </Enter>
      <Enter
        delay={0.4}
        style={{
          position: "absolute",
          top: 970,
          right: -15,
          rotate: "-4deg",
          background: palette.accent,
          color: palette.paper,
          padding: "25px 38px",
          fontWeight: 850,
          fontSize: 65,
        }}
      >
        {v.stamp}
      </Enter>
    </SceneShell>
  );
}
