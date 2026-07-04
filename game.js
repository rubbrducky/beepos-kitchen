/* =====================================================================
   Beepo's Kitchen — game.js
   Milestone 1 / Batch 1: core interaction rework (PLAN.md §4, §8)
   - overlapping flyers (no shelf lockout)          B#0
   - 9 ingredients, MAX 3, 129-dish catalog         (dishes.js)
   - tap-to-start title + Web Audio unlock          B#2
   - tap-to-feed eating with idle auto-bite         B#1
   - counting stir with progress ring               B#3
   - ingredient boing + per-ingredient sound motif  B#4
   ===================================================================== */

/* ================= ingredients (9) ================= */
const INGREDIENTS = [
  {id:'apple',   svg:'ing-apple',   n:'Apple',       c:'#E84B4B'},
  {id:'banana',  svg:'ing-banana',  n:'Banana',      c:'#F7D64A'},
  {id:'berry',   svg:'ing-berry',   n:'Strawberry',  c:'#F04E6E'},
  {id:'egg',     svg:'ing-egg',     n:'Egg',         c:'#FFF3D0'},
  {id:'choco',   svg:'ing-choco',   n:'Chocolate',   c:'#8A5A3B'},
  {id:'cookie',  svg:'ing-cookie',  n:'Cookie',      c:'#B57A3E'},
  {id:'icecream',svg:'ing-icecream',n:'Ice Cream',   c:'#FBEFF2'},
  {id:'worm',    svg:'ing-worm',    n:'Wiggly Worm', c:'#9CCF52', tag:'yucky'},
  {id:'rainbow', svg:'ing-rainbow', n:'Rainbow',     c:'#B78BE8', tag:'magic'},
];
const ING_BY_ID = Object.fromEntries(INGREDIENTS.map(i=>[i.id,i]));

const MAX_ITEMS = 3, BITES = 5;

/* Bespoke SVG looks for combos that have them (key = sorted ids joined by +).
   Every other combo gets a generated bowl tinted from its ingredients.
   All of this is placeholder art until the reskin (PLAN.md §3.6). */
const DISH_LOOKS = {
  'banana+icecream': [['dish-split']],
  'berry+icecream':  [['dish-sundae']],
  'choco+icecream':  [['dish-cone','#8A5A3B']],
  'cookie+icecream': [['dish-icesand']],
  'apple+cookie':    [['dish-pie']],
  'berry+choco':     [['dish-cake']],
  'banana+choco':    [['dish-pops']],
  'choco+cookie':    [['dish-donut']],
  'banana+egg':      [['dish-pancakes']],
  'apple+banana':    [['dish-smoothie','#FFD94A']],
  'banana+berry':    [['dish-smoothie','#F8A8C8']],
  'apple+berry':     [['dish-bowl','#F2545B'],['top-cream']],
  'choco+egg':       [['dish-bday']],
  'cookie+egg':      [['dish-burger']],
  'cookie+worm':     [['dish-burger'],['top-worm']],
  'banana+worm':     [['dish-taco']],
  'apple+banana+berry': [['dish-bowl','#FFF1C9'],['top-fruit']],
  'apple':    [['dish-bowl','#F6B092']],
  'banana':   [['dish-bowl','#FFE08A']],
  'berry':    [['dish-jar']],
  'egg':      [['dish-custard']],
  'choco':    [['dish-bowl','#8A5A3B'],['top-cream']],
  'cookie':   [['dish-cookiemush']],
  'icecream': [['dish-bowl','#FBD9E8'],['top-cream']],
  'worm':     [['dish-bowl','#FFE08A'],['top-noodles'],['top-worm']],
  'rainbow':  [['dish-bowl','#B78BE8'],['top-sparkles']],
};

