1 REM Writen by: Philip Johansson
2 REM 
3 REM
4 REM
5 REM basic main library
6 REM array functions
7 REM
8 REM
9 REM

10 REM How to use!
11 REM Set upp variabel params
15 REM Call a function by its function path
16 REM Exampel:
17 REM LET param1 = "key"
18 REM GOSUB Fget
19 REM The exampel abov return the array value att key value position "key"

80 REM setup namespace
81 NAMESPACE "LIST"

100 REM setup function paths

101 LET LIST@get            = 1001
102 LET LIST@length         = 2001
103 LET LIST@set            = 3001
104 LET LIST@push           = 4001
105 LET LIST@pop            = 5001
106 LET LIST@remove         = 6001
107 LET LIST@addBetween     = 7001

200 REM Init array list
201 ARRAY LIST@list, 1
202 REM Temp data
203 LIST@list[0] = "h"
204 LIST@list[1] = "e"
205 LIST@list[2] = "j"
206 LIST@list[3] = "!"
250 LET param               = 0

1000 GOTO 2000
1001 REM function, get array value by key
1002 PRINT LIST@list[param]
1900 RETURN

2000 GOTO 3000
2001 REM function, length array length
2002 LET array = param1
2003 PRINT array
2900 RETURN

3000 GOTO 4000
3001 REM function, set array value by key
3002 LET array = param1
3003 PRINT array
3900 RETURN

4000 REM code testing
4001 PRINT "start gosub"
4002 param = 0
4010 GOSUB get
4020 PRINT "end"