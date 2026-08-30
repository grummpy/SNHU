"""CS 508 graph model: representations, traversals, and shortest paths.

Run in an IDE:  python3 cs508_graph_model.py
The text report and any available PNG figures are saved in graph_outputs/.
"""
from collections import deque
from heapq import heappop, heappush
from math import inf
from pathlib import Path

GRAPH_1 = {"name":"Graph 1","directed":False,"vertices":list(range(1,8)),"edges":[(1,2,4),(1,3,2),(2,4,5),(2,5,10),(3,6,3),(4,5,2),(5,6,8),(5,7,6),(6,7,1)]}
GRAPH_2 = {"name":"Graph 2","directed":True,"vertices":list(range(1,6)),"edges":[(1,2,5),(1,3,3),(2,4,2),(3,4,6),(3,5,4),(4,5,7)]}

def adjacency_list(g):
    a={v:[] for v in g["vertices"]}
    for u,v,w in g["edges"]:
        a[u].append((v,w))
        if not g["directed"]: a[v].append((u,w))
    for n in a.values(): n.sort()
    return a

def weighted_matrix(g):
    vs=g["vertices"]; ix={v:i for i,v in enumerate(vs)}
    m=[[inf]*len(vs) for _ in vs]
    for i in range(len(vs)): m[i][i]=0
    for u,v,w in g["edges"]:
        m[ix[u]][ix[v]]=w
        if not g["directed"]: m[ix[v]][ix[u]]=w
    return m

def bfs(a,start=1):
    order=[]; seen={start}; q=deque([start])
    while q:
        u=q.popleft(); order.append(u)
        for v,_ in a[u]:
            if v not in seen: seen.add(v); q.append(v)
    return order

def dfs(a,start=1):
    order=[]; seen=set()
    def visit(u):
        seen.add(u); order.append(u)
        for v,_ in a[u]:
            if v not in seen: visit(v)
    visit(start); return order

def dijkstra(a,start=1):
    dist={v:inf for v in a}; prev={v:None for v in a}; dist[start]=0; q=[(0,start)]
    while q:
        du,u=heappop(q)
        if du!=dist[u]: continue
        for v,w in a[u]:
            nd=du+w
            if nd<dist[v]: dist[v],prev[v]=nd,u; heappush(q,(nd,v))
    return dist,prev

def bellman_ford(g,start=1):
    edges=list(g["edges"])
    if not g["directed"]: edges += [(v,u,w) for u,v,w in g["edges"]]
    dist={v:inf for v in g["vertices"]}; prev={v:None for v in g["vertices"]}; dist[start]=0
    for _ in range(len(g["vertices"])-1):
        changed=False
        for u,v,w in edges:
            if dist[u]!=inf and dist[u]+w<dist[v]: dist[v],prev[v],changed=dist[u]+w,u,True
        if not changed: break
    neg=any(dist[u]!=inf and dist[u]+w<dist[v] for u,v,w in edges)
    return dist,prev,neg

def reconstruct(prev,start,target):
    path=[]; u=target
    while u is not None:
        path.append(u)
        if u==start: return path[::-1]
        u=prev[u]
    return []

def path_extremes(g):
    """Global shortest and longest positive-weight simple paths."""
    a=adjacency_list(g); paths=[]
    for start in g["vertices"]:
        def explore(u,seen,path,total):
            for v,w in a[u]:
                if v not in seen:
                    item=(total+w,path+[v]); paths.append(item)
                    explore(v,seen|{v},path+[v],total+w)
        explore(start,{start},[start],0)
    # Several paths may tie. The paper needs one valid example, so ties are
    # resolved deterministically by the lexicographically smallest path.
    low_weight=min(x[0] for x in paths); high_weight=max(x[0] for x in paths)
    shortest=min((x for x in paths if x[0]==low_weight),key=lambda x:x[1])
    longest=min((x for x in paths if x[0]==high_weight),key=lambda x:x[1])
    return shortest,longest

def fmt(x): return "INF" if x==inf else str(int(x) if float(x).is_integer() else x)
def arrows(path): return " -> ".join(map(str,path))