/* ================= sound ================= */
let muted = false, actx;
function unlockAudio(){ try{
  actx = actx || new (window.AudioContext||window.webkitAudioContext)();
  if(actx.state==='suspended') actx.resume();
}catch(e){} }
function beep(fn){ if(muted) return; try{
  unlockAudio();
  fn(actx);
}catch(e){} }
function tone(a, type, f1, f2, t0, dur, vol=0.18){
  const o=a.createOscillator(), g=a.createGain();
  o.type=type; o.frequency.setValueAtTime(f1, a.currentTime+t0);
  o.frequency.exponentialRampToValueAtTime(Math.max(f2,1), a.currentTime+t0+dur);
  g.gain.setValueAtTime(vol, a.currentTime+t0);
  g.gain.exponentialRampToValueAtTime(0.001, a.currentTime+t0+dur);
  o.connect(g); g.connect(a.destination);
  o.start(a.currentTime+t0); o.stop(a.currentTime+t0+dur+0.05);
}
const sPop    = ()=>beep(a=>tone(a,'sine',300,760,0,.16,.2));
const sPlop   = ()=>beep(a=>tone(a,'sine',500,160,0,.2,.2));
const sWhoosh = ()=>beep(a=>{tone(a,'triangle',220,420,0,.25,.13); tone(a,'triangle',260,480,.08,.25,.11);});
const sDing   = ()=>beep(a=>{tone(a,'sine',880,880,0,.35,.15); tone(a,'sine',1320,1320,.03,.4,.09);});
const sChime  = ()=>beep(a=>{[659,880,1319].forEach((f,i)=>tone(a,'sine',f,f,i*.12,.4,.12));});
const sTada   = ()=>beep(a=>{[523,659,784,1047].forEach((f,i)=>tone(a,'triangle',f,f,i*.14,.32,.15));});
const sPeeyew = ()=>beep(a=>{tone(a,'sawtooth',300,150,0,.4,.09); tone(a,'sawtooth',220,90,.35,.55,.09);});
const sSparkle= ()=>beep(a=>{[1047,1319,1568,2093].forEach((f,i)=>tone(a,'sine',f,f,i*.1,.25,.11));});
const sBurp   = ()=>beep(a=>tone(a,'square',140,70,0,.3,.09));
const sSizzle = ()=>beep(a=>{for(let i=0;i<8;i++)tone(a,'triangle',700+Math.random()*600,300,i*.09,.1,.05);});
const sLift   = ()=>beep(a=>{tone(a,'sine',240,900,0,1.7,.09); tone(a,'triangle',480,1800,.25,1.5,.05);});
const sChomp  = ()=>beep(a=>{tone(a,'square',170,70,0,.09,.11); tone(a,'triangle',420,180,.01,.07,.07);});
const sGulp   = ()=>beep(a=>tone(a,'sine',420,110,0,.28,.16));
const sNuhuh  = ()=>beep(a=>{tone(a,'triangle',330,320,0,.15,.15); tone(a,'triangle',262,250,.2,.2,.15);});
const sPluck  = ()=>beep(a=>tone(a,'sine',250,720,0,.18,.18));
const sBoing  = ()=>beep(a=>{tone(a,'sine',180,420,0,.14,.16); tone(a,'sine',420,240,.14,.16,.14);});

/* haptic taps where supported (B#10) — no-op on iOS Safari, works wrapped/Android */
function buzz(p){ try{ navigator.vibrate && navigator.vibrate(p); }catch(e){} }

/* Per-ingredient motifs (B#4) — PLAN.md §4 table */
const MOTIFS = {
  apple:    a=>{tone(a,'sine',660,660,0,.12,.16); tone(a,'sine',880,880,.13,.2,.16);},
  banana:   a=>tone(a,'sine',700,220,0,.3,.16),
  berry:    a=>{[900,1100,1300].forEach((f,i)=>tone(a,'sine',f,f,i*.07,.12,.13));},
  egg:      a=>{tone(a,'sine',520,470,0,.07,.16); tone(a,'sine',300,280,.08,.08,.1);},
  choco:    a=>tone(a,'triangle',330,290,0,.35,.15),
  cookie:   a=>{tone(a,'square',400,380,0,.06,.11); tone(a,'square',340,320,.1,.06,.11);},
  icecream: a=>tone(a,'sine',500,1200,0,.28,.14),
  worm:     a=>{tone(a,'triangle',300,430,0,.15,.14); tone(a,'triangle',430,260,.16,.2,.14);},
  rainbow:  a=>{[523,659,784,1047].forEach((f,i)=>tone(a,'sine',f,f,i*.08,.2,.12));},
};

/* Voice hook (PLAN.md §6.1/§9): VO deferred — clips drop in later as a pure
   asset add. Callers fall back to tones whenever no clip exists. */
const VOICE_CLIPS = {}; /* e.g. VOICE_CLIPS['ing-apple'] = new Audio('assets/vo/apple.mp3') */
function playVoice(id){
  const c = VOICE_CLIPS[id];
  if(!c || muted) return false;
  try{ c.currentTime = 0; c.play(); }catch(e){ return false; }
  return true;
}
function playMotif(id){
  if(playVoice('ing-'+id)) return;
  beep(a=>MOTIFS[id] && MOTIFS[id](a));
}

/* ================= procedural music loop (B#7) =================
   No audio files: a gentle ~92bpm pentatonic wander over soft triangle bass.
   Slightly randomized each bar so it never turns into an earworm. */
let musicOn = true, musicTimer = null, musicGain = null, musicBar = 0;
try{ musicOn = localStorage.getItem('bk-music')!=='0'; }catch(e){}

const M_SCALE = [262, 294, 330, 392, 440, 523, 587, 659]; /* C-pentatonic-ish */
const M_BASS  = [131, 98, 110, 147];                      /* C2 G1 A1 D2-ish walk */
const M_BEAT  = 60/92;

