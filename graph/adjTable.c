/*
 * adjTable.c
 *
 *  Created on: 2013-4-23
 *      Author: IORI
 *  图的邻接表表示方法
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 10
#define DIRECTED 0
#define UNDIRECTED 1

/* 表节点 */
typedef struct tnode{
	int w; /* 此条边的权 */
	struct tnode *next;
	int vertex;
}*tnode;

/* 表头节点  */
struct thnode{
	int v;
	tnode first;
};

typedef struct {
	struct thnode adj[M];
	int nv, ne, kind;
}*tgraph;

tnode tnode_new(int w, int vertex){
	tnode tn;
	tn = (tnode)malloc(sizeof(*tn));
	tn->w = w;
	tn->vertex = vertex;
	tn->next = NULL;
	return tn;
}
struct thnode* tnode_insert(struct thnode*th, tnode tn){
	tn->next = th->first;
	th->first = tn;
	return th;
}

struct thnode* tnode_copy(struct thnode*dest, struct thnode*src){
	tnode tn, tn2, tn3;
	dest->first = NULL;
	tn3 = NULL;
	for(tn=src->first; tn; tn=tn->next){
		tn2 = tnode_new(tn->w, tn->vertex);
		if(!tn3){
			dest->first = tn2;
		}else{
			tn3->next = tn2;
		}
		tn3 = tn2;
	}
	if(tn3) tn3->next = NULL;
	return dest;
}
tgraph tg_create(){
	int i;
	int s, e, w;
	tnode tn;
	tgraph tg = (tgraph)malloc(sizeof(*tg));

	scanf("%d%d%d", &tg->nv, &tg->ne, &tg->kind);
	for(i=0; i<tg->nv; ++i){
		tg->adj[i].first = NULL;
	}
	for(i=0; i<tg->ne; ++i){
		scanf("%d%d%d", &s, &e, &w);
		tn = tnode_new(w, e);
		tnode_insert(tg->adj+s, tn);
		if(tg->kind==UNDIRECTED){
			tn = tnode_new(w, s);
			tnode_insert(tg->adj+e, tn);
		}
	}
	return tg;
}

void tg_print(tgraph tg){
	int i;
	tnode tn;
	for(i=0; i<tg->nv; ++i){
		for(tn=tg->adj[i].first; tn; tn=tn->next){
			printf("(%d, %d, %d)", i, tn->vertex, tn->w);
		}
		printf("\n");
	}
}

tgraph tg_copy(tgraph tg){
	int i;
	tgraph ret;
	ret = malloc(sizeof(*tg));
	ret->nv = tg->nv;
	ret->ne = tg->ne;
	ret->kind = tg->kind;
	for(i=0; i<ret->nv; ++i){
		tnode_copy(ret->adj+i, tg->adj+i);
	}
	return ret;
}
/* 有向图转置, 对邻接矩阵来说是矩阵的置
 * Gt = (V, Et) Et={(u,v)in(V*V)| (v,u) in E}
 */
tgraph tg_transpose(tgraph tg){
	int i;
	tgraph ret;
	tnode tn, tn2;
	ret = malloc(sizeof(*ret));
	ret->nv = tg->nv;
	ret->ne = tg->ne;
	ret->kind = tg->kind;
	for(i=0; i<ret->nv; ++i){
		ret->adj[i].first = NULL;
	}
	for(i=0; i<tg->nv; ++i){
		for(tn=tg->adj[i].first; tn; tn=tn->next){
			tn2 = tnode_new(tn->w, i);
			tnode_insert(ret->adj+tn->vertex, tn2);
		}
	}
	return ret;
}
void tg_test(void){
	tgraph tg ;
	tg = tg_create();
	tg_print(tg);
	tg_print(tg_copy(tg));
	tg_print(tg_transpose(tg));
}
