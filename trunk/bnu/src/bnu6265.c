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
	int ans;     /* ��С������Ȩֵ   */
	int pre[M]; /* �б�(u, v) pre[v]=u; */
	int in[M];  /*  in[v] = min(w(u, v)) ������v�����ı� */
	int id[M]; /* ÿ��������ڵ�Ȧ */
	int vis[M];
	int nc; /* Ȧ�������� Ҳ����ͼ�Ķ�����  */
	int u, v, w, i;
	nc = nv;
	while(1){
		for(i=0; i<nv; ++i) in[i] = INT_MAX;
		/* ����С��� */
		for(i=0; i<ne; ++i){
			u = edges[i].u; v=edges[i].v; w=edges[i].w;
			if(u!=v && w<in[v]){
				pre[v] = u; in[v] = w;
			}
		}
		/* ��û�����Ϊ0�ĵ㣬�����⣬�еĻ������������� */
		for(i=0; i<nv; ++i){
			if(i==r) continue;
			if(in[i]==INT_MAX) return -1;
		}
		/* ��Ȧ */
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
		/* ��Ȧ  */
		if(nc==0) break;
		/* ͼ�ع������±�� */
		for(u=0; u<nv; ++u){
			if(id[u]==-1) id[u]=nc++;
		}
		/* ������Ӧ��Ȩֵ  */
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



/* ����Ϊ��ȷ ���㷨 */
/*
����Ϊ���ǹ̶�������С����ͼ�����ǿ��������һ������Ȼ���ڰ��������ÿ���������������ĵ������Ϊ����󣬻�����Ϊ���бߺʹ�һ�㣬����Ϊr��Ȼ��Ϳ���������С����ͼ���м����ˣ�������Ľ����ȥr,�����r����Ϳ�����Ϊͨ���������ڵ���������ԭͼ�������㣬��ԭͼ�ǲ���ͨ�ģ����ǾͿ�����Ϊ��������С����ͼ�����������С��Ҳͦ�򵥣�������С�뻡ʱ���������������������������ô���������յ����Ҫ��ĸ���
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
        //1.����С���
        for(int i=0;i<NV;i++) In[i] = inf;
        for(int i=0;i<NE;i++){
            int u = E[i].u;
            int v = E[i].v;
            if(E[i].cost < In[v] && u != v) {
                pre[v] = u;
                if(u==root)//��¼��root����һ���ߵ���Ч��ģ���������ʵ�ʵ���㣩
                ansi=i;
                In[v] = E[i].cost;
            }
        }
        for(int i=0;i<NV;i++) {
            if(i == root) continue;
            if(In[i] == inf)    return -1;//���˸������е�û�����,����޷�������
        }
        //2.�һ�
        int cntnode = 0;
    memset(ID,-1,sizeof(ID));
    memset(vis,-1,sizeof(vis));
        In[root] = 0;
        for(int i=0;i<NV;i++) {//���ÿ����
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
        if(cntnode == 0)    break;//�޻�
        for(int i=0;i<NV;i++) if(ID[i] == -1) {
            ID[i] = cntnode ++;
        }
        //3.����,���±��
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
        for(int i=m;i<m+n;i++)//��i���ߵ��յ�Ϊi-m;
        {
            E[i].u=0;
            E[i].v=i-m+1;
            E[i].cost=sum;
        }
        type ans=Directed_MST(0,n+1,m+n);
        if(ans==-1||ans-sum>=sum)//��С����ͼ�ı�Ȩ��ֵ����sum��������˵�������ܹ�����С����ͼ����Ϊ�ض��������������������ı�
        puts("impossible");
        else
        { printf("%I64d %d\n",ans-sum,ansi-m);//����i>=mʱ����i���ߵ��յ�Ϊi-m;���ﲻ���滻ΪE[ansi].v-1;��ΪE[i]�������㷨�����нڵ���Ϣ��仯��
        }
        puts("");
    }
    return 0;
}
#endif
