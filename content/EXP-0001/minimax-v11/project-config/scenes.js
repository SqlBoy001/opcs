/* OPC v11 MiniMax. Custom portrait scenes built on adu-motion-video Scene/mk/show/S/setFrame.
   Source: content-source-v09.json. Cues: MiniMax word timestamps from nine continuous paragraphs.
   No template presenter, sample claims or stock evidence. */
window.END=TIMELINE.end;
const THEMES={
 navy:{bg:'#101820',fg:'#F7F8F7',muted:'#A5B4BF',accent:'#6CE1CD',card:'#1D2A35'},
 blue:{bg:'#102C43',fg:'#F7F8F7',muted:'#ABC5DA',accent:'#8FCBFF',card:'#1A3C57'},
 white:{bg:'#F1F4F3',fg:'#122630',muted:'#5F737C',accent:'#16796D',card:'#FFFFFF'},
 red:{bg:'#301D27',fg:'#FFF5F0',muted:'#D6B8BA',accent:'#FFAA88',card:'#482C36'},
 green:{bg:'#103630',fg:'#EFFAF7',muted:'#ACCEC5',accent:'#96E6C2',card:'#1C4A42'},
 amber:{bg:'#332C22',fg:'#FFF8EC',muted:'#D8C9B0',accent:'#F5CC85',card:'#4B4030'}
};
const titles={hook_costume:'古装押送兵\n怎么穿成了这样？',hook_shackle:'衣服改了\n脚镣又大成这样',hook_result:'为了做出这 60 秒',hook_promise:'怎么做？哪里翻车？\n又花了多少钱？',prep:'开工前，先想清楚',tools:'把工具，接成流程',build_before:'从现有项目出发',build_after:'继续搭建工作台',era_sample:'时代错了\n细节会暴露问题',era_prompt:'问题，已经写进提示词',era_compare:'先修时代，再换参考',sync:'人物改了\n分镜却没跟上',warning:'改完，还要同步下游',state:'脸像了，处境却不对',state_detail:'服装之外，还要看状态',shackle:'修好一个问题\n又出现一个新问题',compare:'同一个动作\n换一种镜头讲法',action:'切反应，再接持刀结果',earned_result:'折腾到这里\n留下这版 60 秒',startup:'账户支出，不是本集成本',episode:'能核实的是这部分费用',connected:'从设定，一步步接到成片',lesson_replay:'这一轮留下的经验',closing:'把错误\n拦在下一步之前'};
const chapters={'01':'真实失败开场','02':'开工准备','03':'搭建工作台','04':'服装与时代','05':'资料与依赖','06':'人物处境','07':'动作与剪辑','08':'结果与投入','09':'本次收获'};
const phases={ '01':'navy','02':'white','03':'blue','04':'red','05':'blue','06':'green','07':'amber','08':'navy','09':'green'};
function txt(sc,text,x,y,size=52,color=sc.theme.fg,width=950,weight=600){return mk(sc.el,`<div class="copy" style="width:${width}px;font-size:${size}px;font-weight:${weight};line-height:1.23;color:${color}">${text.replaceAll('\n','<br>')}</div>`,x,y);}
function imageBox(sc,name,x,y,w,h,fit='contain'){
 const e=mk(sc.el,`<img src="assets/${name}.jpg" style="width:100%;height:100%;object-fit:${fit};display:block">`,x,y,{style:`width:${w}px;height:${h}px;border-radius:20px;overflow:hidden;background:${sc.theme.card};box-shadow:0 16px 45px #0003`});return e;
}
function videoBox(sc,key,x,y,w,h,offset=0){
 const e=mk(sc.el,`<img src="sc/${key}/f_0001.jpg" style="width:100%;height:100%;object-fit:contain;display:block">`,x,y,{style:`width:${w}px;height:${h}px;overflow:hidden;border-radius:20px;background:#080F14;box-shadow:0 16px 45px #0003`});
 const hold=mk(sc.el,'<div style="font-size:22px;color:#FFFFFF;background:#17212BDD;padding:5px 9px;border-radius:5px">片段结束 · 定格</div>',x+10,y+h-42);
 e.tick=t=>{setFrame(e.querySelector('img'),seqAt(key,MEDIA[key].n,24,t,sc.s+offset,false));place(hold,{o:t>=sc.s+offset+MEDIA[key].n/24?1:0});};return e;
}
function pill(sc,text,x,y,color=sc.theme.accent){return mk(sc.el,`<div style="padding:13px 23px;border-radius:12px;background:${sc.theme.card};border:1px solid ${color}88;color:${color};font-size:31px;font-weight:600">${text}</div>`,x,y);}
function underline(sc,x,y,w){return mk(sc.el,`<div style="height:6px;width:${w}px;border-radius:9px;background:${sc.theme.accent}"></div>`,x,y);}
function mark(sc,x,y,w,h,label,lx,ly,at){
 const c=mk(sc.el,`<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><ellipse cx="${w/2}" cy="${h/2}" rx="${w/2-5}" ry="${h/2-5}" fill="none" stroke="${sc.theme.accent}" stroke-width="6" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>`,x,y);
 const line=mk(sc.el,`<svg width="1080" height="1920"><path d="M${lx+65} ${ly+45} L${x+w/2} ${y+h/2}" fill="none" stroke="${sc.theme.accent}" stroke-width="2.5"/></svg>`,0,0);
 const l=pill(sc,label,lx,ly);S(at,'marker',.17);
 return t=>{const p=EZ.out(pr(t,at,at+.48));place(c,{o:1});c.querySelector('ellipse').style.strokeDashoffset=1-p;place(line,{o:p*.8});show(l,t,at,{k:'up',d:.4,dist:18});};
}
function init(shot){
 const theme=THEMES[phases[shot.chapter]], sc=new Scene(shot.t0,shot.t1,theme.bg,{trans:shot.chapter==='01'?null:'wipe',td:.36,tc:theme.bg});sc.theme=theme;sc.shot=shot;
 const cap=txt(sc,'一个人的 OPC 实验',58,64,26,theme.muted,700,500);
 const ix=txt(sc,`${shot.chapter} / 09`,875,64,26,theme.muted,145,500);
 const lab=txt(sc,chapters[shot.chapter],60,170,30,theme.accent,950,600);
 const title=txt(sc,titles[shot.kind],54,232,68,theme.fg,970);
 const rail=mk(sc.el,`<div style="height:3px;width:960px;background:${theme.accent}33"><div class="fill" style="height:100%;width:0;background:${theme.accent}"></div></div>`,60,1805);
 const footer=txt(sc,'AI 漫剧制作实录',60,1833,23,theme.muted,960,400);
 const ticks=[];
 sc.update=t=>{[cap,ix,lab,rail,footer].forEach(e=>place(e));rail.querySelector('.fill').style.width=`${100*t/TIMELINE.end}%`;show(title,t,sc.s-.15,{k:'up',d:.4,dist:24});ticks.forEach(f=>f(t));};
 if(shot.chapter!=='01')S(sc.s,'swipe',.12);
 sc.add=(e,at=sc.s,k='up',options={})=>{ticks.push(t=>show(e,t,at,{k,d:.55,...options}));return e;};
 sc.tick=f=>ticks.push(f);
 sc.note=(text,y=1490)=>sc.add(txt(sc,text,60,y,26,theme.muted,960,400),sc.s+.25);
 sc.cue=(i=0)=>shot.cues[Math.min(i,shot.cues.length-1)].t0;
 return sc;
}
for(const shot of TIMELINE.shots){
 const sc=init(shot),k=shot.kind,T=sc.theme, s=sc.s,e=sc.e;
 if(['hook_costume','era_sample'].includes(k)){
  const x=300,y=410,w=480,h=1036;sc.add(imageBox(sc,'soldier',x,y,w,h),'hook_costume'===k?s-.6:s,'mask');
  const cues=k==='hook_costume'?[s+.12,s+.65,s+1.1]:[sc.cue(1),sc.cue(1)+.5,sc.cue(2)];
  [[x+166,y+25,150,103,'帽檐',70,500,cues[0]],[x+165,y+171,125,70,'立领',810,658,cues[1]],[x+170,y+233,120,173,'双排扣',66,860,cues[2]]].forEach(a=>sc.tick(mark(sc,...a)));
  sc.note('真实失败候选 · 原图仅裁切展示');
 }else if(['hook_shackle','shackle'].includes(k)){
  sc.add(imageBox(sc,'shackle',75,450,930,972),s-.15,'mask');
  sc.tick(mark(sc,162,1160,690,245,'脚镣比例失真',180,1070,s+.5));sc.note('真实失败候选 · 修正也可能带来新问题');
 }else if(['hook_result','earned_result','episode','closing'].includes(k)){
  const key=k==='hook_result'?'resultA':k==='episode'?'resultC':'resultB';
  const v=videoBox(sc,key,40,470,1000,680);sc.add(v,s-.25,'mask');sc.tick(t=>v.tick(t));
  if(k==='episode'){
   sc.add(txt(sc,'¥74.92',60,1178,130,T.accent,930),s+.05,'pop');
   sc.add(txt(sc,'9 月 28 日账户视频现金金额',65,1345,36,T.fg),s+.2);
   sc.note('与本集汇总吻合 · 未逐请求归因',1410);
   sc.add(pill(sc,'完整制作成本仍未知',70,1470),sc.cue(Math.max(0,shot.cues.length-2)));
  }else if(k==='closing'){
   sc.add(txt(sc,'少一次错误传递',64,1215,65,T.accent),s+.3);
   sc.add(txt(sc,'少一次付费重做',64,1320,65),s+.85);
   sc.note('下一步：完整听审，再决定投入 · 尚未发布');
  }else{
   sc.add(txt(sc,k==='hook_result'?'搭工作台，再一轮轮返工':'本轮产物：60 秒检查版',65,1240,59,T.accent),s+.1);
   sc.note('真实检查版片段 · 原片音频尚未主观验收');
  }
 }else if(k==='hook_promise'){
  sc.add(imageBox(sc,'02-projects-after',60,470,960,625),s,'mask');
  ['流程','踩坑','费用'].forEach((a,i)=>{sc.add(txt(sc,a,70+i*332,1190,72,T.accent,310),s+i*.25,'pop');sc.add(underline(sc,70+i*332,1290,260),s+i*.25)});
  sc.note('一个人尝试 AI 漫剧的真实经历');
 }else if(k==='prep'){
  sc.add(imageBox(sc,'statecollar',580,470,440,940,'cover'),s,'left');
  [['故事','先讲清冲突'],['人物','时代、身份、处境'],['工具','文字 → 图像 → 视频'],['预算','把重制也考虑进去']].forEach(([a,b],i)=>{
   sc.add(txt(sc,`0${i+1}`,65,485+i*230,31,T.accent,120),s+i*.5);
   sc.add(txt(sc,a,65,530+i*230,66,T.fg,420),s+i*.5,'left');
   sc.add(txt(sc,b,65,620+i*230,28,T.muted,450,400),s+i*.5);
  });sc.note('先把制作需要的输入准备好');
 }else if(k==='tools'){
  [['文字模型','整理故事和角色资料'],['图像工具','建立参考，再检查修正'],['视频模型','生成镜头，接入剪辑']].forEach(([a,b],i)=>{
   const at=sc.cue(Math.min(i,shot.cues.length-1));
   sc.add(txt(sc,`0${i+1}`,60,490+i*285,54,T.accent,150),at);
   sc.add(txt(sc,a,195,480+i*285,68,T.fg,800),at,'left');
   sc.add(txt(sc,b,195,575+i*285,35,T.muted,800,400),at+.15);
   sc.add(underline(sc,195,650+i*285,750),at+.2);S(at,'card',.12);
  });sc.note('难点，是让这些环节接起来');
 }else if(k==='build_before'||k==='build_after'||k==='startup'){
  const asset=k==='build_before'?'01-projects-before':'02-projects-after';
  sc.add(imageBox(sc,asset,45,460,990,700),s,'mask');
  if(k==='startup'){
   sc.add(txt(sc,'9 月账户 ¥274.92',65,1205,78,T.accent),s+.1,'pop');
   sc.add(txt(sc,'其中 ¥200 为节省计划',65,1335,44),s+.3);
   sc.note('2026 年 9 月账单快照 · 不全归本集',1430);
  }else{
   sc.add(txt(sc,k==='build_before'?'基于 LocalMiniDrama':'整理创作入口与制作流程',65,1220,55,T.accent),s+.2);
   sc.add(txt(sc,k==='build_before'?'继续搭建自己的工作台':'流程顺了，画面问题才刚开始',65,1325,42),s+.35);
   sc.note('真实历史界面截图');
  }
 }else if(k==='era_prompt'){
  sc.add(imageBox(sc,'prompt',50,460,500,880),s,'left');
  sc.add(txt(sc,'提示词里\n已混入',605,520,56,T.accent,400),s+.15);
  ['立领','双排扣','帽檐','裤中缝'].forEach((a,i)=>sc.add(txt(sc,a,625,775+i*125,56,T.fg,350),s+.3+i*.18,'left'));
  sc.note('图中文字为当时生成提示词 · 右侧为摘录');
 }else if(k==='era_compare'||k==='lesson_replay'){
  sc.add(imageBox(sc,'soldier',50,490,465,865),s,'left');sc.add(imageBox(sc,'correct',565,490,465,865),s+.25,'right');
  sc.add(pill(sc,'重制前',60,415,'#FFAA88'),s);sc.add(pill(sc,'重制首轮',570,415,'#96E6C2'),s+.25);
  sc.add(txt(sc,k==='era_compare'?'纠正时代 → 更换参考':'先核对设定，再同步下游',60,1410,49,T.accent),s+.65);
  sc.note(k==='era_compare'?'真实前后版本 · 仅对比时代与服制':'动作不顺，也可以换一种镜头讲',1510);
 }else if(k==='sync'){
  ['人物卡已更新','分镜仍用旧资料','旧错误继续传递'].forEach((a,i)=>{
   const yy=500+i*280;sc.add(txt(sc,`0${i+1}`,65,yy,40,T.muted,125),s+i*.32);
   sc.add(txt(sc,a,205,yy-8,64,i===1?'#FFAA88':T.fg,800),s+i*.32,'left');
   if(i<2)sc.add(txt(sc,'↓',205,yy+105,68,T.accent,200),s+.3+i*.32);
  });sc.add(pill(sc,'上游变了，下游也要重新核对',60,1380),sc.cue(2));sc.note('依赖关系示意 · 对应本次旧资料问题');
 }else if(k==='warning'){
  sc.add(imageBox(sc,'storyboard',60,460,960,875),s,'mask');
  sc.add(pill(sc,'同步依赖 → 失效旧引用 → 逐镜核对',65,1390),s+.3);
  sc.note('真实历史截图 · 分镜参考与版本提醒');
 }else if(k==='state'||k==='state_detail'){
  if(k==='state'){
   sc.add(imageBox(sc,'state',50,445,980,930),s,'mask');
   sc.add(pill(sc,'押送状态，要落在画面里',65,1405),s+.5);
  }else{
   sc.add(imageBox(sc,'stateleg',50,450,465,900),s,'left');sc.add(imageBox(sc,'statecollar',565,450,465,900),s+.2,'right');
   sc.add(pill(sc,'污痕 / 磨损 / 脚镣',55,1380),s+.25);sc.add(pill(sc,'人物身份 / 木枷',575,1380),s+.45);
  }sc.note('本次检查版真实画面 · 不只核对长相');
 }else if(k==='compare'){
  const a=videoBox(sc,'raw',60,465,960,440),b=videoBox(sc,'edit',60,1045,960,440);
  sc.add(a,s-.2,'mask');sc.add(b,s-.2,'mask');sc.tick(t=>{a.tick(t);b.tick(t)});
  sc.add(pill(sc,'原片 · 原速',74,411,'#FFAA88'),s-.2);sc.add(pill(sc,'剪辑版 · 原速',74,977),s-.2);sc.note('原速播放 6 秒，随后定格',1515);
  sc.tick(t=>{b.style.opacity=t>=s?1:0;});
 }else if(k==='action'){
  const v=videoBox(sc,'edit',50,470,980,630);sc.add(v,s-.15,'mask');sc.tick(t=>v.tick(t));
  ['接近刀柄','切对方反应','持刀结果'].forEach((a,i)=>{sc.add(txt(sc,`0${i+1}`,60+i*337,1190,31,T.accent,300),s+i*.45);sc.add(txt(sc,a,60+i*337,1250,44,T.fg,315),s+i*.45,'left')});
  sc.add(txt(sc,'改善来自剪辑',60,1390,65,T.accent),sc.cue(1));
  sc.note('前 6 秒原速播放，之后定格供讲解');
 }else if(k==='connected'){
  sc.add(imageBox(sc,'03-ai-create',60,445,960,420),s,'mask');sc.add(imageBox(sc,'storyboard',60,895,960,465),s+.2,'mask');
  ['故事 / 人物','参考 / 分镜','视频 / 剪辑'].forEach((a,i)=>sc.add(pill(sc,a,60+i*332,1405),s+i*.45));sc.note('从上游设定到下游画面，逐步检查',1510);
 }
}
