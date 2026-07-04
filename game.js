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

const MAX_ITEMS = 3, STIRS_NEEDED = 3, BITES = 5;

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

/* ================= state & elements ================= */
let potItems = [], stirs = 0, cooking = false;
const $ = id => document.getElementById(id);
const shelf=$('shelf'), soupItems=$('soupItems'), soupEl=$('soupEllipse'),
      potWrap=$('potWrap'), stirBtn=$('stirBtn'), ringFill=$('ringFill'),
      beepo=$('beepo'), bubbleTalk=$('bubbleTalk'), counter=$('counter'),
      overlay=$('overlay'), dishName=$('dishName'), reaction=$('reaction'),
      dishBig=$('dishBig'), dishIngs=$('dishIngs'), plateWrap=$('plateWrap'),
      feedHand=$('feedHand');
const RING_LEN = 289; /* 2*pi*46, matches stroke-dasharray in styles.css */

function iconSVG(id, size, color){
  return `<svg class="icon" viewBox="0 0 100 100" width="${size}" height="${size}"${color?` style="color:${color}"`:''}><use href="#${id}"/></svg>`;
}

/* build shelf */
INGREDIENTS.forEach(item=>{
  const b=document.createElement('button');
  b.className='ing';
  b.innerHTML=iconSVG(item.svg,74)+'<small>'+item.n+'</small>';
  b.addEventListener('click',()=>addIngredient(item,b));
  shelf.appendChild(b);
});

$('muteBtn').addEventListener('click',()=>{
  muted=!muted; $('muteBtn').textContent = muted?'🔇':'🔊';
});

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
const ADD_LINES=['Ooooh!','Yum yum!','Into the pot!','More more!','Bloop!','Tasty!'];
const YUCKY_LINES=['Pee-yew!!','Wiggly!!','Eww hehe!','It tickles!'];
const FULL_LINES=['Full pot!','Time to stir!','Stir it!'];

/* ================= start / title overlay (B#2) ================= */
$('startBeepo').appendChild(document.querySelector('#beepo svg').cloneNode(true));
$('startOverlay').addEventListener('click',()=>{
  unlockAudio();           /* the one guaranteed user gesture — iOS audio unlock */
  sChime();
  $('startOverlay').classList.add('gone');
  beepo.classList.remove('hop'); void beepo.offsetWidth; beepo.classList.add('hop');
  setTimeout(()=>say('Feed the pot! 🍎'), 700);
},{once:true});

/* ================= add ingredient (B#0: overlapping flyers) ================= */
function addIngredient(item, btn){
  if(cooking) return;
  /* every tap responds instantly: boing + motif, no shelf lockout */
  btn.classList.remove('boing'); void btn.offsetWidth; btn.classList.add('boing');
  playMotif(item.id);
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
  sBoing();
  potWrap.classList.remove('happy'); void potWrap.offsetWidth;
  potWrap.classList.add('happy');
  say(pick(FULL_LINES), 1400);
  stirBtn.classList.add('nudge');
  const b=document.createElement('div');
  b.className='flyer'; b.innerHTML=iconSVG(item.svg,52);
  b.style.left=(to.left+to.width/2-26)+'px';
  b.style.top=(to.top-6)+'px';
  document.body.appendChild(b);
  const dx=(Math.random()>.5?1:-1)*(70+Math.random()*50);
  b.animate([
    {transform:'translate(0,0) scale(.6) rotate(0deg)', opacity:1},
    {transform:`translate(${dx*.6}px,-80px) scale(.75) rotate(140deg)`, opacity:1, offset:.45},
    {transform:`translate(${dx}px,60px) scale(.5) rotate(300deg)`, opacity:0}
  ],{duration:620, easing:'cubic-bezier(.3,.4,.6,1)'}).onfinish=()=>b.remove();
}

let uidCounter = 0;
const SLOT_X = [4, 47, 90], SLOT_Y = [-8, 5, -8];
function landInPot(item){
  const used = new Set(potItems.map(e=>e.slot));
  const free = [0,1,2].filter(s=>!used.has(s));
  const slot = free.length ? pick(free) : 0;
  const entry = {...item, uid:++uidCounter, slot};
  potItems.push(entry);
  sPlop();
  const f=document.createElement('div');
  f.className='floatItem'; f.innerHTML=iconSVG(item.svg,38);
  f.style.left=(SLOT_X[slot] + (Math.random()*4-2))+'px';
  f.style.top=(SLOT_Y[slot] + (Math.random()*4-2))+'px';
  f.style.animationDelay=(Math.random()*2)+'s';
  f.dataset.uid = entry.uid;
  f.addEventListener('click', ()=>removeFromPot(entry.uid, f));
  soupItems.appendChild(f);
  soupEl.style.fill = blendColors(potItems.map(i=>i.c));
  potWrap.classList.remove('stirring'); void potWrap.offsetWidth;
  potWrap.classList.add('stirring');
  beepo.classList.remove('hop'); void beepo.offsetWidth; beepo.classList.add('hop');
  if(item.tag==='yucky'){ say(pick(YUCKY_LINES)); sPeeyew(); setExp(beepo,'yuck',1700); }
  else if(item.tag==='magic'){ say('✨ Oooh magic! ✨'); sSparkle(); setExp(beepo,'wow',1700); }
  else {
    /* early word learning: sometimes name the ingredient (B#4) */
    say(Math.random()<0.4 ? item.n+'!' : pick(ADD_LINES));
    setExp(beepo,'yum',1300);
  }
  updateCounter();
  stirBtn.style.display='block';
}

