#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

void go1(int num)
{
	printf("\n[Button Clicked]\n");
}

void go2(int num)
{
	system("clear");
	printf("\nRESET\n");
}

void go3(int num)
{
	printf("\nBYE\n");
	exit(0);
}

int main()
{
	setbuf(stdout, NULL);

	signal(SIGUSR1, go1);
	signal(SIGUSR2, go2);
	signal(SIGTERM, go3);

	while(1){
		for(int i='A'; i<='Z'; i++){
			printf("%c", i);
			usleep(1000 * 100);
		}
	}

	return 0;
}
