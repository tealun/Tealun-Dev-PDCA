"""Draw the dev-pdca marketplace avatar (512x512 PNG).

Usage: python3 scripts/make_avatar.py assets/dev-pdca-avatar.png
Needs Pillow; uses Inter Display Bold if installed, else DejaVu Sans Bold.
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont
S=2048; out=sys.argv[1]
img=Image.new("RGB",(S,S),"#0F1B2D"); d=ImageDraw.Draw(img)
cx=cy=S/2; R=640; W=150
segs=[("P",180,"#3B82F6"),("D",270,"#10B981"),("C",0,"#F59E0B"),("A",90,"#A78BFA")]
gap=7; head=16
font=ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf" if __import__('os').path.exists("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf") else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",300)
for letter,start,col in segs:
    a0=start+gap; a1=start+90-gap-head
    d.arc([cx-R,cy-R,cx+R,cy+R],a0,a1,fill=col,width=W)
    # arrow head at a1 pointing clockwise
    t=math.radians(a1); tip=math.radians(a1+head)
    rm=R-W/2
    p1=(cx+(R+W*0.35)*math.cos(t),cy+(R+W*0.35)*math.sin(t))
    p2=(cx+(R-W*1.35)*math.cos(t),cy+(R-W*1.35)*math.sin(t))
    p3=(cx+rm*math.cos(tip),cy+rm*math.sin(tip))
    d.polygon([p1,p2,p3],fill=col)
    # letter inside quadrant
    mid=math.radians(start+45); rl=R-W-250
    x,y=cx+rl*math.cos(mid),cy+rl*math.sin(mid)
    d.text((x,y),letter,font=font,fill=col,anchor="mm")
img=img.resize((512,512),Image.LANCZOS)
img.save(out,"PNG",optimize=True)
