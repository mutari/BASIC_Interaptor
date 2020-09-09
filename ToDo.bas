10 REM initing
20 ARRAY T, 2
21 LET N = 0
30 REM pos data 10000 = print line, 140 = To beginign
31 ARRAY D, 1
32 D[0] = 10000
33 D[1] = 140

100 PRINT "ToDo app"
110 GOSUB D[0]

120 PRINT "write 'HELP' for help"

140 INPUT ":"; A
150 IF A == "HELP" THEN GOSUB 400
151 IF A == "ADD" THEN GOSUB 500
152 IF A == "REMOVE" THEN GOSUB 600
153 IF A == "UPDATE" THEN GOSUB 700
154 IF A == "TOGGEL" THEN GOSUB 800
155 IF A == "LIST" THEN GOSUB 900

399 GOTO D[1]

400 GOSUB D[0]
405 PRINT "HELP menu"
410 PRINT "ADD      - adds a ToDo"
415 PRINT "REMOVE   - removes a ToDo based on id"
420 PRINT "UPDATE   - update a ToDo based on id"
425 PRINT "TOGGEL   - toggel based on id"
430 PRINT "LIST     - list all"
498 GOSUB D[0]
499 RETURN

500 GOSUB D[0]
505 INPUT "Title: "; A
506 T[N][0] = A
510 INPUT "Discription: "; A
511 T[N][1] = A
515 T[N][2] = 0
516 N = N + 1
520 GOSUB D[0]
599 RETURN 

600 GOSUB D[0]
641 PRINT "Remove"
642 GOSUB D[0]
650 INPUT "id: "; A
651 INPUT "Do you whant to remove question: " + A + "(YES/NO)"; B
659 IF B == "YES" THEN GOTO 660 ELSE GOTO D[1]
660 FOR I = A TO N
661 PRINT I + "  " + N
665 IF I + 1 < N THEN GOTO 666 ELSE GOTO 675
666 T[I][0] = T[I + 1][0]
667 T[I][1] = T[I + 1][1]
668 T[I][2] = T[I + 1][2]
669 GOTO 680
675 T[I][0] = ""
676 T[I][1] = ""
677 T[I][2] = ""
680 NEXT I
685 N = N - 1
699 RETURN

700 GOSUB D[0]
799 RETURN

800 GOSUB D[0]
899 RETURN

900 GOSUB D[0]
905 FOR I = 0 TO N 
910 IF T[I][2] == 0 THEN LET X = "Working on!"
920 PRINT I + ": " + T[I][0] + ", " + T[I][1] + " : " + X
930 NEXT I
940 GOSUB D[0]
999 RETURN


10000 PRINT "--------------"
10001 RETURN