import type { CSSProperties } from 'react';
import { AbsoluteFill, Sequence, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { Audio, Video } from '@remotion/media';
import type { Caption } from '@remotion/captions';
import data from './full-content.json';
import { Enter, Picture, palette } from './visuals';
type Shot = (typeof data.shots)[number];
const lengths: Record<string, number> = { resultA: 4, resultB: 11, resultC: 18, raw: 6, edit: 6 };
const keywords = ['古装','脚镣','六十秒','时代','双排扣','近现代','旧衣服','同步','污痕','磨损','巨型','剪辑','七十五元','核对','付费重做'];
function Photo({ name, style }: { name: string; style?: CSSProperties }) {
  return <Picture file={name+'.jpg'} style={{ width:'100%',height:'100%',objectFit:'contain',background:'#EAE6DE',borderRadius:6,...style }} />;
}
function Clip({ name }: { name: string }) {
  const f=useCurrentFrame(); const {fps}=useVideoConfig(); const hold=f>=lengths[name]*fps;
  return <div style={{width:'100%',height:'100%',position:'relative',background:'#181818'}}>
    {hold ? <Photo name={name+'-end'} style={{background:'#181818'}}/> : <Video src={staticFile('assets/'+name+'.mp4')} muted premountFor={fps} style={{width:'100%',height:'100%'}}/>}
    {hold && <div style={{position:'absolute',bottom:12,right:12,padding:'7px 12px',background:'#171717CE',color:'white',fontSize:24}}>片段结束 · 定格</div>}
  </div>;
}
function Label({children,accent=false}:{children:string;accent?:boolean}) {
 return <div style={{padding:'14px 20px',background:accent?palette.accent:palette.ink,color:palette.paper,fontSize:34,fontWeight:700}}>{children}</div>;
}
function Note({children}:{children:string}) {
 return <div style={{position:'absolute',bottom:10,left:0,right:0,fontSize:31,lineHeight:1.4,color:palette.muted}}>{children}</div>;
}
function PhotoPanel({name,top=290,height=710}:{name:string;top?:number;height?:number}) {
 return <Enter delay={0.08} style={{position:'absolute',top,width:'100%',height}}><Photo name={name}/></Enter>;
}
function Pair({left,right,leftLabel,rightLabel}:{left:string;right:string;leftLabel:string;rightLabel:string}) {
 return <Enter delay={0.1} style={{position:'absolute',top:290,width:'100%',height:775,display:'flex',gap:20}}>
  <div style={{width:'50%',display:'flex',flexDirection:'column'}}><Label>{leftLabel}</Label><Photo name={left} style={{height:700}}/></div>
  <div style={{width:'50%',display:'flex',flexDirection:'column'}}><Label accent>{rightLabel}</Label><Photo name={right} style={{height:700}}/></div>
 </Enter>;
}
function Steps({items,shot}:{items:string[][];shot:Shot}) {
 const {fps}=useVideoConfig();
 return <div style={{position:'absolute',top:310,width:'100%'}}>{items.map(([heading,body],i)=><Enter key={heading} delay={Math.min(i*.35,shot.durationFrames/fps/3)} style={{borderTop:`2px solid ${palette.line}`,padding:'28px 0 30px',display:'flex',gap:35}}>
  <div style={{color:palette.accent,fontSize:45,paddingTop:10}}>0{i+1}</div><div><div style={{fontSize:60,fontWeight:850}}>{heading}</div><div style={{fontSize:34,color:palette.muted,marginTop:15}}>{body}</div></div>
 </Enter>)}</div>;
}
function Evidence({shot}:{shot:Shot}) {
 const k=shot.kind;
 if(['hook_costume','era_sample'].includes(k)) return <><PhotoPanel name="soldier" top={265} height={825}/>
  <div style={{position:'absolute',top:320,left:0}}><Label accent>帽檐</Label></div><div style={{position:'absolute',top:510,right:0}}><Label accent>立领</Label></div><div style={{position:'absolute',top:720,left:0}}><Label accent>双排扣</Label></div><Note>真实失败候选 · 时代不对，细节会暴露</Note></>;
 if(['hook_shackle','shackle'].includes(k)) return <><PhotoPanel name="shackle" top={285} height={780}/><Note>真实失败候选 · 脚镣比例失真</Note></>;
 if(['hook_result','earned_result','closing'].includes(k)) return <><Enter delay={0.08} style={{position:'absolute',top:340,width:'100%',height:600}}><Clip name={k==='hook_result'?'resultA':'resultB'}/></Enter><Enter delay={0.2} style={{position:'absolute',top:1010,fontSize:56,fontWeight:850,color:palette.accent}}>{k==='closing'?'少一次错误传递':'本轮产物：60 秒检查版'}</Enter><Note>{k==='closing'?'少一次付费重做':'搭工作台，再一轮轮返工'}</Note></>;
 if(k==='hook_promise') return <><PhotoPanel name="02-projects-after" height={630}/><div style={{position:'absolute',top:1020,display:'flex',gap:85,fontSize:68,fontWeight:850,color:palette.accent}}><span>流程</span><span>踩坑</span><span>费用</span></div><Note>一个人尝试 AI 漫剧的真实经历</Note></>;
 if(k==='prep') return <><Steps shot={shot} items={[["故事","先讲清冲突"],["人物","时代、身份、处境"],["工具","文字 → 图像 → 视频"],["预算","把重制也考虑进去"]]}/><Note>先把制作需要的输入准备好</Note></>;
 if(k==='tools') return <><Steps shot={shot} items={[["文字模型","整理故事和角色资料"],["图像工具","建立参考，再检查修正"],["视频模型","生成镜头，接入剪辑"]]}/><Note>难点，是让这些环节接起来</Note></>;
 if(['build_before','build_after'].includes(k)) return <><PhotoPanel name={k==='build_before'?'01-projects-before':'02-projects-after'} height={680}/><div style={{position:'absolute',top:1030,fontSize:55,fontWeight:850,color:palette.accent}}>{k==='build_before'?'基于 LocalMiniDrama':'整理创作入口与制作流程'}</div><Note>真实历史界面截图</Note></>;
 if(k==='era_prompt') return <><div style={{position:"absolute",top:290,width:470,height:800}}><Photo name="prompt"/></div><div style={{position:"absolute",top:350,left:530,fontSize:52,lineHeight:1.9}}><div style={{fontSize:34,color:palette.muted}}>提示词摘录</div><div>立领</div><div>双排扣</div><div>帽檐</div><div>裤中缝</div></div><Note>问题出现在提示词润色环节</Note></>;
 if(['era_compare','lesson_replay'].includes(k)) return <><Pair left="soldier" right="correct" leftLabel="重制前" rightLabel="重制首轮"/><Note>{k==='era_compare'?'纠正时代 → 更换参考':'先核对设定，再同步下游；动作不顺，换镜头讲'}</Note></>;
 if(k==='sync') return <><Steps shot={shot} items={[["人物卡已更新","上游设定已经变化"],["分镜仍用旧资料","旧衣服、旧描述继续被引用"],["旧错误继续传递","下游需要重新核对"]]}/><Note>依赖关系示意 · 对应本次旧资料问题</Note></>;
 if(k==='warning') return <><PhotoPanel name="storyboard" height={815}/><Note>同步依赖 → 失效旧引用 → 逐镜核对</Note></>;
 if(k==='state') return <><PhotoPanel name="state" height={800}/><Note>押送状态，要落在画面里</Note></>;
 if(k==='state_detail') return <><Pair left="stateleg" right="statecollar" leftLabel="污痕 / 磨损 / 脚镣" rightLabel="身份 / 木枷"/><Note>本次检查版真实画面 · 不只核对长相</Note></>;
 if(k==='compare') return <><div style={{position:'absolute',top:255,width:'100%',height:460}}><Label>原片 · 原速</Label><div style={{height:390}}><Clip name="raw"/></div></div><div style={{position:'absolute',top:745,width:'100%',height:460}}><Label accent>剪辑版 · 原速</Label><div style={{height:390}}><Clip name="edit"/></div></div></>;
 if(k==='action') return <><div style={{position:'absolute',top:300,width:'100%',height:600}}><Clip name="edit"/></div><div style={{position:'absolute',top:975,fontSize:45}}>接近刀柄 → 切对方反应 → 持刀结果</div><Note>改善来自剪辑 · 连续动作仍有问题</Note></>;
 if(k==='startup') return <><Enter delay={0.1} style={{position:'absolute',top:340,fontSize:47,color:palette.muted}}>2026 年 9 月 · 火山账户</Enter><Enter delay={0.2} style={{position:'absolute',top:445,fontSize:172,letterSpacing:-9,fontWeight:900,color:palette.accent}}>¥274.92</Enter><div style={{position:'absolute',top:770,fontSize:52}}>其中 ¥200 为节省计划</div><Note>账户金额包含套餐费用</Note></>;
 if(k==='episode') return <><Enter delay={0.1} style={{position:'absolute',top:330,fontSize:48,color:palette.muted}}>这版视频的生成与修改</Enter><Enter delay={0.2} style={{position:'absolute',top:470,fontSize:265,letterSpacing:-10,fontWeight:900,color:palette.accent}}><span style={{fontSize:82,letterSpacing:0}}>约 </span>75<span style={{fontSize:82,letterSpacing:0}}> 元</span></Enter><Note>把反复修改，也算进这次尝试</Note></>;
 if(k==='connected') return <><div style={{position:'absolute',top:280,width:'100%',height:400}}><Photo name="03-ai-create"/></div><div style={{position:'absolute',top:715,width:'100%',height:400}}><Photo name="storyboard"/></div><Note>故事 / 人物 → 参考 / 分镜 → 视频 / 剪辑</Note></>;
 throw new Error('Unmapped shot: '+k);
}
function ShotCaptions({shot}:{shot:Shot}) {
 const f=useCurrentFrame();const {fps}=useVideoConfig();const t=(shot.startFrame+f)/fps*1000;
 const cue=shot.cues.find(c=>t>=c.startMs&&t<c.displayEndMs);if(!cue)return null;
 const words:Caption[]=cue.words;let offset=0;
 return <div style={{position:'absolute',left:75,right:75,bottom:188,height:85,display:'flex',alignItems:'center',justifyContent:'center',fontSize:48,fontWeight:650,whiteSpace:'nowrap'}}>{words.map((w,i)=>{
  const at=offset;offset+=w.text.length;const emphasis=keywords.some(k=>{const n=cue.text.indexOf(k);return n>=0&&at>=n&&at<n+k.length;});
  return <span key={i} style={{color:emphasis&&t>=w.startMs?palette.accent:palette.ink,fontWeight:emphasis?900:650}}>{w.text.replace(/[，。；：？！]$/,'')}</span>;
 })}</div>;
}
function FullShot({shot}:{shot:Shot}) {
 const f=useCurrentFrame();
 return <AbsoluteFill style={{fontFamily:'OPC Sans',background:palette.paper,color:palette.ink,overflow:'hidden'}}>
  <div style={{position:'absolute',inset:36,border:`2px solid ${palette.line}`}}/>
  <div style={{position:'absolute',top:96,left:80,right:80,display:'flex',justifyContent:'space-between',fontSize:28,color:palette.muted}}><span>OPC / 实验记录</span><span>{shot.chapter} / 09</span></div>
  <div style={{position:'absolute',top:157,left:80,right:80,height:2,background:palette.line}}/>
  <div style={{position:'absolute',left:80,right:80,top:205,height:1305}}><div style={{fontSize:30,color:palette.accent,marginBottom:28}}>{shot.chapterName}</div><Enter><h1 style={{margin:0,fontSize:72,lineHeight:1.2,fontWeight:850,letterSpacing:-2,whiteSpace:'pre-line'}}>{shot.title}</h1></Enter><Evidence shot={shot}/></div>
  <ShotCaptions shot={shot}/><div style={{position:'absolute',bottom:112,left:80,right:80,height:5,background:palette.line}}><div style={{height:5,background:palette.accent,width:`${(shot.startFrame+f+1)/data.durationFrames*100}%`}}/></div>
 </AbsoluteFill>;
}
// Intentionally one data-driven template; content.json controls every evidence shot.
export function FullFilm() {
 const {fps}=useVideoConfig();
 return <AbsoluteFill>{data.shots.map(shot=><Sequence key={shot.id} name={shot.title.replace('\n',' ')} from={shot.startFrame} durationInFrames={shot.durationFrames} premountFor={fps}><FullShot shot={shot}/></Sequence>)}<Audio src={staticFile('full-voice.wav')} premountFor={fps}/></AbsoluteFill>;
}
