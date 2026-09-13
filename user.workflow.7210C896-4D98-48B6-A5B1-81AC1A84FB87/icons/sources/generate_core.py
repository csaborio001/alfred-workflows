"""Generate original, simple UI symbols; requires Pillow only when rebuilding."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def create(name,color,kind):
 im=Image.new('RGBA',(256,256));d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,12,244,244),radius=52,fill=color)
 def line(points):d.line(points,fill='white',width=12,joint='curve')
 def box(bounds):d.rounded_rectangle(bounds,radius=8,outline='white',width=10)
 if kind=='users':
  d.ellipse((101,54,155,108),outline='white',width=10);d.arc((71,115,185,219),180,360,fill='white',width=12)
  d.arc((48,66,94,112),65,295,fill='white',width=9);d.arc((31,124,102,202),180,280,fill='white',width=9)
  d.arc((162,66,208,112),245,475,fill='white',width=9);d.arc((154,124,225,202),260,360,fill='white',width=9)
 elif kind in ['posts','pages','forms']:
  box((70,49,186,205))
  for y in [91,125,159]:line([(92,y),(163,y)])
  if kind=='posts':line([(145,188),(202,131)])
  if kind=='forms':
   for y in [86,120,154]:d.rectangle((84,y,95,y+11),fill=color)
 elif kind=='media':
  box((48,63,208,195));d.ellipse((79,86,105,112),fill='white');line([(59,181),(114,127),(144,155),(174,120),(200,147)])
 elif kind=='settings':
  for x,y in [(75,101),(128,153),(181,91)]:
   line([(x,59),(x,197)]);d.ellipse((x-17,y-17,x+17,y+17),fill=color,outline='white',width=9)
 elif kind in ['themes','customize']:
  box((57,57,199,199));line([(63,103),(193,103)]);line([(108,109),(108,193)])
 elif kind=='plugins':
  line([(98,48),(98,93)]);line([(158,48),(158,93)]);box((77,91,179,157));line([(128,158),(128,204)])
 elif kind=='network':
  for b in [(105,46,151,90),(45,162,91,206),(165,162,211,206)]:box(b)
  line([(128,92),(128,129),(68,129),(68,160)]);line([(128,129),(188,129),(188,160)])
 elif kind=='comments':
  box((50,58,206,168));line([(85,167),(85,202),(125,168)])
  for x in [87,128,169]:d.ellipse((x-6,106,x+6,118),fill='white')
 elif kind=='home':
  line([(44,120),(128,52),(212,120)]);line([(69,106),(69,200),(187,200),(187,106)]);box((110,147,146,204))
 elif kind in ['privacy','login']:
  d.arc((90,48,166,136),180,360,fill='white',width=12);box((72,110,184,199));d.ellipse((120,141,136,157),fill='white');line([(128,151),(128,174)])
 elif kind=='updates':
  d.arc((57,57,199,199),35,300,fill='white',width=12);line([(158,44),(173,73),(143,81)])
 elif kind=='health':
  line([(43,132),(82,132),(103,84),(131,177),(151,116),(168,132),(211,132)])
 elif kind in ['import','export','backup']:
  box((57,145,199,202));line([(128,51),(128,153)]);line([(94,119),(128,153),(162,119)])
  if kind=='export': im=im.rotate(180)
 elif kind=='tags':
  line([(58,63),(140,63),(209,133),(133,209),(58,133),(58,63)]);d.ellipse((81,86,99,104),fill='white')
 elif kind=='link':
  d.rounded_rectangle((49,97,144,159),radius=26,outline='white',width=11);d.rounded_rectangle((112,97,207,159),radius=26,outline='white',width=11)
 elif kind=='tools':
  line([(71,189),(177,83)]);d.arc((128,44,209,125),20,280,fill='white',width=14);d.ellipse((60,178,81,199),fill='white')
 else:
  for x in [62,141]:
   for y in [62,141]:box((x,y,x+53,y+53))
 im.resize((128,128),Image.Resampling.LANCZOS).save(ROOT/(name+'.png'))
for name,color in {'users':'#4475D5','posts':'#397EB9','pages':'#5864C7','forms':'#774BBB','media':'#B84D9B','settings':'#64748B','themes':'#9558BC','plugins':'#5967C4','network':'#337E96','comments':'#32938A','home':'#2784A1','privacy':'#428573','login':'#5266B4','updates':'#359971','health':'#D45465','import':'#397FAC','export':'#8464BF','backup':'#B17E35','tags':'#AA743B','link':'#488BA8','tools':'#68788D','dashboard':'#2271B1'}.items():create(name,color,name)
