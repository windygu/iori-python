/*
 * adjMatrix.c
 *
 *  Created on: 2013-4-23
 *      Author: IORI
 *      图的邻接矩阵的表示法及相关算法
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 10
#define DIRECTED 0
#define UNSET 0
#define UNDIRECTED 1
#define SWAP_INT(a,b) do{\
	int c; c=(a); (a)=(b);(b)=c;\
}while(0)

typedef struct {
	int adj[M][M];
	int ne, nv; /* 边和顶点数 */
	int kind;
}*mgraph;


int visited[M];
int visit_no = 0;  /* 记录顶点访问次序  */
int tree_edge[M*10][2]; /* 树边 */
int forward_edge[M*10][2];
int back_edge[M*10][2];
int cross_edge[M*10][2];
int ntree, nforward, nback, ncross;

int entry_t[M];  /* first encounter a vertext */
int exit_t[M];	/* exit a vertex */
mgraph mg_create(){
	int i;
	int s, e, w;
	mgraph mg = malloc(sizeof(*mg));
	memset(mg->adj, 0, sizeof(mg->adj));
	scanf("%d%d%d", &mg->nv, &mg->ne, &mg->kind);
	memset(mg->adj, 0, mg->nv *mg->nv*sizeof(int));
	for(i=0; i<mg->ne; ++i){
		scanf("%d%d%d", &s, &e, &w);
		mg->adj[s][e] = w;
		if(mg->kind==UNDIRECTED){
			mg->adj[e][s] = w;
		}
	}
	return mg;
}

void mg_print(mgraph mg){
	int i, j;
	for(i=0; i<mg->nv; ++i){
		for(j=0; j<mg->nv; ++j){
			printf("%4d ", mg->adj[i][j]);
		}
		printf("\n");
	}
}

mgraph mg_copy(mgraph mg){
	int i,j;
	mgraph ret = malloc(sizeof(*mg));
	ret->kind = mg->kind;
	ret->nv  = mg->nv;
	ret->ne = mg->ne;
	for(i=0; i<mg->nv; ++i){
		for(j=0; j<mg->nv; ++j){
			ret->adj[i][j] = mg->adj[i][j];
		}
	}
	return ret;

}
/* 有向图转置, 对邻接矩阵来说是矩阵的置
 * Gt = (V, Et) Et={(u,v)in(V*V)| (v,u) in E}
 */
mgraph mg_transpose(mgraph mg){
	mgraph ret;
	int i,j;
	ret = mg_copy(mg);
	for(i=0; i<ret->nv; ++i){
		for(j=0; j<i; ++j){
			SWAP_INT(ret->adj[i][j], ret->adj[j][i]);
		}
	}
	return ret;

}
/*
 * 有向图平方图
 * G^2=(V, E^2) E^2={(u, w) in (V*V)| v in V && (u,v)in(E) && (v,w)in(E)
 */

/* 汇顶占  Vin=n-1, Vout=0
 * O(n)找出汇
 * 汇点 t  adj[i][t] = 1
 *		adk[t][i] = 0
 * a[i][j]=0 j不是汇， j的入度少了 （i==j除外 )
 * a[i][j]=1 i不是汇,i有出度了
 *
 * */
