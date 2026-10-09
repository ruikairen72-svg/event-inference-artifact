"""Compatible histories as a visible set-restriction mechanism, not a pipeline."""
from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'data/theory/normative_cells.jsonl';cells=[json.loads(s) for s in source.read_text().splitlines()];assert len(cells)==18
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(17.8/2.54,7.4/2.54));ax.set(xlim=(0,17.8),ylim=(0,7.4));ax.axis('off')
blue='#2563A6';green='#148064';orange='#B65D24';ink='#24354A';muted='#58697B'
def text(x,y,t,**kw):
 kw.setdefault('color',ink);ax.text(x,y,t,va='center',**kw)
def card(x,y,w,h,fc='#F3F6FA',edge='#D9E1EA'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06,rounding_size=.12',facecolor=fc,edgecolor=edge,linewidth=.7))
def chip(x,y,t,color=blue,w=.65):
 card(x-w/2,y-.19,w,.38,'white',color);text(x,y,t,ha='center',fontsize=7,color=color)
# Region hierarchy and concrete input.
text(.2,7.02,'(a)  TARGET CONTRAST',weight='bold',fontsize=7.7)
text(4.72,7.02,'(b)  ENDPOINT ALTERNATIVES',weight='bold',fontsize=7.7)
text(11.12,7.02,'(c)  EVIDENCE SELECTS HISTORIES',weight='bold',fontsize=7.7)
card(.2,1.75,4.05,4.65)
text(.45,5.96,'Avery was reading\na paragraph.',weight='bold',fontsize=7.6)
text(.45,5.25,'Witness: several words\nactually read.',fontsize=7)
text(.45,4.65,'ACTIVITY TARGET  A',color=blue,weight='bold')
text(.45,4.08,'read text\nfrom the paragraph',fontsize=7.7)
text(.45,3.48,'Occurrence: progress ≥ 2',color=muted,fontsize=7)
text(.45,3.03,'BOUNDED TARGET  B',color=green,weight='bold')
text(.45,2.53,'read the entire paragraph',fontsize=7.7)
text(.45,2.15,'Culmination: progress = 4',color=muted,fontsize=7)
# Shared activity and diverging endpoint alternatives at visual center.
card(4.72,1.75,5.93,4.65,'#F8FAFC')
text(5.02,6.0,'Shared activity witness;\nendpoint attainment differs.',fontsize=7.1)
xs=[5.25,6.30,7.35,8.40,9.45]
def path(y,states,plus):
 for j in range(len(states)-1):ax.plot(xs[j:j+2],[y,y],color=blue if j<1 else (green if plus else orange),lw=1.8,zorder=2)
 for j,st in enumerate(states):
  color=orange if st=='S' else (green if st==4 else blue)
  marker='s' if st=='S' else 'o';ax.scatter([xs[j]],[y],s=170,marker=marker,c='white' if st==4 else color,edgecolors=color,linewidths=1.4,zorder=3)
  text(xs[j],y,str(st),ha='center',fontsize=7.5,color=color if st==4 else 'white',weight='bold')
 text(10.05,y,r'$h_+$' if plus else r'$h_-$',ha='center',fontsize=9)
path(4.94,[1,2,'S'],False);path(3.65,[1,2,3,4,'S'],True)
text(7.35,4.48,'stops before endpoint',color=orange,ha='center',fontsize=7)
text(8.4,3.18,'endpoint attained',color=green,ha='center',fontsize=7)
ax.plot([5.25,6.3],[2.63,2.63],color=blue,lw=3)
text(5.77,2.20,'shared witness',ha='center',color=blue,fontsize=7)
text(8.8,2.42,'S = permanent stop',ha='center',color=muted,fontsize=7)
# Set table: label derivation is the highlighted operation.
card(11.12,1.75,6.45,4.65,'#F3F8F6')
text(11.38,5.96,'Evidence',weight='bold');text(13.84,5.96,'Histories',ha='center',weight='bold');text(16.18,5.96,'B',ha='center',color=green,weight='bold');text(17.07,5.96,'A',ha='center',color=blue,weight='bold')
for y,label,hs,b in [(5.08,'Neutral',['minus','plus'],'U'),(3.92,'Endpoint\nattained',['plus'],'E'),(2.76,'Permanent\ncancellation',['minus'],'C')]:
 text(11.38,y,label,fontsize=7.1)
 for j,h in enumerate(hs):chip(13.45+.80*j if len(hs)==2 else 13.84,y,r'$h_-$' if h=='minus' else r'$h_+$',orange if h=='minus' else green)
 color={'U':'#74539A','E':green,'C':orange}[b]
 chip(16.18,y,b,color,w=.50);chip(17.07,y,'E',blue,w=.50)
text(14.34,2.05,'all true → E   |   all false → C   |   mixed → U',ha='center',fontsize=6.9)
# Rendering strip subordinate to semantic mechanism, no implied linguistic identity.
ax.plot([.25,17.55],[1.26,1.26],color='#C9D4DF',lw=.8)
text(.28,.78,'MATCHED PRESENTATIONS',weight='bold',fontsize=7.1)
for x,w,title,detail,color in [(4.82,3.48,'Real','ordinary verb + arguments',blue),(8.58,4.19,'Nonce','defined process + shared root','#76549C'),(13.04,4.47,'Micro','symbolic progress + target rule',green)]:
 card(x,.30,w,.83,'#F6F8FB',color);text(x+.16,.86,title,color=color,weight='bold');text(x+.16,.49,detail,fontsize=7)
fig.subplots_adjust(left=.005,right=.995,top=.99,bottom=.01)
for ext in ['pdf','svg','png']:fig.savefig(ROOT/f'figures/method_schematic.{ext}',dpi=300)
plt.close(fig)
manifest={'purpose':'method mechanism: evidence selects compatible histories; no empirical frequency claim','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cells':18,'example_family':'F141; VP excerpts, schematic histories','reference_visual_rules':'CoRE Figure 1: concrete instance, aligned relationship table, distinct levels and direct category labels; no scientific content copied','reference':'https://aclanthology.org/2025.findings-acl.992/','outputs':[f'figures/method_schematic.{e}' for e in ['pdf','svg','png']]}
(ROOT/'.research/figures/method_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'figures/method_schematic_caption.md').write_text('Compatible-history evaluation: two histories share witnessed activity but differ in endpoint attainment. Neutral evidence retains both histories; endpoint and permanent-cancellation evidence retain one, deriving bounded U/E/C with activity E throughout. The reading family illustrates target extent; Real, Nonce and Micro preserve target truth alternatives while differing in rendering. Histories are schematic alternatives, not empirical frequencies.\n')
