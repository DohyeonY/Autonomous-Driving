#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void go()
{
	printf("\n===SYSTEM ERROR===\n");
	exit(1);
}

int main()
{
	signal(SIGALRM, go);

	char buf[100];
	while(1){
		alarm(3);
		printf("INPUT >> ");
		scanf("%s", buf);
		printf("%s\n", buf);
	}
	return 0;
}
