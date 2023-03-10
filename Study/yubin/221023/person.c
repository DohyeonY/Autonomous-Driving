#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <signal.h>
#include <stdlib.h>

int main(int arg1, char *arg2[])
{
	if(arg1!=2){
		printf("\nERROR\n");
		return 0;
	}
	
	int num = atoi(arg2[1]);
	int cmd;

	while(1){
		printf("INPUT >> ");
		scanf("%d", &cmd);
	
		if(cmd==1) kill(num, SIGUSR1);	
		if(cmd==2) kill(num, SIGUSR2);	
		if(cmd==3) kill(num, SIGTERM);
	}	

	return 0;
}
