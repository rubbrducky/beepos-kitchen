import time, glob, os, sys
import gen_food as g
OUT = r"C:\Users\gusta\ComfyUI\output\beepo_food"
SOCK = "a grubby cream tube sock with a chunky ribbed RED cuff and a red toe, clearly a dirty smelly sock"
TAIL = ", green slime oozing and dripping, little wavy green stink squiggles rising"
V = {
 "sock_t016": f"{SOCK} poking right out of a big round bite-hole in a shiny red apple and waving hello, the sock is the big main subject filling the frame{TAIL}",
 "sock_t034": f"{SOCK} as the big main subject, nestled and tangled in a small nest of fluffy yellow scrambled egg, grinning{TAIL}",
 "sock_t041": f"a plump sesame-seed cheeseburger, and instead of the meat patty {SOCK} flops out the side like a giant tongue, the sock big and obvious{TAIL}",
 "sock_t043": f"a swirly soft-serve ice cream in a cup shrieking in shock because {SOCK} is flopped right on top of the swirl, the sock big and obvious{TAIL}",
}
before={p:set(glob.glob(os.path.join(OUT,p+"_*.png"))) for p in V}
for p,b in V.items():
    g.queue_prompt(g.workflow(g.full_prompt(b), g.stable_seed(p), f"beepo_food/{p}"))
    print("queued",p,flush=True)
done={}; dl=time.time()+240
while len(done)<len(V) and time.time()<dl:
    time.sleep(5)
    for p in V:
        if p in done: continue
        new=set(glob.glob(os.path.join(OUT,p+"_*.png")))-before[p]
        if new: done[p]=sorted(new)[-1]; print("DONE",p,flush=True)
print("landed",len(done),"/",len(V))
