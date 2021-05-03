1 REM this checks if ther is a compiled version of file.bas (file.sab) if ther is non the compile the file.bas file
2 REM save all the file.bas variabels as file
10 IMPORT "file.bas" AS file

11 REM write out a var from file 
20 PRINT file.var

21 REM call a function by the name of ADD in file
30 CALL file.ADD 
