import type { CSSProperties, ReactNode } from "react";
import {
  AbsoluteFill,
  CanvasImage,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import type { Caption } from "@remotion/captions";
import content from "./content.json";
loadFont({
  family: "OPC Sans",
  url: staticFile("fonts/NotoSansSC.ttf"),
  weight: "100 900",
});
export type Scene = (typeof content.scenes)[number];
export const palette = {
  paper: "#F5F1E8",
  ink: "#26231F",
  accent: "#C34A32",
  muted: "#766D62",
  line: "#D9D0C2",
};
export const headline: CSSProperties = {
  fontSize: 88,
  lineHeight: 1.15,
  fontWeight: 850,
  letterSpacing: -3,
  margin: 0,
};
export function Picture({
  file,
  style,
}: {
  file: string;
  style?: CSSProperties;
}) {
  const { fps } = useVideoConfig();
  return (
    <CanvasImage
      src={staticFile("assets/" + file)}
      premountFor={fps}
      style={{ objectFit: "cover", ...style }}
    />
  );
}
export function Enter({
  children,
  delay = 0,
  style,
}: {
  children: ReactNode;
  delay?: number;
  style?: CSSProperties;
}) {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        opacity: interpolate(f, [delay * fps, (delay + 0.25) * fps], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
        translate: `0 ${interpolate(f, [delay * fps, (delay + 0.35) * fps], [28, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) })}px`,
        ...style,
      }}
    >
      {children}
    </div>
  );
}
function Captions({ scene }: { scene: Scene }) {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (f / fps) * 1000;
  const cue = scene.cues.find((c) => t >= c.startMs && t < c.displayEndMs);
  if (!cue) return null;
  const words: Caption[] = cue.words;
  let offset = 0;
  return (
    <div
      data-caption
      style={{
        position: "absolute",
        left: 80,
        right: 80,
        bottom: 205,
        textAlign: "center",
        fontSize: 49,
        lineHeight: 1.45,
        fontWeight: 650,
      }}
    >
      {words.map((w, i) => {
        const at = offset;
        offset += w.text.length;
        const emphasis = scene.keywords.some((k) => {
          const n = cue.text.indexOf(k);
          return n >= 0 && at >= n && at < n + k.length;
        });
        return (
          <span
            key={i}
            style={{
              color: emphasis && t >= w.startMs ? palette.accent : palette.ink,
              fontWeight: emphasis ? 900 : 650,
            }}
          >
            {w.text.replace(/[，。；：]$/, "")}
          </span>
        );
      })}
    </div>
  );
}
export function SceneShell({
  scene,
  children,
}: {
  scene: Scene;
  children: ReactNode;
}) {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        background: palette.paper,
        color: palette.ink,
        fontFamily: "OPC Sans",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 36,
          border: `2px solid ${palette.line}`,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 97,
          left: 80,
          right: 80,
          display: "flex",
          justifyContent: "space-between",
          fontSize: 28,
          letterSpacing: 2,
          color: palette.muted,
        }}
      >
        <span>OPC / 实验记录</span>
        <span>{scene.id} / 04</span>
      </div>
      <div
        style={{
          position: "absolute",
          left: 80,
          right: 80,
          top: 158,
          height: 3,
          background: palette.line,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 80,
          right: 80,
          top: 240,
          bottom: 390,
        }}
      >
        {children}
      </div>
      <Captions scene={scene} />
      <div
        style={{
          position: "absolute",
          left: 80,
          right: 80,
          bottom: 112,
          height: 5,
          background: palette.line,
        }}
      >
        <div
          style={{
            height: 5,
            background: palette.accent,
            width: `${Math.min(100, ((f + 1) / scene.durationFrames) * 100)}%`,
          }}
        />
      </div>
      <Audio src={staticFile(scene.audio)} premountFor={fps} />
    </AbsoluteFill>
  );
}