function mNote(f, t0, dur, type='sine', vol=.05){
  const o=actx.createOscillator(), g=actx.createGain();
  o.type=type; o.frequency.value=f;
  g.gain.setValueAtTime(0.0001, actx.currentTime+t0);
  g.gain.linearRampToValueAtTime(vol, actx.currentTime+t0+.04);
  g.gain.exponentialRampToValueAtTime(.001, actx.currentTime+t0+dur);
  o.connect(g); g.connect(musicGain);
  o.start(actx.currentTime+t0); o.stop(actx.currentTime+t0+dur+.05);
}
function playBar(){
  if(muted || !musicOn) return;
  const bass=M_BASS[musicBar%4];
  mNote(bass, 0, M_BEAT*3.6, 'triangle', .045);
  mNote(bass*1.5, M_BEAT*2, M_BEAT*1.7, 'triangle', .028);
  for(let i=0;i<4;i++){
    if(Math.random()<.75)
      mNote(pick(M_SCALE), i*M_BEAT + (Math.random()<.3 ? M_BEAT/2 : 0), M_BEAT*.9, 'sine', .05);
  }
  if(musicBar%2===1) mNote(pick(M_SCALE)*2, M_BEAT*3, M_BEAT*.8, 'sine', .022);
  musicBar++;
}
function startMusic(){
  if(musicTimer || !musicOn || muted) return;
  unlockAudio();
  if(!actx) return;
  if(actx.state!=='running'){                 /* resume is async: retry once ready */
    try{ actx.resume().then(()=>setTimeout(startMusic,60)); }catch(e){}
    return;
  }
  if(!musicGain){ musicGain=actx.createGain(); musicGain.gain.value=.55; musicGain.connect(actx.destination); }
  playBar();
  musicTimer=setInterval(playBar, M_BEAT*4*1000);
}
function stopMusic(){ clearInterval(musicTimer); musicTimer=null; }
document.addEventListener('visibilitychange', ()=>{ document.hidden ? stopMusic() : startMusic(); });

/* ================= state & elements ================= */
let potItems = [], cooking = false;
const $ = id => document.getElementById(id);
const shelf=$('shelf'), soupItems=$('soupItems'), soupEl=$('soupEllipse'),
      potWrap=$('potWrap'), potSpoon=$('potSpoon'), cookFlame=$('cookFlame'),
      beepo=$('beepo'), bubbleTalk=$('bubbleTalk'),
      overlay=$('overlay'), dishName=$('dishName'), reaction=$('reaction'),
      dishBig=$('dishBig'), dishIngs=$('dishIngs'), plateWrap=$('plateWrap');

function iconSVG(id, size, color){
  return `<svg class="icon" viewBox="0 0 100 100" width="${size}" height="${size}"${color?` style="color:${color}"`:''}><use href="#${id}"/></svg>`;
}

/* build shelf */
INGREDIENTS.forEach(item=>{
  const b=document.createElement('button');
  b.className='ing';
  b.innerHTML=iconSVG(item.svg,80);           /* icon-only: the food IS the label */
  b.setAttribute('aria-label', item.n);
  /* pointerdown, not click: fires instantly for EVERY finger — iOS suppresses
     synthesized clicks during multi-touch, which killed overlapping flyers */
  b.addEventListener('pointerdown',()=>addIngredient(item,b));
  shelf.appendChild(b);
});

/* mute persists across reloads (C#7) */
try{ muted = localStorage.getItem('bk-muted')==='1'; }catch(e){}
const sndIcon = ()=>{ $('muteBtn').innerHTML = iconSVG(muted?'ui-snd-off':'ui-snd',24); };
sndIcon();
$('muteBtn').addEventListener('click',()=>{
  muted=!muted; sndIcon();
  try{ localStorage.setItem('bk-muted', muted?'1':'0'); }catch(e){}
  if(muted) stopMusic(); else startMusic();
});

/* music toggle (persisted) */
$('musicBtn').classList.toggle('off', !musicOn);
$('musicBtn').addEventListener('click',()=>{
  musicOn=!musicOn;
  $('musicBtn').classList.toggle('off', !musicOn);
  try{ localStorage.setItem('bk-music', musicOn?'1':'0'); }catch(e){}
  if(musicOn) startMusic(); else stopMusic();
});

/* ================= guide hand + idle attract (B#5, C#1-2, C#6) =================
   One reusable pointing hand. Every ~8s of no input it points at whatever the
   next tap should be; any interaction hides it and restarts the clock. */
const guideHand = document.createElement('div');
guideHand.id='guideHand'; guideHand.innerHTML=iconSVG('ui-hand',52);
document.body.appendChild(guideHand);
function pointAt(el, dx=0, dy=0){
  const r=el.getBoundingClientRect();
  if(!r.width) return;
  guideHand.style.left=(r.left+r.width/2-27+dx)+'px';
  guideHand.style.top=(r.top+r.height/2+2+dy)+'px';
  guideHand.classList.add('show');
}
function hideHand(){ guideHand.classList.remove('show'); }

