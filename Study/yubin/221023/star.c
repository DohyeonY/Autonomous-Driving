 #include <ncurses.h>
 #include <unistd.h>
 #include <time.h>
 #include <stdlib.h>

 int main()
 {
     initscr();
     curs_set(0);
     srand(time(NULL));

     while(1) {

         int y = rand() % 50;
         int x = rand() % 50;

         for(int i = 0; i < 5; i++) {
             clear();
             for(int j = 0; j<=i; j++) {
                 mvprintw(y+j, x, "*");
                 refresh();
             }
             usleep(1000 * 50); // 0.01 sec
         }

         for(int i = 0; i < 5; i++) {
             clear();
             for(int j = 4; j>=i; j--) {
                 mvprintw(y+j, x, "*");
                 refresh();
             }
             usleep(1000 * 50); // 0.01 sec
         }
         usleep(1000 * 10);

         clear();
     }

     getch();
     endwin();

     return 0;
 }
