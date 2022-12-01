1000 REM Fibonacci Sequence Project
1010 REM Quite BASIC Math Project
1020 REM ------------------------ 
2020 REM The array F holds the Fibonacci numbers
2030 ARRAY F
2040 F[0] = 0
2050 F[1] = 1
2055 LET OUT = ""
2060 LET N = 1
2070 REM Compute the next Fibbonacci number
2080 F[N + 1] = F[N] + F[N - 1]
2100 OUT = OUT + "(" + N + ")" + F[N] + ", "
2090 LET N = N + 1
2110 REM Stop after printing  50 numbers
2120 IF N <= 50 THEN GOTO 2080
2125 PRINT N
2130 PRINT OUT