let idleTimer, attractN=0;
function armIdle(ms=8000){ clearTimeout(idleTimer); idleTimer=setTimeout(attract, ms); }
function currentTarget(){
  if(!$('startOverlay').classList.contains('gone')) return [$('startBtn'),0,14];
  if(overlay.classList.contains('show')){
    if(!lifted) return [cloche,0,40];
    if(feeding) return null;                               /* eating runs itself */
    if(overlay.classList.contains('revealed')) return [$('againBtn'),0,10];
    return null;
  }
  if(cooking) return null;
  if(potItems.length) return null;                         /* auto-cook is coming */
  const kids=shelf.children;
  return kids.length ? [kids[Math.floor(Math.random()*kids.length)],0,12] : null;
}
function attract(){
  attractN++;
  const t=currentTarget();
  if(t) pointAt(t[0],t[1],t[2]);
  /* Beepo joins in on the main stage */
  if($('startOverlay').classList.contains('gone') && !overlay.classList.contains('show') && !cooking){
    beepo.classList.remove('hop'); void beepo.offsetWidth; beepo.classList.add('hop');
    if(!potItems.length) say(pick(['Feed the pot!','Pick a goodie!','Yummy time!']));
    else say('Cook it!');
    setExp(beepo, attractN%2 ? 'yum' : 'wow', 1400);
  }
  armIdle(8000);
}
document.addEventListener('pointerdown', ()=>{ hideHand(); armIdle(); }, {capture:true});
armIdle();

/* toddler-proofing: no pinch zoom, no long-press menus (iOS Safari) */
document.addEventListener('gesturestart', e=>e.preventDefault());
document.addEventListener('contextmenu', e=>e.preventDefault());

/* ================= Beepo expressions ================= */
const revealBeepo = $('revealBeepo');
revealBeepo.appendChild(document.querySelector('#beepo svg').cloneNode(true));
let expTimer;
function setExp(el, exp, ms){
  el.classList.remove('exp-yum','exp-yuck','exp-wow','exp-eat','exp-refuse','fast');
  if(exp){ void el.offsetWidth; el.classList.add('exp-'+exp); }
  if(el===beepo){
    clearTimeout(expTimer);
    if(ms) expTimer=setTimeout(()=>el.classList.remove('exp-'+exp), ms);
  }
}

/* ================= talk ================= */
let talkTimer;
function say(txt, ms=2200){
  bubbleTalk.textContent=txt; bubbleTalk.classList.add('show');
  clearTimeout(talkTimer);
  talkTimer=setTimeout(()=>bubbleTalk.classList.remove('show'), ms);
}
const ADD_LINES=['Ooooh!','Yum yum!','Into the pot!','More more!','Bloop!','Tasty!','Plip plop!','Good pick!','Hehe!','So fresh!'];
const YUCKY_LINES=['Pee-yew!!','Wiggly!!','Eww hehe!','It tickles!','Squirmy!!','My nose!!'];
const FULL_LINES=['Full pot!','Time to stir!','Stir it!','Ready ready!'];
const EAT_START=['Nom nom nom…','Feed me!','Bite time!','Open wide!'];
const VOR_START=['CHOMP CHOMP!!','GIMME GIMME!!','SO HUNGRY!!'];
const EAT_END=['All gone!','So yummy!','More please?','Happy tummy!'];
const VOR_END=['BUUURP!','WOWIE!','YUM-TASTIC!'];
/* dish-specific one-liners, first keyword hit wins (B#9) */
const DISH_LINES=[
  ['Burger','BURGER TIME!!'],['Rainbow','So sparkly!'],['Worm','It wiggles!!'],['Cake','Party time!'],
  ['Smoothie','Slurrrp!'],['Sundae','Cherry on top!'],['Pancake','Flippy floppy!'],
  ['Cookie','Crunch crunch!'],['Choco','Mmm chocolate!'],['Jam','Sticky sweet!'],
  ['Soup','Slurpy soup!'],['Taco','Crunchy crunch!'],['Pie','Sweetie pie!'],
  ['Egg','Wibbly wobbly!'],['Banana','Go bananas!'],['Berry','Berry nice!'],
];

/* ================= start / title overlay (B#2) ================= */
$('startBeepo').appendChild(document.querySelector('#beepo svg').cloneNode(true));
$('startOverlay').addEventListener('click',()=>{
  unlockAudio();           /* the one guaranteed user gesture — iOS audio unlock */
  sChime();
  setTimeout(startMusic, 900);   /* music fades in after the chime */
  $('startOverlay').classList.add('gone');
  beepo.classList.remove('hop'); void beepo.offsetWidth; beepo.classList.add('hop');
  setTimeout(()=>say('Feed the pot!'), 700);
  armIdle(1800);   /* first-run onboarding: hand points at the shelf right away */
},{once:true});

