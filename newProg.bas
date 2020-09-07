10 REM prog init
11 ARRAY Q, 2

100 REM prog start
101 PRINT "Hello?"
110 INPUT A; "Do you need a tuturial?"
120 IF A == "Y" THEN GOSUB 301

300 REM tutorial
301 PRINT "this is how you do"
