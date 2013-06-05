/*
 * bnu6028.c
 *
 *  Created on: 2013-6-4
 *      Author: Administrator
 *  修过的路可以看成成本是0
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define M 108
static int cost[M][M];
static int nv, ne;

static int prim(void){
	static int key[M];
	static int used[M];
	int u, v, k ;
	int ans, mkey ;
	for(u=0; u<nv; ++u){
		key[u] = cost[0][u]; /* 此问题的图是满的 共  nv*(nv-1)/2条边 */
		used[u] = 0;
	}
	for(ans=0, used[0]=1, k=0; k<nv-1; ++k){
		for(mkey=INT_MAX, u=1; u<nv; ++u){
			if(!used[u] && mkey>key[u]){
				mkey = key[u]; v=u;
			}
		}
		if(mkey==INT_MAX) return 0;
		ans += mkey;
		used[v] = 1;
		for(u=0; u<nv; ++u){
			if(!used[u] && cost[v][u] <key[u]){
				key[u] = cost[v][u];
			}
		}
	}
	return ans;
}

static void solve(void){
	int i;
	int u, v,c , e;
	while(scanf("%d", &nv), nv){
		ne = nv*(nv-1)/2;
		memset(cost, 0, sizeof(cost));
		for(i=0; i<ne; ++i){
			scanf("%d%d%d%d", &u, &v, &c, &e);
			c = e? 0: c;
			 cost[u-1][v-1]=cost[v-1][u-1] = c;
		}
		printf("%d\n", prim());
	}
}
#if 0
int main(void) {
	freopen("data.dat", "r", stdin);
	solve();
	return EXIT_SUCCESS;
}
#endif