function removeFromPot(uid, el){
  if(cooking) return;
  const idx = potItems.findIndex(e=>e.uid===uid);
  if(idx<0) return;
  potItems.splice(idx,1);
  sPluck();
  say('Out you go!');
  el.style.pointerEvents='none';
  el.animate([
    {transform:'translateY(0) scale(1)', opacity:1},
    {transform:'translateY(-58px) scale(1.25) rotate(-16deg)', opacity:1, offset:.55},
    {transform:'translateY(-30px) scale(.3) rotate(-40deg)', opacity:0}
  ],{duration:520, easing:'cubic-bezier(.3,1.2,.5,1)'}).onfinish=()=>el.remove();
  soupEl.style.fill = potItems.length ? blendColors(potItems.map(i=>i.c)) : '#F2B04A';
  updateCounter();
  if(!potItems.length) resetStir();
}

function updateCounter(){
  counter.innerHTML='';
  for(let i=0;i<MAX_ITEMS;i++){
    const d=document.createElement('div');
    d.className='dot'+(i<potItems.length?' full':'');
    counter.appendChild(d);
  }
}

function resetStir(){
  stirs=0;
  ringFill.style.strokeDashoffset = RING_LEN;
  stirBtn.style.display='none';
  stirBtn.classList.remove('nudge');
}

/* ================= counting stir (B#3) ================= */
const COUNT_WORDS = ['One!','Two!','Three!'];
const COUNT_TONES = [523, 659, 784];
stirBtn.addEventListener('click',()=>{
  if(cooking||!potItems.length) return;
  stirs=Math.min(stirs+1, STIRS_NEEDED);
  stirBtn.classList.remove('nudge');
  if(!playVoice('count-'+stirs)){
    const f=COUNT_TONES[stirs-1];
    beep(a=>tone(a,'triangle',f,f,0,.28,.17));
  }
  sWhoosh();
  say(COUNT_WORDS[stirs-1], 900);
  ringFill.style.strokeDashoffset = RING_LEN * (1 - stirs/STIRS_NEEDED);
  potWrap.classList.remove('stirring'); void potWrap.offsetWidth;
  potWrap.classList.add('stirring');
  soupItems.classList.remove('swirl'); void soupItems.offsetWidth;
  soupItems.classList.add('swirl');
  if(stirs>=STIRS_NEEDED) cook();
});