/* ================= add ingredient (B#0: overlapping flyers) ================= */
function addIngredient(item, btn){
  if(cooking) return;
  /* every tap responds instantly: boing + motif, no shelf lockout */
  btn.classList.remove('boing'); void btn.offsetWidth; btn.classList.add('boing');
  playMotif(item.id); buzz(8);
  const from=btn.getBoundingClientRect(), to=potWrap.getBoundingClientRect();
  const fl=document.createElement('div');
  fl.className='flyer'; fl.innerHTML=iconSVG(item.svg,64);
  fl.style.left=(from.left+from.width/2-32)+'px';
  fl.style.top=(from.top+4)+'px';
  document.body.appendChild(fl);
  const dx=(to.left+to.width/2-32)-(from.left+from.width/2-32);
  const dy=(to.top+14)-(from.top+4);
  fl.animate([
    {transform:'translate(0,0) scale(1) rotate(0deg)'},
    {transform:`translate(${dx*0.5}px, ${dy-120}px) scale(1.1) rotate(160deg)`, offset:.55},
    {transform:`translate(${dx}px, ${dy}px) scale(.55) rotate(330deg)`}
  ],{duration:450, easing:'cubic-bezier(.35,.5,.5,1)'}).onfinish=()=>{
    fl.remove();
    if(cooking) return;                       /* landed mid-cook: quietly vanish */
    if(potItems.length>=MAX_ITEMS) bounceOff(item, to);
    else landInPot(item);
  };
}

/* pot-full is an invitation, never a "no" (C#4): the extra item bounces off
   the rim, the pot wiggles happily, the stir button asks for attention */
function bounceOff(item, to){
  sBoing(); buzz([20,40,20]);
  potWrap.classList.remove('happy'); void potWrap.offsetWidth;
  potWrap.classList.add('happy');
  say(pick(FULL_LINES), 1400);
  const b=document.createElement('div');
  b.className='flyer'; b.innerHTML=iconSVG(item.svg,52);
  b.style.left=(to.left+to.width/2-26)+'px';
  b.style.top=(to.top-6)+'px';
  document.body.appendChild(b);
  /* must read as REJECTED: squash on the rim, then arc clearly AWAY from the
     pot and fall past the counter — never sink into the soup */
  const dx=(Math.random()>.5?1:-1)*(110+Math.random()*70);
  b.animate([
    {transform:'translate(0,-4px) scale(.9,.45) rotate(0deg)', opacity:1},
    {transform:`translate(${dx*.4}px,-84px) scale(.72) rotate(130deg)`, opacity:1, offset:.4},
    {transform:`translate(${dx}px,150px) scale(.6) rotate(320deg)`, opacity:1, offset:.9},
    {transform:`translate(${dx*1.08}px,200px) scale(.55) rotate(360deg)`, opacity:0}
  ],{duration:680, easing:'cubic-bezier(.3,.4,.6,1)'}).onfinish=()=>b.remove();
}

let uidCounter = 0;
const SLOT_X = [0, 49, 99], SLOT_Y = [-16, -9, -16], FLOAT_SIZE = 56;  /* tuned to the 204px pot */
function landInPot(item){
  const used = new Set(potItems.map(e=>e.slot));
  const free = [0,1,2].filter(s=>!used.has(s));
  const slot = free.length ? pick(free) : 0;
  const entry = {...item, uid:++uidCounter, slot};
  potItems.push(entry);
  sPlop();
  const f=document.createElement('div');
  f.className='floatItem'; f.innerHTML=iconSVG(item.svg,FLOAT_SIZE);
  f.style.left=(SLOT_X[slot] + (Math.random()*4-2))+'px';
  f.style.top=(SLOT_Y[slot] + (Math.random()*4-2))+'px';
  f.style.animationDelay=(Math.random()*2)+'s';
  f.dataset.uid = entry.uid;
  soupItems.appendChild(f);
  f.classList.add('land'); buzz(12);
  soupEl.style.fill = blendColors(potItems.map(i=>i.c));
  potWrap.classList.remove('stirring'); void potWrap.offsetWidth;
  potWrap.classList.add('stirring');
  beepo.classList.remove('hop'); void beepo.offsetWidth; beepo.classList.add('hop');
  if(item.tag==='yucky'){ say(pick(YUCKY_LINES)); sPeeyew(); setExp(beepo,'yuck',1700); }
  else if(item.tag==='magic'){ say('Oooh magic!'); sSparkle(); setExp(beepo,'wow',1700); }
  else {
    /* early word learning: sometimes name the ingredient (B#4) */
    say(Math.random()<0.4 ? item.n+'!' : pick(ADD_LINES));
    setExp(beepo,'yum',1300);
  }
  cookFlame.classList.add('lit');    /* flame on = it's cooking, no tap needed */
  potSpoon.classList.add('shown');
  potWrap.classList.add('ready');
  /* AUTO-COOK: fires by itself — soon when full, patient otherwise.
     Every new ingredient resets the timer; a pot tap just cooks sooner. */
  clearTimeout(cookTimer);
  cookTimer=setTimeout(cookNow, potItems.length>=MAX_ITEMS ? 1300 : 4200);
}
let cookTimer;

function resetStir(){
  clearTimeout(cookTimer);
  potWrap.classList.remove('ready');
  potSpoon.classList.remove('shown','swirl');
  cookFlame.classList.remove('lit','flare');
}

