/*
EEE3096S Prac 6
Sort (assembly implementation of in place selection sort)
Jonah Swain [SWNJON003]

Register use:
R0 - address of sorted number string (for printf)
R4 - address of number array
R5 - current number to compare
R6 - current smallest number
R7 - offset for outer loop
R8 - offset for inner loop
R9 - offset of next uncompared number
R10 - number of numbers to sort

Reference: https://github.com/kevinhooke/ARM-ASM-SortAlgorithms/blob/master/sort.S
*/

.data @ data section
numbers:
.word @ numbers to sort
num_numbers:
.word @ number of numbers to sort
output:
.asciz "%d\n"


.text @ code section

.global main
main:
	push {ip, lr} @ push link register to stack
	@ set default values for R7, R8, R9
	MOV R7, #0
	MOV R8, #0
	MOV R9, #0
	@ load values for R4, R10
	LDR R4, =numbers
	
outer_loop:
	MOV R6, #255 @ set smallest value to 255
	MOV R8, R7 @ copy outer loop offset into inner loop offset
inner_loop: