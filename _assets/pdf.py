import asyncio,re,sys
from playwright.async_api import async_playwright
h=open('kislev.html',encoding='utf-8').read()
# print variant: A4 single page, light theme forced
h=h.replace('</style>','''
@page{size:A4;margin:0}
html,body{background:#fff}
:root{--paper:#fff;--tint:#fff}
.sheet{max-width:none;width:210mm;height:297mm;overflow:hidden;box-shadow:none;margin:0;
  display:flex;flex-direction:column}
body{font-size:12.6pt;line-height:1.7}
.band{padding:26px 26px 20px}
.vicon{width:96px;height:96px}
.heb{font-size:32px}
.lat{font-size:12px}
.value{margin-top:13px;font-size:12px;padding:6px 16px}
main{padding:22px 26px 6px;flex:1}
p{margin-bottom:12px}
.greet{font-size:12.6pt;margin-bottom:11px}
.sign{margin-top:13px;padding-top:11px}
.sign .n{font-size:12.6pt;margin-top:6px}
.sign .team{font-size:10.2pt}
footer{padding:12px 22px 14px;margin-top:8px}
footer img{height:46px}
footer span{font-size:9pt}
.pdfbtn{display:none!important}
</style>''')
h=h.replace('<div style="padding:0 28px 6px;display:flex;justify-content:flex-start">','<div class="pdfbtn" style="padding:0 28px 6px;display:flex;justify-content:flex-start">')
open('kislev_print.html','w',encoding='utf-8').write(h)

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page()
        await pg.emulate_media(color_scheme='light')
        await pg.goto('file:///home/claude/kislev_print.html')
        await pg.wait_for_timeout(900)
        await pg.pdf(path='/mnt/user-data/outputs/מכתב_כסלו_תשפז.pdf',format='A4',print_background=True,
                     margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
asyncio.run(main())
print('pdf ok')
