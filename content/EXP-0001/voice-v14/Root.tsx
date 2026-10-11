import { Composition } from 'remotion';
import { FullFilm } from './FullFilm';
import data from './full-content.json';
export const RemotionRoot = () => <Composition id="OPC-Full-F" component={FullFilm} durationInFrames={data.durationFrames} fps={30} width={1080} height={1920} />;
