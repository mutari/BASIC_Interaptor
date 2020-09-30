10 REM prog init
11 ARRAY Q, 2
12 Q[0][0] = "är färgen blå blå?"
13 Q[0][1] = "YES"
14 Q[1][0] = "Lever elvis?"
15 Q[1][1] = "NO"
99 LET N = 2 

100 REM prog start
101 PRINT "Välkomen till quisME"
102 PRINT "Forgesport:          1"
103 PRINT "skapa frågot:        2"
104 PRINT "ändra frågor:        3"
105 PRINT "Skriv ut frågor:     4"
110 INPUT ":"; A
120 IF A == 1 THEN GOTO 301
121 IF A == 2 THEN GOTO 401
122 IF A == 3 THEN GOTO 501
123 IF A == 4 THEN GOTO 601

200 END

300 REM ask
301 GOSUB 1000
302 PRINT "quis"
303 LET R = 0
310 FOR I = 0 TO N
320 INPUT Q[I][0] + "  "; A
330 IF A == Q[I][1] THEN GOSUB 360 ELSE PRINT "Du svarade fel"
340 GOSUB 1000
350 NEXT I
351 PRINT "Slutgiltigt resultat: " + R + "/" + N
352 GOSUB 1000
399 GOTO 102

360 PRINT "Du svarade rätt"
361 R = R + 1
369 RETURN

400 REM create
401 PRINT "create a quesion"
410 INPUT "Fråga: "; A
411 Q[N][0] = A
420 INPUT "Svar (YES/NO): "; A
421 Q[N][1] = A
430 N = N + 1
435 GOSUB 1000
440 GOTO 102

500 REM ändra
501 GOSUB 1000
502 PRINT "Update row:  1"
503 PRINT "Remove row:  2"
504 INPUT ":"; A
505 IF A == 1 THEN GOTO 520
506 IF A == 2 THEN GOTO 540

520 PRINT "Update"
521 GOSUB 590
522 INPUT ":"; A
523 PRINT "Fråga: 0"
524 PRINT "Svar: 1"
525 INPUT ":"; B
526 INPUT Q[A][B] + " = "; C
527 Q[A][B] = C 
539 GOTO 102


540 PRINT ""
541 PRINT "Remove"
542 GOSUB 1000
543 GOSUB 590
550 INPUT ":"; A
551 INPUT "Do you whant to remove question: " + A + "(YES/NO)"; B
559 IF B == "YES" THEN GOTO 560 ELSE GOTO 102
560 FOR I = A TO N
561 IF I + 1 < N THEN GOTO 562 ELSE GOTO 565
562 Q[I][0] = Q[I + 1][0]
563 Q[I][1] = Q[I + 1][1]
564 GOTO 570
565 Q[I][0] = ""
565 Q[I][1] = ""
570 NEXT I
573 N = N - 1
574 GOSUB 1000

589 GOTO 102

590 REM print all questions
591 FOR I = 0 TO N
592 PRINT  I + ": " + Q[I][0] + " / " + Q[I][1]
593 NEXT I
594 RETURN

601 GOSUB 1000
602 GOSUB 591
603 GOSUB 1000
604 GOTO 102


1000 PRINT "----------------------------------"
1001 RETURN