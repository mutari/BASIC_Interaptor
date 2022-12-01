1000 REM Quite BASIC Algorithm Project
1010 REM Merge Sort program
1100 REM Initialize the arrays
1100 LET N = 10
1110 LET C = 0 
1120 ARRAY A
1131 ARRAY B
1140 GOSUB 3000
1150 REM Print the random array
1160 PRINT "Random list:"
1170 GOSUB 4000
1180 REM Sort the array
1190 GOSUB 2000
1200 PRINT "Sorted list:"
1210 REM Print the sorted array
1220 GOSUB 4000
1230 PRINT "Number of Iterations: ";
1240 PRINT C
1250 END
2000 REM Merge sort the list A of length N
2010 REM Using the array B for temporary storage
2020 REM 
2030 REM === Split phase ===
2040 REM C counts the number of split/merge iterations
2050 LET C = C + 1
2060 LET X = 1
2070 LET Y = 1
2080 LET Z = N
2090 GOTO 2110
2100 IF X < 10 THEN GOTO 2101 ELSE GOTO 2170
2101 IF A[X] < A[X - 1] THEN GOTO 2170
2110 B[Y] = A[X]
2120 LET Y = Y + 1
2130 LET X = X + 1 
2140 IF Z < Y THEN GOTO 2200
2150 GOTO 2100
2160 IF A[X] < A[X - 1] THEN GOTO 2110
2170 LET B[Z] = A[X]
2180 LET Z = Z - 1
2190 LET X = X + 1 
2200 IF Z < Y THEN GOTO 2300
2210 GOTO 2160
2220 REM 
2300 REM === Merge Phase ===
2310 REM Q means "we're done" (or "quit")
2320 REM Q is 1 until we know that this is _not_ the last iteration
2330 LET Q = 1
2340 LET X = 1
2350 LET Y = 1
2360 LET Z = N
2370 REM First select the smaller item
2380 IF B[Y] < B[Z] THEN GOTO 2480 ELSE GOTO 2520
2390 REM Check if the loop is done
2400 IF Z < Y THEN GOTO 2560
2410 REM If both items are smaller then start over with the smallest
2420 IF B[Y] >= A[X - 1] OR B[Z] >= A[X - 1] THEN GOTO 2450
2430 LET Q = 0
2440 GOTO 2370
2450 REM Pick the smallest item that represents an increase
2460 IF B[Z] < B[Y] AND B[Z] >= A[X - 1] THEN GOTO 2520
2470 IF B[Z] > B[Y] AND B[Y] < A[X - 1] THEN GOTO 2520
2480 LET A[X] = B[Y]
2490 LET Y = Y + 1
2500 LET X = X + 1
2510 GOTO 2390
2520 LET A[X] = B[Z]
2530 LET Z = Z - 1
2540 LET X = X + 1
2550 GOTO 2390
2560 IF Q = 0 THEN GOTO 2030
2570 RETURN
3000 REM Create a random list of N integers
3030 FOR I = 1 TO N
3040 A[I] = I * 10
3070 NEXT I
3090 RETURN 
4000 REM PRINT the list A
4005 LET STR = ""
4010 FOR I = 1 TO N
4020 STR = STR + A[I] + ", "
4040 NEXT I
4050 PRINT STR
4060 RETURN
