#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <limits.h>
#if 0
#define M 1008

struct enode{
	int u, w;
	int w;
};
static int ne, nv;
static struct enode edges[M*M];
int mst_directed(int r){
	int ans;     /* 最小生成树权值   */
	int pre[M]; /* 有边(u, v) pre[v]=u; */
	int in[M];  /*  in[v] = min(w(u, v)) 所以与v相连的边 */
	int id[M]; /* 每个面点属于的圈 */
	int vis[M];
	int nc; /* 圈的数量， 也是新图的顶点数  */
	int u, v, w, i;
	nc = nv;
	while(1){
		for(i=0; i<nv; ++i) in[i] = INT_MAX;
		/* 找最小入度 */
		for(i=0; i<ne; ++i){
			u = edges[i].u; v=edges[i].v; w=edges[i].w;
			if(u!=v && w<in[v]){
				pre[v] = u; in[v] = w;
			}
		}
		/* 有没有入度为0的点，除根外，有的话，则无生成树 */
		for(i=0; i<nv; ++i){
			if(i==r) continue;
			if(in[i]==INT_MAX) return -1;
		}
		/* 找圈 */
		memset(id, -1, sizeof(id));
		memset(vis, -1, sizeof(vis));
		for(nc=0, i=0; i<nv; ++i){
			ans += in[i];
			v = i;
			while(id[v]==-1 && vis[v]!=i && v!=r){
				vis[v]=i;
				v = pre[v];
			}
			if(v!=r && id[v]==-1){
				for(u=prev[v]; u!=v; u=prev[u]) id[u]=nc;
				id[u] = nc++;
			}
		}
		/* 无圈  */
		if(nc==0) break;
		/* 图重构，重新编号 */
		for(u=0; u<nv; ++u){
			if(id[u]==-1) id[u]=nc++;
		}
		/* 更新相应的权值  */
		for(i=0; i<ne; ++i){
			u = edges[i].u; v=edges[i].v; w=edges[i].w;
			edges[i].u = id[u];
			edges[i].v = id[v];
			if(id[u]!=id[v]) edges[i].w -= in[v];
		}
		nv = nc;
		r = id[r];
	}

	return ans;
}
static void solve(void){
	int u, v, c;
	int ans, w, cal;
	int i;
	while(~scanf("%d%d", &nv, &ne)){
		for(i=0; i<ne; ++i){
			scanf("%d%d%d", &u, &v, &w);
			edges[i].u=u; edges[i].v=v; edges[i].w=w;
		}

		if(ans==INT_MAX){
			printf("impossible\n");
		}else{
			printf("%d %d\n", ans, c);
		}
	}
	
}
int main(void){
	freopen("data.dat", "r", stdin);
	solve();
	return 0;
}



/* 下面为正确 的算法 */
/*
本题为不是固定根的最小树形图，我们可以虚拟出一根来，然后在把这个根跟每个点相连，相连的点可以设为无穷大，或者设为所有边和大一点，比如为r，然后就可以利用最小树形图进行计算了，计算出的结果减去r,如果比r还大就可以认为通过这个虚拟节点我们连过原图中两个点，即原图是不连通的，我们就可以认为不存在最小树形图。关于输出最小根也挺简单，在找最小入弧时，如果这条弧的起点是虚拟根，那么这条弧的终点就是要求的根。
*/
#include <cstdio>
#include <iostream>
#include<queue>
#include<set>
#include<ctime>
#include<algorithm>
#include<cmath>
#include<vector>
#include<map>
#include<cstring>
using namespace std;
const double eps=1e-10;
#define M 1009
#define type __int64
const type inf=(1LL)<<60;
struct point
{
    int x,y,h;
}p[M];

struct Node{
    int u , v;
    type cost;
}E[M*M+5];
int pre[M],ID[M],vis[M];
type In[M],sum;
int n,m,ansi;
type Directed_MST(int root,int NV,int NE) {
    type ret = 0;
    while(true) {
        //1.找最小入边
        for(int i=0;i<NV;i++) In[i] = inf;
        for(int i=0;i<NE;i++){
            int u = E[i].u;
            int v = E[i].v;
            if(E[i].cost < In[v] && u != v) {
                pre[v] = u;
                if(u==root)//记录是root从哪一条边到有效点的（这个点就是实际的起点）
                ansi=i;
                In[v] = E[i].cost;
            }
        }
        for(int i=0;i<NV;i++) {
            if(i == root) continue;
            if(In[i] == inf)    return -1;//除了跟以外有点没有入边,则根无法到达它
        }
        //2.找环
        int cntnode = 0;
    memset(ID,-1,sizeof(ID));
    memset(vis,-1,sizeof(vis));
        In[root] = 0;
        for(int i=0;i<NV;i++) {//标记每个环
            ret += In[i];
            int v = i;
            while(vis[v] != i && ID[v] == -1 && v != root) {
                vis[v] = i;
                v = pre[v];
            }
            if(v != root && ID[v] == -1) {
                for(int u = pre[v] ; u != v ; u = pre[u]) {
                    ID[u] = cntnode;
                }
                ID[v] = cntnode ++;
            }
        }
        if(cntnode == 0)    break;//无环
        for(int i=0;i<NV;i++) if(ID[i] == -1) {
            ID[i] = cntnode ++;
        }
        //3.缩点,重新标记
        for(int i=0;i<NE;i++) {
            int v = E[i].v;
            E[i].u = ID[E[i].u];
            E[i].v = ID[E[i].v];
            if(E[i].u != E[i].v) {
                E[i].cost -= In[v];
            }
        }
        NV = cntnode;
        root = ID[root];
    }
    return ret;
}
int main()
{
    int u,v;
    type w;
    while(scanf("%d%d",&n,&m)!=EOF)
    {
        sum=0;
        for(int i=0;i<m;i++)
        {
            scanf("%d%d%I64d",&u,&v,&w);
            u++;
            v++;
            E[i].u=u;
            E[i].v=v;
            E[i].cost=w;
            sum+=w;
        }
        sum++;
        for(int i=m;i<m+n;i++)//第i条边的终点为i-m;
        {
            E[i].u=0;
            E[i].v=i-m+1;
            E[i].cost=sum;
        }
        type ans=Directed_MST(0,n+1,m+n);
        if(ans==-1||ans-sum>=sum)//最小树形图的边权和值大于sum的两倍，说明不可能构成最小树形图，因为必定存在两条从虚拟点出发的边
        puts("impossible");
        else
        { printf("%I64d %d\n",ans-sum,ansi-m);//利用i>=m时，第i条边的终点为i-m;这里不能替换为E[ansi].v-1;因为E[i]在朱刘算法过程中节点信息会变化。
        }
        puts("");
    }
    return 0;
}
#endif