/* ================= one-tap cooking (B#3, playtest v3) ================= */
/* the pot IS the cook control: tap it anywhere once ingredients are in */
potWrap.addEventListener('pointerdown', ()=>{
  if(cooking) return;
  if(!potItems.length){                 /* empty pot: a friendly wobble, never a "no" */
    potWrap.classList.remove('wobble'); void potWrap.offsetWidth;
    potWrap.classList.add('wobble');
    sPluck();
    say(pick(['Feed the pot!','Pick a goodie!']));
    return;
  }
  cookNow();
});

function cookNow(){
  if(cooking) return;
  clearTimeout(cookTimer);
  sWhoosh(); buzz(20);
  say(pick(['Cook cook!','Here we go!','Stir-a-whirl!']), 1000);
  potSpoon.classList.remove('swirl'); void potSpoon.offsetWidth;
  potSpoon.classList.add('swirl');
  setTimeout(()=>potSpoon.classList.remove('swirl'), 650);
  sparkleAt(potWrap, 3);
  potWrap.classList.remove('stirring'); void potWrap.offsetWidth;
  potWrap.classList.add('stirring');
  soupItems.classList.remove('swirl'); void soupItems.offsetWidth;
  soupItems.classList.add('swirl');
  cook();
}

function puffSteam(n){
  for(let i=0;i<n;i++){
    const st=document.createElement('div');
    st.className='steam';
    st.style.left=(16+Math.random()*110)+'px';
    st.style.animationDuration=(1.8+Math.random()*.8)+'s';
    st.style.animationDelay=(i*.2)+'s';
    potWrap.appendChild(st);
    setTimeout(()=>st.remove(), 3200);
  }
}

/* magic-happens-here burst */
function sparkleAt(el, n=3){
  const r=el.getBoundingClientRect();
  for(let i=0;i<n;i++){
    const s=document.createElement('div');
    s.className='flyer';
    s.innerHTML=iconSVG('top-sparkles', 34+Math.random()*14);
    s.style.left=(r.left+r.width/2-24+(Math.random()*56-28))+'px';
    s.style.top=(r.top+r.height/2-24+(Math.random()*40-20))+'px';
    document.body.appendChild(s);
    s.animate([
      {transform:'scale(.2)', opacity:0},
      {transform:'scale(1.15) rotate(15deg)', opacity:1, offset:.35},
      {transform:`translateY(-${26+Math.random()*22}px) scale(.5) rotate(40deg)`, opacity:0}
    ],{duration:550+Math.random()*250, easing:'ease-out'}).onfinish=()=>s.remove();
  }
}

function cook(){
  cooking=true;
  clearTimeout(cookTimer);
  hideHand();
  potWrap.classList.remove('ready');
  cookFlame.classList.add('flare');   /* the flame does the cooking */
  sparkleAt(potWrap, 6);
  puffSteam(3);
  potSpoon.classList.remove('shown');
  sSizzle(); say('It’s cooking!!',1800);
  setTimeout(()=>{ sDing(); reveal(); }, 2000);
}

/* ================= find the dish (129-dish catalog) ================= */
function findDish(){
  const ids=[...new Set(potItems.map(i=>i.id))].sort();
  const key=ids.join('+');
  const entry=DISH_CATALOG[key] || {n:'Mystery Mush', v:'yummy'};
  let parts=DISH_LOOKS[key];
  if(parts){ parts=parts.map(p=>[...p]); }
  else{
    parts=[['dish-bowl', blendColors(ids.map(id=>ING_BY_ID[id].c))]];
    if(ids.includes('worm')) parts.push(['top-worm']);
    if(entry.v==='yucky') parts.push(['top-stink']);
    if(entry.v==='magical') parts.push(['top-sparkles']);
  }
  return {name:entry.n, verdict:entry.v, parts, size:ids.length};
}

/* ================= reveal (under a cover!) ================= */
const cloche=$('cloche'), hint=$('hint');
let lifted=false, autoLift=null, anticTimer=null, pendingResult=null;

function reveal(){
  const dish = findDish();
  const tier = dish.verdict==='yucky' ? 'refuse'
             : (dish.verdict==='magical' || dish.size>=2) ? 'vor' : 'ok';
  pendingResult = {verdict:dish.verdict, tier, name:dish.name};

  dishName.textContent = dish.name;
  dishBig.innerHTML = '<svg viewBox="0 0 100 100">'+
    dish.parts.map(p=>`<use href="#${p[0]}"${p[1]?` style="color:${p[1]}"`:''}/>`).join('')+
    '</svg>';
  dishIngs.innerHTML = potItems.map(i=>iconSVG(i.svg,34)).join('');

  let face, word, color;
  if(dish.verdict==='yucky'){ face='ui-face-yuck'; word='PEE-YEW!! WIGGLY!'; color='#C6F08C'; }
  else if(dish.verdict==='magical'){ face='ui-face-wow'; word='MAGICAL! WOW!'; color='#E7D6FF'; }
  else { face='ui-face-yum'; word='YUMMY IN MY TUMMY!'; color='#FFE9A8'; }
  reaction.innerHTML = iconSVG(face,22)+'<span>'+word+'</span>';
  reaction.style.background = color;

  /* reset to covered state */
  lifted=false;
  plateWrap.querySelectorAll('.stinkLine').forEach(x=>x.remove());
  overlay.classList.remove('revealing','revealed');
  cloche.classList.remove('lift');
  hint.classList.remove('gone');
  setExp(revealBeepo, null);
  hideHand();
  overlay.classList.add('show');
  clearTimeout(autoLift); clearTimeout(anticTimer);
  /* anticipation beat (B#8): lean in with an "Ooh?" just before the auto-lift */
  anticTimer = setTimeout(()=>{
    if(lifted) return;
    revealBeepo.classList.remove('lean'); void revealBeepo.offsetWidth;
    revealBeepo.classList.add('lean');
    sayR('Ooh?');
    beep(a=>tone(a,'sine',280,760,0,.6,.1));
  }, 2800);
  autoLift = setTimeout(liftCover, 4000);
}

