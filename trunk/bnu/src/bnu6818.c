#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <limits.h>
/* AC */
#define M 18
static int cost[M][M];
static int nv, ne;
static int wn[M];
static int sno[M];
static int nr, nc;
static double ratio ;
static int mtree[M];
static int prim(void){
	static int key[M];
	static int used[M];
	int u, v, k, r ;
	int i;
	int ans, mkey ;
	nv = nr;
	r = sno[0];
	for(i=0; i<nv; ++i){
		u = sno[i];
		key[u] = cost[r][u];
		used[u] = 0;
	}
	for(ans=0, used[r]=1, k=0; k<nv-1; ++k){
		for(mkey=INT_MAX, i=0; i<nv; ++i){
			u = sno[i];
			if(!used[u] && mkey>key[u]){
				mkey = key[u]; v=u;
			}
		}
		if(mkey==INT_MAX) return 0;
		ans += mkey;
		used[v] = 1;
		for(i=0; i<nv; ++i){
			u = sno[i];
			if(!used[u] && cost[v][u] <key[u]){
				key[u] = cost[v][u];
			}
		}
	}
	return ans;
}
static int prim2(void){
	static int key[M];
	static int used[M];
	static int cost2[M][M];
	int u, v, k ;
	int i, j;
	int ans, mkey ;
	nv = nr;
	for(i=0; i<nv; ++i){
		for(j=0; j<nv; ++j){
			cost2[i][j] = cost[sno[i]][sno[j]];
		}
	}

	for(u=0; u<nv; ++u){
		key[u] = cost2[0][u];
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
			if(!used[u] && cost2[v][u] <key[u]){
				key[u] = cost2[v][u];
			}
		}
	}
	return ans;
}

void combine(int x, int k){
	if(k>=nr){
		int i;
		int tn, te;
		double r;
#if 1
		te =prim2();
		for(tn=0, i=0; i<nr; ++i){
			tn += wn[sno[i]];
		}
		r = 1.0*te/tn;
		if(ratio<0 || ratio-r>1e-8){
			ratio = r;
			for(i=0; i<nr; ++i){
				mtree[i] = sno[i]+1;
			}
		}
#else
		for(i=0; i<nr; ++i){
			printf("%d ", sno[i]);
		}
		printf("\n");
#endif
	}else if(x>=nc){
		return;
	}else{
		sno[k] = x;
		combine(x+1, k+1);
		combine(x+1, k);
	}

}
void dfs(int u,int cnt){
    int i,j;
    sno[cnt]=u;
    if(cnt>=nr-1){
		int tn, te;
		double r;
		te =prim();
		for(tn=0, i=0; i<nr; ++i){
			tn += wn[sno[i]];
		}
		r = 1.0*te/tn;
		if(ratio<0 || ratio-r>1e8){
			ratio = r;
			for(i=0; i<nr; ++i){
				mtree[i] = sno[i]+1;
			}
		}
    }else{
    	for(i=u+1;i<nc;i++)
    		dfs(i,cnt+1);
    }
}
void combine2(int u, int k){
	int i;
	for(i=0; i<nc; ++i){
		dfs(i, 0);
	}
}
static void solve(void){
	int i, j;
	while(~scanf("%d%d", &nc, &nr)){
		if(!nc) break;
		for(i=0; i<nc; ++i) scanf("%d", wn+i);
		for(i=0; i<nc; ++i){
			for(j=0; j<nc; ++j){
				scanf("%d", &cost[i][j]);
			}
		}
		ratio = -1.0;
		combine(0, 0);
		for(i=0; i<nr; ++i){
			if(i) printf(" ");
			printf("%d", mtree[i]);
		}
		printf("\n");
	}
}
int main(void){
	freopen("data.dat", "r", stdin);
	solve();
	return 0;
}