function cook(){
  cooking=true;
  stirBtn.style.display='none';
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
let lifted=false, autoLift=null, pendingResult=null;

function reveal(){
  const dish = findDish();
  const tier = dish.verdict==='yucky' ? 'refuse'
             : (dish.verdict==='magical' || dish.size>=2) ? 'vor' : 'ok';
  pendingResult = {verdict:dish.verdict, tier};

  dishName.textContent = dish.name;
  dishBig.innerHTML = '<svg viewBox="0 0 100 100">'+
    dish.parts.map(p=>`<use href="#${p[0]}"${p[1]?` style="color:${p[1]}"`:''}/>`).join('')+
    '</svg>';
  dishIngs.innerHTML = potItems.map(i=>iconSVG(i.svg,34)).join('');

  let face, word, color;
  if(dish.verdict==='yucky'){ face='🤢'; word='PEE-YEW!! WIGGLY!'; color='#C6F08C'; }
  else if(dish.verdict==='magical'){ face='🤩'; word='MAGICAL! WOW!'; color='#E7D6FF'; }
  else { face='😋'; word='YUMMY IN MY TUMMY!'; color='#FFE9A8'; }
  reaction.textContent = face+' '+word;
  reaction.style.background = color;

  /* reset to covered state */
  lifted=false;
  plateWrap.querySelectorAll('.stinkLine').forEach(x=>x.remove());
  overlay.classList.remove('revealing','revealed');
  cloche.classList.remove('lift');
  hint.classList.remove('gone');
  setExp(revealBeepo, null);
  overlay.classList.add('show');
  clearTimeout(autoLift);
  autoLift = setTimeout(liftCover, 4500);
}

function liftCover(){
  if(lifted) return;
  lifted = true;
  clearTimeout(autoLift);
  hint.classList.add('gone');
  sLift();
  overlay.classList.add('revealing');
  cloche.classList.add('lift');
  setTimeout(finishReveal, 2100);
}
cloche.addEventListener('click', liftCover);

function finishReveal(){
  const {verdict, tier} = pendingResult || {verdict:'yummy', tier:'ok'};
  overlay.classList.add('revealed');
  if(verdict==='yucky'){
    setExp(revealBeepo,'yuck');
    sPeeyew();
    [40,115,190].forEach((x,i)=>{
      const s=document.createElement('div');
      s.className='stinkLine'; s.textContent='💚';
      s.style.left=x+'px'; s.style.top='20px'; s.style.animationDelay=(i*.6)+'s';
      plateWrap.appendChild(s);
    });
    schedule(()=>refuseDish(), 1700);
    return;
  }
  if(verdict==='magical'){
    setExp(revealBeepo,'wow');
    sSparkle(); setTimeout(sTada,500);
    confettiBurst(32);
  } else {
    setExp(revealBeepo,'yum');
    sTada();
    confettiBurst(18);
  }
  schedule(()=>beginFeeding(tier), 1300);
}

/* ================= tap-to-feed (B#1) ================= */
const rBubble = $('rBubble');
let eatTimers = [], feeding=false, bitesDone=0, idleFeedTimer;
function schedule(fn, ms){ eatTimers.push(setTimeout(fn, ms)); }
function clearEating(){ eatTimers.forEach(clearTimeout); eatTimers=[]; clearTimeout(idleFeedTimer); }
function sayR(txt){ rBubble.textContent=txt; rBubble.classList.add('show'); }

function refuseDish(){
  sayR('NO WAY!! 🙅');
  setExp(revealBeepo,'refuse');
  sNuhuh();
  plateWrap.classList.add('pushed');
  schedule(sNuhuh, 900);
}

function beginFeeding(tier){
  feeding=true; bitesDone=0;
  overlay.classList.add('eating');
  revealBeepo.classList.add('feeding');
  if(tier==='vor') revealBeepo.classList.add('fast');
  sayR(tier==='vor' ? 'CHOMP CHOMP!!' : 'Feed me!');
  feedHand.classList.add('show');
  armIdleBite();
}
/* never stalls: an idle toddler still sees Beepo eat, one bite at a time */
function armIdleBite(){
  clearTimeout(idleFeedTimer);
  idleFeedTimer=setTimeout(bite, 2600);
}
function bite(){
  if(!feeding) return;
  bitesDone++;
  feedHand.classList.remove('show');
  sChomp();
  revealBeepo.classList.remove('bite'); void revealBeepo.offsetWidth;
  revealBeepo.classList.add('bite');
  dishBig.style.transform =
    `translate(-50%,-50%) scale(${Math.max(1-bitesDone*0.19,0.05)}) rotate(${bitesDone%2?-5:5}deg)`;
  crumbs(revealBeepo.classList.contains('fast')?4:2);
  if(bitesDone>=BITES) finishFeeding();
  else armIdleBite();
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
    sayR(fast ? 'BUUURP! 😋' : 'All gone! 😋');
    if(fast){ sBurp(); confettiBurst(12); } else sDing();
  }, 600);
}
plateWrap.addEventListener('click', ()=>{ if(feeding) bite(); });

function crumbs(n){
  const colors=['#E0A860','#F2B04A','#FBD9E8','#FFD94A','#F27EB4'];
  for(let i=0;i<n;i++){
    const c=document.createElement('div');
    c.className='crumb';
    c.style.background=pick(colors);
    c.style.left=(112+Math.random()*38)+'px';
    c.style.top=(104+Math.random()*22)+'px';
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
  sPop();
  clearTimeout(autoLift);
  clearEating();
  feeding=false; bitesDone=0;
  overlay.classList.remove('show','revealing','revealed','eating');
  cloche.classList.remove('lift');
  hint.classList.remove('gone');
  revealBeepo.classList.remove('feeding','fast','bite');
  setExp(revealBeepo, null);
  rBubble.classList.remove('show');
  feedHand.classList.remove('show');
  plateWrap.classList.remove('pushed');
  plateWrap.querySelectorAll('.crumb').forEach(x=>x.remove());
  dishBig.style.transform=''; dishBig.style.opacity='';
  potItems=[]; cooking=false; lifted=false;
  soupItems.querySelectorAll('.floatItem').forEach(x=>x.remove());
  soupEl.style.fill='#F2B04A';
  resetStir();
  updateCounter();
  say('What’s next, chef? 👩‍🍳');
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
  for(let i=0;i<n;i++){
    const c=document.createElement('div');
    c.className='confetti';
    c.style.left=Math.random()*100+'vw';
    c.style.background=pick(colors);
    c.style.borderRadius=Math.random()>.5?'50%':'3px';
    c.style.animationDuration=(2.2+Math.random()*1.8)+'s';
    c.style.animationDelay=(Math.random()*.6)+'s';
    document.body.appendChild(c);
    setTimeout(()=>c.remove(),5000);
  }
}

updateCounter();