function liftCover(){
  if(lifted) return;
  lifted = true;
  clearTimeout(autoLift); clearTimeout(anticTimer);
  revealBeepo.classList.remove('lean');
  rBubble.classList.remove('show');
  hideHand();
  hint.classList.add('gone');
  sLift(); buzz(20);
  overlay.classList.add('revealing');
  cloche.classList.add('lift');
  setTimeout(finishReveal, 2100);
}
cloche.addEventListener('pointerdown', liftCover);

function finishReveal(){
  const {verdict, tier, name} = pendingResult || {verdict:'yummy', tier:'ok', name:''};
  overlay.classList.add('revealed');
  /* dish-specific one-liner (B#9) */
  const dl = DISH_LINES.find(d=>name && name.includes(d[0]));
  if(dl) sayR(dl[1]);
  if(verdict==='yucky'){
    setExp(revealBeepo,'yuck');
    sPeeyew();
    [24,80,136,192,248].forEach((x,i)=>{
      const s=document.createElement('div');
      s.className='stinkLine';
      s.innerHTML='<svg width="30" height="42" viewBox="-9 -33 22 38"><use href="#g-stink"/></svg>';
      s.style.left=x+'px'; s.style.top='20px'; s.style.animationDelay=(i*.6)+'s';
      plateWrap.appendChild(s);
    });
    schedule(()=>refuseDish(), 1700);
    return;
  }
  if(verdict==='magical'){
    setExp(revealBeepo,'wow');
    sSparkle(); setTimeout(sTada,500);
    confettiBurst(40); buzz([30,50,30]);
    overlay.classList.remove('shake'); void overlay.offsetWidth;
    overlay.classList.add('shake');
  } else {
    setExp(revealBeepo,'yum');
    sTada();
    confettiBurst(20); buzz(25);
  }
  schedule(()=>beginFeeding(tier), 1300);
}

/* ================= tap-to-feed (B#1) ================= */
const rBubble = $('rBubble');
let eatTimers = [], feeding=false, bitesDone=0, idleFeedTimer;
function schedule(fn, ms){ eatTimers.push(setTimeout(fn, ms)); }
function clearEating(){ eatTimers.forEach(clearTimeout); eatTimers=[]; clearTimeout(idleFeedTimer); }
function sayR(txt){ rBubble.textContent=txt; rBubble.classList.add('show'); }

/* gross-out comedy (B#6): refuse → dramatic faint → giggly recovery.
   Zero fail — it's the best silly outcome. */
function refuseDish(){
  sayR('NO WAY!!');
  setExp(revealBeepo,'refuse');
  sNuhuh(); buzz([40,60,40]);
  plateWrap.classList.add('pushed');
  spawnFlies(3);
  schedule(sNuhuh, 900);
  schedule(()=>{                                   /* dramatic faint */
    revealBeepo.classList.add('faint');
    sayR('Bleh…!');
    beep(a=>tone(a,'triangle',900,180,0,.7,.12));  /* slide-whistle down */
  }, 2000);
  schedule(()=>{                                   /* pop back up, all giggles */
    revealBeepo.classList.remove('faint');
    setExp(revealBeepo,'yum');                     /* joyBounce ×3 */
    sBoing();
    sayR('Hihi! Again?');
    $('againBtn').classList.add('shown');   /* only after the whole gag */
  }, 3500);
  schedule(()=>{ if(overlay.classList.contains('show')) $('againBtn').click(); }, 8200);
}
function spawnFlies(n){
  for(let i=0;i<n;i++){
    const f=document.createElement('div');
    f.className='fly'; f.innerHTML=iconSVG('ui-fly',26);
    f.style.left=(112+i*14)+'px';
    f.style.top=(92+i*16)+'px';
    f.style.animationDelay=(i*-0.7)+'s';
    f.style.animationDuration=(2+i*0.4)+'s';
    plateWrap.appendChild(f);
  }
}

