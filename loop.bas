10 LET K = "B"
20 ARRAY T,1
25 T[0] = 0
30 IF K == "A" THEN T[0] = T[0] + 1 ELSE T[0] = T[0] + 5
40 PRINT T[0]
50 GOTO 30