def report(g):
    a=adjacency_list(g); m=weighted_matrix(g); dd,dp=dijkstra(a); bd,bp,neg=bellman_ford(g); shortest,longest=path_extremes(g)
    assert dd==bd
    lines=["="*68,f'{g["name"]} ({"directed" if g["directed"] else "undirected"})',"="*68,"Adjacency list:"]
    for u in g["vertices"]:
        neighbors=", ".join(f"({v}, weight={fmt(w)})" for v,w in a[u]) or "no outgoing edges"
        lines.append(f"  {u}: {neighbors}")
    lines += ["","Weighted adjacency matrix (INF = no direct edge):","       "+"".join(f"{v:>6}" for v in g["vertices"])]
    lines += [f"  {u:>3}  "+"".join(f"{fmt(x):>6}" for x in row) for u,row in zip(g["vertices"],m)]
    lines += ["",f"BFS order from 1: {arrows(bfs(a))}",f"DFS order from 1: {arrows(dfs(a))}",
              f"Global shortest simple path: {arrows(shortest[1])}; weight={fmt(shortest[0])}",
              f"Global longest simple path: {arrows(longest[1])}; weight={fmt(longest[0])}","","Dijkstra results from vertex 1:"]
    lines += [f"  1 to {v}: distance={fmt(dd[v])}, path={arrows(reconstruct(dp,1,v))}" for v in g["vertices"]]
    lines += ["","Bellman-Ford results from vertex 1:"]
    lines += [f"  1 to {v}: distance={fmt(bd[v])}, path={arrows(reconstruct(bp,1,v))}" for v in g["vertices"]]
    lines.append(f"  Reachable negative-weight cycle: {'Yes' if neg else 'No'}")
    return "\n".join(lines)

def save_figures(g,out):
    """Save a graph diagram and matrix heatmap; NetworkX is not required."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch
    except ImportError:
        print("Matplotlib is unavailable; calculations still completed and PNGs were skipped."); return
    import math
    out.mkdir(parents=True,exist_ok=True); vs=g["vertices"]; n=len(vs)
    pos={v:(math.cos(math.pi/2-2*math.pi*i/n),math.sin(math.pi/2-2*math.pi*i/n)) for i,v in enumerate(vs)}
    fig,ax=plt.subplots(figsize=(7,6)); ax.set_aspect("equal"); ax.axis("off")
    for u,v,w in g["edges"]:
        x1,y1=pos[u]; x2,y2=pos[v]
        ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>" if g["directed"] else "-",mutation_scale=16,linewidth=1.8,color="#38598b",shrinkA=22,shrinkB=22))
        ax.text((x1+x2)/2,(y1+y2)/2,str(w),fontsize=10,bbox=dict(boxstyle="round,pad=.15",fc="white",ec="none"))
    for v,(x,y) in pos.items():
        ax.scatter([x],[y],s=900,c="#dbeafe",edgecolors="#1e3a5f",linewidths=2,zorder=3); ax.text(x,y,str(v),ha="center",va="center",fontsize=13,weight="bold",zorder=4)
    ax.set_title(f'{g["name"]}: Weighted {"Directed" if g["directed"] else "Undirected"} Graph')
    fig.tight_layout(); fig.savefig(out/f'{g["name"].lower().replace(" ","_")}_diagram.png',dpi=200); plt.close(fig)
    matrix=weighted_matrix(g); display=[[0 if x==inf else x for x in row] for row in matrix]
    fig,ax=plt.subplots(figsize=(7,6)); image=ax.imshow(display,cmap="Blues")
    ax.set_xticks(range(n),vs); ax.set_yticks(range(n),vs); ax.set_xlabel("To vertex"); ax.set_ylabel("From vertex"); ax.set_title(f'{g["name"]}: Weighted Adjacency Matrix')
    peak=max(max(row) for row in display)
    for i,row in enumerate(matrix):
        for j,value in enumerate(row): ax.text(j,i,fmt(value),ha="center",va="center",fontsize=9,color="white" if display[i][j]>peak/2 else "black")
    fig.colorbar(image,ax=ax,label="Direct edge weight"); fig.tight_layout(); fig.savefig(out/f'{g["name"].lower().replace(" ","_")}_matrix.png',dpi=200); plt.close(fig)

def main():
    out=Path(__file__).resolve().parent/"graph_outputs"
    text="\n\n".join(report(g) for g in (GRAPH_1,GRAPH_2))+"\n"
    print(text); out.mkdir(exist_ok=True); (out/"graph_algorithm_results.txt").write_text(text,encoding="utf-8")
    for g in (GRAPH_1,GRAPH_2): save_figures(g,out)
    print(f"\nSaved results and available figures to: {out}")

if __name__=="__main__": main()
