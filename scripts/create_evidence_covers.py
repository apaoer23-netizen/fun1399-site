#!/usr/bin/env python3
"""Render two editorial diagrams; manual asset step, not a Pages build dependency.
Requires Pillow and a CJK font. Set --font when the default font is unavailable.
"""
from pathlib import Path
import argparse,html
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',default='/root/.local/share/fonts/NotoSansCJKtc-Regular.otf');args=parser.parse_args()
 out=ROOT/'static/images/articles/evidence';out.mkdir(parents=True,exist_ok=True)
 for slug,title,subtitle,cards,note in [
  ('casino-dcard-2026','娛樂城 Dcard 討論整理','閱讀心得之前，先核對這三件事。',[
   ('原文','找得到來源嗎？',['原始網址與發文日期','是否有更新與完整前後文']),
   ('證據','紀錄支持到哪裡？',['區分申請、付款與入帳','單筆經驗不是安全保證']),
   ('關係','推薦關係說清楚？',['留意邀請碼與合作揭露','不因導流就直接判定真假'])], '編輯查核示意圖｜不是論壇截圖或玩家實測紀錄'),
  ('rtp-compare','娛樂城 RTP 比較','先分清楚資料類型，再談比較。',[
   ('理論值','遊戲設計的預期比例',['核對遊戲規則與版本','不是每次遊玩的保證回報']),
   ('觀察值','某批紀錄算出的比例',['總派彩 ÷ 總投注','須交代期間、條件與局數']),
   ('資料限制','百分比不能單獨下結論',['樣本與波動一起看','不等於勝率或平台排名'])], '資料閱讀示意圖｜不是平台排行或實測結果')]:
  im=Image.new('RGB',(1280,672),'#eff4f8');d=ImageDraw.Draw(im);svg=[]
  def rect(box,fill,radius=0):
   d.rounded_rectangle(box,radius=radius,fill=fill);x,y,x2,y2=box;svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{radius}" fill="{fill}"/>')
  def text(pos,value,size,fill):
   font=ImageFont.truetype(args.font,size);d.text(pos,value,font=font,fill=fill,anchor='lt')
   if d.textbbox(pos,value,font=font,anchor='lt')[2]>1230:raise ValueError('Cover text overflow')
   x,y=pos;svg.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK TC, sans-serif" font-size="{size}" dominant-baseline="text-before-edge" fill="{fill}">{html.escape(value)}</text>')
  rect((0,0,1280,672),'#eff4f8');rect((0,0,1280,270),'#132c42')
  text((64,38),'FUN1399 / 編輯查核筆記',22,'#9ed7e7');text((1060,40),'2026 更新版',20,'#e2edf5')
  text((60,102),title,64,'#ffffff');text((64,201),subtitle,28,'#d8e7ef')
  for i,(label,sub,lines) in enumerate(cards):
   x=64+i*390;rect((x,304,x+368,560),'#ffffff',20);rect((x+24,330,x+30,380),'#247c9c',3)
   text((x+48,328),label,36,'#132c42');text((x+24,398),sub,23,'#216b87')
   for j,line in enumerate(lines):text((x+24,449+j*39),line,21,'#475569')
  text((64,611),note,22,'#475569')
  stem=out/f'{slug}-20261015';im.save(stem.with_suffix('.png'),optimize=True)
  stem.with_suffix('.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="672" viewBox="0 0 1280 672" role="img" aria-label="'+title+'">'+''.join(svg)+'</svg>')
  print(stem.name,im.size,stem.with_suffix('.png').stat().st_size,'bytes')
if __name__=='__main__':main()