int mg_is_sink(mgraph mg, int v){
	int i;
	for(i=0; i<mg->nv; ++i){
		if(mg->adj[v][i]==1) return 0;
		if(i!=v && mg->adj[i][v]==0) return 0;
	}
	return 1;
}
void mg_universe_sink(mgraph mg){
	int i,j;
	/**
	 * 此函数退出时， 0..i-1肯定不是汇点
	 * i<n时，肯定是 j>=n, 说明每一列均有0元素
	 * 对 i<k<n，行k没有检查，0出现的位置肯定不在k行的对角线上(t@[0,n-1]&&t!=k,a[k][t]=0)
	 * adj[t][j]==0 j@(0..n-1) j肯定不是汇点， t=j除外
	 */
	for(i=0,j=1; i<mg->nv && j<mg->nv;){
		if(mg->adj[i][j]!=0){ /* i肯定不是汇 */
			i++;
		}else{
			j++;
		}
	}
	if(i>=mg->nv){
		printf("no universe sink\n");
	}else{

	}
}
static void dfs(mgraph mg, int v){
	int i;
	visited[v] = visit_no++;
	printf("%d, ", v+1);
	for(i=0; i<mg->nv; ++i){
		if(mg->adj[v][i]){
			if(!visited[i]){
				dfs(mg, i);
			}
		}
	}
}
/*
 * 对无向图来说，只有树边和向后边
Edge classification in a DFS:
1. Tree Edge, if in edge (u,v), v is first discovered, then (u, v) is a tree
  edge.
1. Back Edge, if ......, v is discovered already and v is an ancestor, then it's
  a back edge.
3. Forward Edge, if ......, v is discovered already and v is a descendant of u,
  forward edge it is.
4. Cross Edge, all edges except for the above three.
f you really need it, you can check it by maintaining so called entry and exit
 times for each node. During the run of the algorithm, you increment a time
 variable (starting from 0, of course) each time you encounter a new vertex.
 The times entry_t(v), exit_t(v) are initially unset for all vertices.

When you first encounter a vertex, you set entry(v):=time. When you exit a vertex
by an up edge (ie. poping the vertex from the stack), you set its exit(v):=time.
With that, you have:
if entry(u) is set and exit(u) is not set, then u is ancestor of the current
vertex (ie. vu is a back edge)
if entry(u)>entry(current), then u is descendant from the current vertex
(current->u is a forward edge)
otherwise, it is a cross edge.
Note that these relations are made for checking during the run of the algorithm.
 After the algorithm has completed, a check of ancestry is basically:
u is_descendant_of v = entry(u)>entry(v) and exit(u)<=exit(v)
*/
static void edge_dfs(mgraph mg, int v){
	int i;
	entry_t[v] = visit_no++;
	for(i=0; i<mg->nv; ++i){
		if(mg->adj[v][i]){
			if(entry_t[i]==UNSET){ /* tree edge */
				tree_edge[ntree][0] = v;
				tree_edge[ntree++][1] = i;
				edge_dfs(mg, i);
			}else if(entry_t[v]<entry_t[i]){ /* forword edge */
				forward_edge[nforward][0] = v;
				forward_edge[nforward++][1] = i;

			}else if(exit_t[i]==UNSET){
				back_edge[nback][0] = v;
				back_edge[nback++][1] = i;
			}else{
				cross_edge[ncross][0] = v;
				cross_edge[ncross++][1] = i;
			}
		}
	}
	exit_t[v] = visit_no;
}
void mg_edge_classify(mgraph mg){
	int i;
	for(i=0; i<mg->nv; ++i){
		entry_t[i] = exit_t[i] = UNSET;
	}
	visit_no = 1;
	ntree = nforward = nback = ncross = 0;
	for(i=0; i<mg->nv; ++i){
		if(entry_t[i] == UNSET){
			edge_dfs(mg, i);
		}
	}
	printf("tree edge:\n");
	for(i=0; i<ntree; ++i){
		printf("(%d, %d)", tree_edge[i][0]+1, tree_edge[i][1]+1);
	}
	printf("\nback edge: \n");
	for(i=0; i<nback; ++i){
		printf("(%d, %d)", back_edge[i][0]+1, back_edge[i][1]+1);
	}
	printf("\nforward edge:\n");
	for(i=0; i<nforward; ++i){
		printf("(%d, %d)", forward_edge[i][0]+1, forward_edge[i][1]+1);
	}
	printf("\ncross_edge:\n");
	for(i=0; i<ncross; ++i){
		printf("(%d, %d)", cross_edge[i][0]+1, cross_edge[i][1]+1);
	}
	printf("\n");
	for(i=0; i<mg->nv; ++i){
		printf("(%d, %d)", entry_t[i], exit_t[i]);
	}
	printf("\n");
}


void mg_dfs(mgraph mg){
	int i;
	for(i=0; i<mg->nv; ++i){
		visited[i] = 0;
	}
	visit_no = 1;
	ntree = nforward = nback = ncross = 0;
	for(i=0; i<mg->nv; ++i){
		if(!visited[i]){
			dfs(mg, i);
			printf("\n");
		}
	}
}
void mg_test(void){
	mgraph mg;
	mg = mg_create();
	mg_dfs(mg);
	mg_edge_classify(mg);
}
