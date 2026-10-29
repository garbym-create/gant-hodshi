import json,sys,asyncio,base64
from playwright.async_api import async_playwright

FONTS=open('heebo.css').read()
LOGO=open('logo.b64').read()
ICONS={'shonut':open('ico_shonut.b64').read()}
PASKOL=open('paskol.b64').read()

def shade(hex,f):
    h=hex.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    r,g,b=[int(c+(255-c)*f) for c in (r,g,b)]
    return '#%02X%02X%02X'%(r,g,b)
def dark(hex,f):
    h=hex.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return '#%02X%02X%02X'%tuple(int(c*(1-f)) for c in (r,g,b))

def html(s):
    c=s.get('color','#C87830')
    chips=s.get('chips',[])
    bigh=185 if chips else 290
    t=s['title']
    tsz=78 if len(t)<=16 else (66 if len(t)<=21 else (58 if len(t)<=28 else 50))
    icon=s.get('valicon')
    if s.get('brand')=='paskol': iconhtml=f'<img class="big" src="data:image/png;base64,{PASKOL}">'
    elif icon: iconhtml=f'<img class="big" src="data:image/png;base64,{ICONS[icon]}">'
    else: iconhtml=f'<div class="emo">{s.get("emoji","")}</div>'
    chiphtml=''
    if chips:
        parts=[]
        for i,ch in enumerate(chips):
            if len(chips)==5 and i==3: parts.append('<div class="brk"></div>')
            parts.append(f'<div class="chip">{ch}</div>')
        chiphtml='<div class="chips">'+''.join(parts)+'</div>'
    return f"""<!DOCTYPE html><html dir="rtl"><head><meta charset="utf-8"><style>
{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;font-family:Heebo,sans-serif;background:#F5F1EA;position:relative;overflow:hidden}}
.band{{position:absolute;top:0;left:0;right:0;height:250px;background:{c};overflow:hidden}}
.band .blob{{position:absolute;top:-120px;left:-120px;width:380px;height:380px;border-radius:50%;background:{shade(c,0.09)}}}
.band .kick{{position:absolute;top:62px;right:62px;text-align:right;color:#fff}}
.band .kick .k1{{font-size:34px;font-weight:800;letter-spacing:-.5px}}
.band .kick .k2{{font-size:25px;font-weight:500;margin-top:10px;color:{shade(c,0.72)}}}
.stage{{position:absolute;top:250px;left:0;right:0;bottom:96px;display:flex;flex-direction:column;justify-content:space-evenly;align-items:center;padding:0 64px}}
.card{{width:100%;background:#fff;border-radius:34px;padding:54px 60px 60px;box-shadow:0 16px 46px rgba(90,54,21,.10);text-align:center}}
.ico{{display:flex;justify-content:center;align-items:center;margin-bottom:8px}}
.ico img.big{{height:{bigh}px}}
.emo{{font-size:{int(bigh*0.62)}px;line-height:1}}
h1{{font-size:{tsz}px;font-weight:900;color:#5A3615;line-height:1.14;margin-top:14px}}
.cred{{font-size:29px;font-weight:500;color:#8A7D6E;margin-top:16px}}
.rule{{width:104px;height:7px;border-radius:4px;background:{shade(c,0.38)};margin:30px auto}}
.sub{{font-size:35px;font-weight:500;color:#5C5248;line-height:1.52}}
.chips{{display:flex;flex-wrap:wrap;justify-content:center;gap:22px;width:100%}}
.brk{{flex-basis:100%;height:0}}
.chip{{background:#fff;border:3px solid {shade(c,0.55)};border-radius:20px;padding:20px 32px;font-size:32px;font-weight:700;color:#5A3615;box-shadow:0 5px 16px rgba(90,54,21,.06)}}
.foot{{position:absolute;bottom:0;left:0;right:0;height:96px;border-top:2px solid #E7DFD3;display:flex;align-items:center;justify-content:space-between;padding:0 60px}}
.foot img{{height:62px}}
.foot .mid{{font-size:21px;color:#8A7D6E;font-weight:500}}
.foot .rgt{{font-size:21px;color:#8A7D6E;font-weight:500}}
.foot .rgt b{{color:{dark(c,0.18)};font-weight:800}}
</style></head><body>
<div class="band"><div class="blob"></div><div class="kick"><div class="k1">{s['kick']}</div>{'<div class="k2">'+s['kick2']+'</div>' if s.get('kick2') else ''}</div></div>
<div class="stage">
  <div class="card">
    <div class="ico">{iconhtml}</div>
    <h1>{t}</h1>{'<div class="cred">'+s['cred']+'</div>' if s.get('cred') else ''}<div class="rule"></div><div class="sub">{s['sub']}</div>
  </div>
  {chiphtml}
</div>
<div class="foot">
  <img src="data:image/png;base64,{LOGO}">
  <div class="mid">משרד החינוך | אגף בכיר יסודי | המחלקה לחיים ולחינוך בחברה</div>
  <div class="rgt"><b>תחזי"ת</b> ערכית חברתית תשפ"ז</div>
</div></body></html>"""

async def main():
    specs=json.load(open(sys.argv[1]))
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':1080},device_scale_factor=1)
        for s in specs:
            await pg.set_content(html(s)); await pg.wait_for_timeout(400)
            await pg.screenshot(path=s['out'])
            print(s['out'])
        await b.close()
asyncio.run(main())
