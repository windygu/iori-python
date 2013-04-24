#include <stdio.h>

void tg_test(void);
void mg_test(void);

int main(int ac, char *av[]){

	freopen("data.dat", "r", stdin);
#if 0
	tg_test();
#else
	mg_test();
#endif
	return 0;
}
