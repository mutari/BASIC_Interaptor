1 REM colors
10 ARRAY c
11 c[1] = "red"
12 c[2] = "blue"
13 c[3] = "yellow"
14 c[4] = "cyan"
15 c[5] = "blue"
16 c[6] = "magenta"
17 c[7] = "gray"
30 S = 1

50 REM variablar
51 ARRAY K, 2
52 REM X
53 K[0][0] = 10
54 K[1][0] = K[0][0]
55 REM Y
56 K[0][1] = 10
57 K[1][1] = K[0][1]
58 REM aray whit placeholder vars [0] = Standing on color, [1] = number of random walls, [2] [3] [4] = random shit, [10] = What world algorytme to use 1000 = random. 2000 = maze, [100] = what program to run 90 = game, 10000 = map creator
59 ARRAY N
60 N[1] = 1000
61 N[10] = 1000
62 N[100] = 90
70 REM screan size
71 W = 50
72 H = 50

80 GOTO N[100]

90 REM Game setup
91 DISPLAY W, H, TRUE
92 REM creat word
93 GOSUB N[10]
94 REM Draw Game
95 GOSUB 3000

100 REM start game loop
101 CLS
102 REM draw game
110 PLOT K[0][0], K[0][1], c[S]
111 DRAW B

300 REM key input
301 LET U = UPPERCASE(GETCHAR())
310 IF U = "" THEN GOTO 300 ELSE GOTO 400

400 REM Key handler
401 IF U = "A" THEN K[0][0] = K[0][0]-1
402 IF U = "D" THEN K[0][0] = K[0][0]+1
403 IF U = "W" THEN K[0][1] = K[0][1]-1
404 IF U = "S" THEN K[0][1] = K[0][1]+1
405 GOSUB 600
430 REM go to start of game loop
431 GOTO 100 


600 REM Colision
601 LET N[0] = COLOR(K[0][0], K[0][1])
602 IF N[0] = "gray" THEN GOTO 610 ELSE GOTO 620
610 K[0][0] = K[1][0]
611 K[0][1] = K[1][1]
612 RETURN
620 K[1][0] = k[0][0]
621 K[1][1] = k[0][1]
622 RETURN

1000 REM declear the world (RANDOM)
1001 ARRAY B,2 
1002 REM B[20][20] = c[7]
1003 REM B[21][20] = c[7]
1004 FOR I = 1 TO N[1]
1005 N[2] = RAND(W)-1
1006 N[3] = RAND(H)-1
1007 IF B[N[2]][N[3]] = "red" THEN GOTO 1100
1010 B[N[2]][N[3]] = c[7]
1011 NEXT I
1099 RETURN

1100 REM If wall owerlay remove
1101 B[N[2]][N[3]] = "red"
1102 GOTO 1005

2000 REM declare maze world
2001 ARRAY B,2
2002 FOR I = 0 TO W
2003 FOR J = 0 TO H
2004 B[I][J] = "gray"
2005 NEXT J
2006 NEXT I
2007 N[2000] = 0
2008 N[2001] = 3
2009 B[N[2000]][N[2001]] = ""
2999 RETURN

3000 REM draw game
3001 PLOT K[0][0], K[0][1], c[S]
3002 DRAW B
3003 RETURN



10000 REM Map creator
10001 PRINT GETCLICK()
10002 GOTO 10000