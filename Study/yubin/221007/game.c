#include <stdio.h>
#include <ncurses.h>
#include <locale.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <pthread.h>

#define N 15
char map[N][N + 1] = {

	"###############",
	"#    ^^    a###",
	"########  #####",
	"#       ^^    #",
	"###^ ##########",
	"#^^       ^^  #",
	"# ####^ #### ##",
	"#        a    #",
	"#### ### ### ##",
	"#    ^^^      #",
	"## ###### #####",
	"#^      ^^^^  #",
	"########## ####",
	"#  a         Y#",
	"###############",
};

int ny = 1;
int nx = 1;

int my1 = 1;
int mx1 = 10;

int my2 = 14;
int mx2 = 4;

int hp = 100;

void *mon(){
	
	int dy[4] = {-1, 1, 0, 0};
	int dx[4] = {0 ,0, -1, 1};

	while(1) {

		int d1 = rand() % 4;
		int d2 = rand() % 4;
		int tmpx1 = mx1 + dx[d1];
		int tmpy1 = my1 + dy[d1];
		int tmpx2 = mx2 + dx[d2];
		int tmpy2 = my2 + dy[d2];

		if(map[tmpy1][tmpx1]=='#') continue;
		if(map[tmpy2][tmpx2]=='#') continue;
		mx1 = tmpx1;
		my1 = tmpy1;
		mx2 = tmpx2;
		my2 = tmpy2;

		usleep(1000 * 200);
	}
}

void print()
{
	clear();
	for (int y = 0; y < N; y++) {
		for (int x = 0; x < N; x++) {
			if (y == ny && x == nx) {
				printw("ᑒ ");
			}
			else if (y == my1 && x == mx1) {
				printw("⍩1");
			}
			else if (y == my2 && x == mx2) {
				printw("⍩2");
			}
			else if (map[y][x] == '#') {
				printw("▒▒");
			}
			else if (map[y][x] == '^') {
				printw("^^");
			}
			else if (map[y][x] == 'a') {
				printw("aa");
			}
			else if (map[y][x] == 'Y') {
				printw("YY");
			}
			else if (map[y][x] == ' ') {
				printw("  ");
			}
		}
		printw("\n");
	}
	printw("HP : %d\n", hp);
	refresh();
}

int main()
{
	srand(time(NULL));
	setlocale(LC_CTYPE, "ko_KR.utf8");
	initscr();

	pthread_t tid;

	pthread_create(&tid, NULL, mon, NULL);

	nodelay(stdscr, TRUE);
	keypad(stdscr,	TRUE);

	while(1) {
		print();
		int ch = getch();
		if (ch == ERR) ch = 0;

		if(ch==KEY_LEFT) {
			if(map[ny][nx-1] != '#') nx--;
			if(map[ny][nx] == '^') hp -= 10;
		}
		if(ch==KEY_RIGHT) {
			if(map[ny][nx+1] != '#') nx++;
			if(map[ny][nx] == '^') hp -= 10;
		}
		if(ch==KEY_UP) {
			if(map[ny-1][nx] != '#') ny--;
			if(map[ny][nx] == '^') hp -= 10;
		}
		if(ch==KEY_DOWN) {
			if(map[ny+1][nx] != '#') ny++;
			if(map[ny][nx] == '^') hp -= 10;
		}

		if((ny==my1 && nx==mx1)||(ny==my2 && nx==mx2)|| hp == 0) {
			print();
			usleep(1000 * 500);
			clear();
			mvprintw(10, 30, "GAME OVER");
			refresh();
			sleep(1);
			break;
		}
		if(map[ny][nx] == 'Y') {
			print();
			usleep(1000 * 500);
			clear();
			mvprintw(10, 30, "WIN![%d]", hp);
			refresh();
			sleep(1);
			break;
		}
		if( map[ny][nx] == 'a') {
			hp += 100;
			map[ny][nx] = ' ';
		}
	}

	getch();
	endwin();
	return 0;
}