function beginFeeding(tier){
  feeding=true; bitesDone=0;
  overlay.classList.add('eating');
  revealBeepo.classList.add('feeding');
  if(tier==='vor') revealBeepo.classList.add('fast');
  sayR(tier==='vor' ? pick(VOR_START) : pick(EAT_START));
  armAutoBite(900);
}
/* eating runs by itself on a tasty rhythm; taps just add bonus bites */
function armAutoBite(ms){
  clearTimeout(idleFeedTimer);
  idleFeedTimer=setTimeout(bite, ms);
}
function bite(){
  if(!feeding) return;
  bitesDone++;
  sChomp(); buzz(10);
  revealBeepo.classList.remove('bite'); void revealBeepo.offsetWidth;
  revealBeepo.classList.add('bite');
  dishBig.style.transform =
    `translate(-50%,-50%) scale(${Math.max(1-bitesDone*0.19,0.05)}) rotate(${bitesDone%2?-5:5}deg)`;
  crumbs(revealBeepo.classList.contains('fast')?4:2);
  if(bitesDone>=BITES) finishFeeding();
  else armAutoBite(revealBeepo.classList.contains('fast') ? 480 : 1050);
}
function finishFeeding(){
  feeding=false;
  clearTimeout(idleFeedTimer);
  dishBig.style.transform = 'translate(-50%,-50%) scale(0)';
  dishBig.style.opacity = '0';
  sGulp();
  schedule(()=>{
    const fast = revealBeepo.classList.contains('fast');
    revealBeepo.classList.remove('feeding','fast','bite');
    setExp(revealBeepo,'yum');
    sayR(fast ? pick(VOR_END) : pick(EAT_END));
    if(fast){ sBurp(); confettiBurst(12); } else sDing();
    $('againBtn').classList.add('shown');   /* only after the reaction */
  }, 600);
  /* auto-restart: the arrow button just skips this wait */
  schedule(()=>{ if(overlay.classList.contains('show')) $('againBtn').click(); }, 5200);
}
plateWrap.addEventListener('pointerdown', ()=>{ if(feeding) bite(); });

function crumbs(n){
  const colors=['#E0A860','#F2B04A','#FBD9E8','#FFD94A','#F27EB4'];
  for(let i=0;i<n;i++){
    const c=document.createElement('div');
    c.className='crumb';
    c.style.background=pick(colors);
    c.style.left=(130+Math.random()*44)+'px';
    c.style.top=(122+Math.random()*26)+'px';
    plateWrap.appendChild(c);
    const dx=(Math.random()*120-60), dy=-(15+Math.random()*55);
    c.animate([
      {transform:'translate(0,0) scale(1)', opacity:1},
      {transform:`translate(${dx}px,${dy}px) scale(.9)`, opacity:1, offset:.55},
      {transform:`translate(${dx*1.2}px,${dy+62}px) scale(.5)`, opacity:0}
    ],{duration:620+Math.random()*250, easing:'ease-out'}).onfinish=()=>c.remove();
  }
}

/* ================= reset ================= */
$('againBtn').addEventListener('click',()=>{
  sPop(); buzz(8);
  $('againBtn').classList.remove('shown');
  clearTimeout(autoLift);
  clearEating();
  feeding=false; bitesDone=0;
  overlay.classList.remove('show','revealing','revealed','eating');
  cloche.classList.remove('lift');
  hint.classList.remove('gone');
  revealBeepo.classList.remove('feeding','fast','bite','lean','faint');
  setExp(revealBeepo, null);
  rBubble.classList.remove('show');
  plateWrap.classList.remove('pushed');
  plateWrap.querySelectorAll('.crumb, .fly').forEach(x=>x.remove());
  dishBig.style.transform=''; dishBig.style.opacity='';
  potItems=[]; cooking=false; lifted=false;
  soupItems.querySelectorAll('.floatItem').forEach(x=>x.remove());
  soupEl.style.fill='#F2B04A';
  resetStir();
  say('What’s next, chef?');
});

/* ================= helpers ================= */
function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }
function blendColors(hexes){
  let r=0,g=0,b=0;
  hexes.forEach(h=>{ const n=parseInt(h.slice(1),16); r+=n>>16; g+=(n>>8)&255; b+=n&255; });
  const L=hexes.length;
  return `rgb(${Math.round(r/L)},${Math.round(g/L)},${Math.round(b/L)})`;
}
function confettiBurst(n){
  const colors=['#FF6B6B','#FFD93C','#6BCB77','#4D96FF','#E96BC0','#FF9F45'];
  const star='polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)';
  for(let i=0;i<n;i++){
    const c=document.createElement('div');
    c.className='confetti';
    const size=9+Math.random()*8;
    c.style.width=size+'px'; c.style.height=size+'px';
    c.style.left=Math.random()*100+'vw';
    c.style.background=pick(colors);
    const shape=Math.random();
    if(shape<.33) c.style.clipPath=star;
    else c.style.borderRadius = shape<.66 ? '50%' : '3px';
    c.style.setProperty('--dx', (Math.random()*160-80)+'px');
    c.style.animationDuration=(2.2+Math.random()*1.8)+'s';
    c.style.animationDelay=(Math.random()*.6)+'s';
    document.body.appendChild(c);
    setTimeout(()=>c.remove(),5000);
  }
}
