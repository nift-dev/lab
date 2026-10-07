"""Standalone publication figure, generated from validated shell observations."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def draw_shell_plot(data, output):
    by={j['id']:j['summary'] for j in data['jobs']}
    names=('bash','zsh','fish','nu','nift')
    plt.rcParams.update({'font.family':['DejaVu Sans Mono','monospace'],'font.size':11,'svg.hashsalt':'nift-october-2026','svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(9,3.5),dpi=100)
    bg,ink,muted,line,accent,median='#1b1420','#f4edf6','#c8b5ce','#49314d','#ed85dc','#c5f777'
    fig.set_facecolor(bg);ax.set_facecolor(bg)
    for y,name in enumerate(names):
        v=by[name+'/bare/interactive']
        ax.hlines(y,v['min_ms'],v['max_ms'],color=accent,linewidth=2)
        ax.scatter(v['median_ms'],y,color=median,marker='o',s=42,zorder=3)
        ax.scatter(v['p95_ms'],y,color=accent,marker='D',s=30,zorder=3)
    ax.set_yticks(range(len(names)),names);ax.invert_yaxis()
    ax.set_xlim(0,max(by[n+'/bare/interactive']['max_ms'] for n in names)*1.12)
    ax.set_xlabel('First prompt latency (ms)',color=muted)
    ax.tick_params(colors=ink);ax.grid(axis='x',color=line,linewidth=.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():spine.set_color(line)
    handles=[Line2D([],[],color=accent,label='min–max'),Line2D([],[],color=median,marker='o',linestyle='',label='median'),Line2D([],[],color=accent,marker='D',linestyle='',label='p95')]
    ax.legend(handles=handles,loc='upper right',facecolor=bg,edgecolor=line,labelcolor=ink,ncol=3,fontsize=9)
    fig.tight_layout(pad=1.5)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,metadata={'Date':None,'Title':'Bare first-prompt distributions — 100 measured samples per shell'})
    fig.savefig(output.with_suffix('.png'),dpi=160,facecolor=bg)
    plt.close(fig)

def draw_comparison(labels, series, output, title, unit, slug, log=False):
    palettes={'shell':('#1b1420','#f4edf6','#49314d',['#ed85dc','#c5f777','#b59dcc','#f6c477']), 'scripting':('#171e18','#eaf2e8','#354737',['#b4de79','#e4bd72','#d393b6','#84c8b0']), 'website-generator':('#211d17','#f1e9da','#514332',['#e7ac62','#c7b68b','#d18b73','#a9c098'])}
    output=Path(output)
    bg,ink,line,colors=palettes[slug]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'nift-october-2026','svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(9,max(3.8,len(labels)*.65+1.5)))
    fig.set_facecolor(bg);ax.set_facecolor(bg);height=.72/len(series)
    if output.stem=='scaling':
        markers=['o','s','^','D']
        for k,name in enumerate(labels):
            xs=[int(key.split()[0]) for key in series]
            ys=[values[k] for values in series.values()]
            ax.plot(xs,ys,label=name,color=colors[k],marker=markers[k])
        ax.set_xscale('log');ax.set_yscale('log');ax.set_xticks(xs,[f'{v:,}' for v in xs]);ax.set_xlabel('Corpus pages — logarithmic scale',color=ink);ax.set_ylabel('Median build time (s) — logarithmic scale',color=ink)
        ax.set_title(title,color=ink);ax.tick_params(colors=ink);ax.grid(color=line);ax.legend(facecolor=bg,labelcolor=ink)
        fig.tight_layout();fig.savefig(output,metadata={'Date':None,'Title':title});fig.savefig(output.with_suffix('.png'),dpi=160);plt.close(fig);return
    for k,(name,values) in enumerate(series.items()):
        positions=[i-.36+height/2+k*height for i in range(len(labels))]
        ax.barh(positions,values,height=height*.9,color=colors[k%len(colors)],label=name,hatch=['','//','xx','..'][k%4],edgecolor=ink,linewidth=.3)
        for y,v in zip(positions,values):ax.annotate(f'{v:,.3f}' if v<100 else f'{v:,.1f}',(v,y),xytext=(4,0),textcoords='offset points',va='center',color=ink,fontsize=8)
    ax.set_yticks(range(len(labels)),labels);ax.invert_yaxis()
    if log:ax.set_xscale('log');ax.set_xlim(left=min(v for vals in series.values() for v in vals)*.7)
    else:ax.set_xlim(left=0)
    ax.set_xlim(right=max(v for vals in series.values() for v in vals)*(2 if log else 1.23))
    ax.set_xlabel(unit+(' — logarithmic scale' if log else ''),color=ink);ax.set_title(title,color=ink,pad=35)
    ax.tick_params(colors=ink);ax.grid(axis='x',color=line);ax.set_axisbelow(True)
    for spine in ax.spines.values():spine.set_color(line)
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.01),ncol=len(series),facecolor=bg,edgecolor=line,labelcolor=ink,fontsize=8)
    fig.tight_layout();output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,metadata={'Date':None,'Title':title});fig.savefig(output.with_suffix('.png'),dpi=160);plt.close(fig)

def draw_corpus_scaling(runs, supplemental, output):
    """Keep the targeted follow-up on its own axes rather than pooling nodes."""
    bg,ink,line='#211d17','#f1e9da','#514332'
    fig,axes=plt.subplots(1,2,figsize=(12,5.8),gridspec_kw={'width_ratios':[1.5,1]})
    fig.set_facecolor(bg);colors=['#e7ac62','#c7b68b','#d18b73','#a9c098','#e4ca78','#c5a5c3','#f2dfb2']
    xs=[r['pages'] for r in runs];by=[{j['id']:j['summary'] for j in r['jobs']} for r in runs]
    specs=[(n+' full',n+'/application-cold') for n in ('Nift','Hugo','Astro','VitePress')]+[('Nift incremental '+case,'Nift/incremental/'+case) for case in ('no-op','one-page','shared-template')]
    for k,(label,key) in enumerate(specs):
        axes[0].plot(xs,[d[key]['median_ms']/1000 for d in by],label=label,color=colors[k],marker=['o','s','^','D','v','P','X'][k],linestyle='-' if k<4 else '--')
    sb={j['id']:j['summary'] for j in supplemental['jobs']}
    for key,label,color,marker,style in [('fresh-full','Fresh full reference','#e7ac62','o','-'),('targeted-one-page','Explicit target: page-1','#e4ca78','X','--')]:
        axes[1].plot(xs,[sb[f'Nift/{n}/{key}']['median_ms']/1000 for n in xs],label=label,color=color,marker=marker,linestyle=style)
    for ax,title in zip(axes,('Original campaign: full + incremental','Separate follow-up node: explicit target')):
        ax.set_facecolor(bg);ax.set_xscale('log');ax.set_yscale('log');ax.set_xticks(xs,[f'{n:,}' for n in xs]);ax.tick_params(colors=ink);ax.grid(color=line);ax.set_xlabel('Corpus pages (log scale)',color=ink);ax.set_ylabel('Median seconds (log scale)',color=ink);ax.set_title(title,color=ink,fontsize=11)
        for spine in ax.spines.values():spine.set_color(line)
        ax.legend(loc='upper left',bbox_to_anchor=(0,-.2),facecolor=bg,edgecolor=line,labelcolor=ink,fontsize=8,ncol=2 if ax is axes[0] else 1)
    fig.subplots_adjust(bottom=.34,wspace=.3,top=.9);output=Path(output)
    fig.savefig(output,metadata={'Date':None,'Title':'Corpus scaling: original full and incremental builds; separate targeted follow-up'});fig.savefig(output.with_suffix('.png'),dpi=160);plt.close(fig)
