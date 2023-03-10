#include <ncurses.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int main()
{
	initscr();

	int a, b;
	scanw("%d", &a);
	scanw("%d", &b);

	srand(time(NULL));

	for(int i=0; i<10; i++){
		printw("%d\n", rand() % (b-a+1) + a);
	}
	refresh();

	getch();
	endwin();

	return 0;
}
