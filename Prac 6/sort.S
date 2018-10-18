/*
EEE3096S Prac 6
Sort (assembly implementation of in place selection sort)
Jonah Swain [SWNJON003]

Register use:
R0 - address of output string (for printf)
R1 - address of output number (for printf)

R4 - address of array of numbers
R5 - size of array of numbers
R6 - outer loop offset (address of number to swap)
R7 - inner loop offset (address of current number to compare)
R8 - current number to compare
R9 - offset of smallest number (in current loop iteration)
R10 - smallest number (in current loop iteration)
R11 - number to swap
*/

.data @ data section
numbers:
.word 5, 3, 6, 34, 2, 6, 9, 1 @ numbers to sort
num_numbers:
.word 8 @ number of numbers to sort
out_str_unsorted:
.asciz "Unsorted numbers:\n"
out_str_sorted:
.asciz "Sorted numbers:\n"
out_str_number:
.asciz "%d\n"

.text @ code section

.global main
main:
  push {ip, lr} @ push link register to stack
  @ load initial register values
  LDR R4, =numbers @ load address of numbers array into R4
  LDR R0, =num_numbers @ load address of num_numbers into R0
  LDR R5, [R0] @ load size of numbers array into R5
  LSL R5, R5, #2 @ multiply R5 by 4 (left shift by 2) to get the memory size of the numbers array
  SUB R5, R5, #4 @ subtract 4 from R5 to get the maximum offset of the numbers array
  MOV R6, #0 @ load 0 into R6
  MOV R7, #0 @ load 0 into R7
  @ print heading for unsorted numbers
  LDR R0, =out_str_unsorted @ load string into R0
  BL printf @ branch to printf
print_numbers:
  MOV R0, =out_str_number @ load output string address into R0
  LDR R1, [R4, R7] @ load current number from numbers into R1 (address R4 + offset R7)
  BL printf @ branch to printf
  CMP R7, R5 @ compare current offset to size of numbers array
  ADD R7, R7, #4 @ increment current offset by one word
  BLT print_numbers @ branch to print_numbers if R7 < R5 (loop if more numbers to print)
  MOV R7, #0 @ load 0 into R7
outer_loop:
  MOV R10, #255 @ reset the current smallest number to 255
  MOV R7, R6 @ copy outer loop offset to inner loop offset
  MOV R9, R6 @ copy outer loop offset to smallest number offset (in event no smaller numbers are found it wont swap some arbitrary memory)
inner_loop:
  LDR R8, [R4, R7] @ load current number to compare into R8
  CMP R8, R10 @ compare current number and smallest number
  BLT set_smallest @ branch to set smallest number
continue_inner:
  CMP R7, R5 @ compare current offset to size of numbers array
  ADD R7, R7, #4 @ increment current offset by one word
  BLT inner_loop @ branch to inner loop if R7 < R5 (more numbers to compare)
continue_outer:
  BL swap_smallest @ swap the smallest number with the current number
  CMP R6, R5 @ compare current offset to size of numbers array
  ADD R6, R6, #4 @ increment current offset by one word
  BLT outer_loop @ branch to outer loop if R6 < R5 (more iterations required)
print_sorted_header:
  LDR R0, =out_str_sorted @ load output string address into R0
  BL printf @ branch to printf
  MOV R7, #0 @ load 0 into R7
print_sorted_numbers:
  MOV R0, =out_str_number @ load output string address into R0
  LDR R1, [R4, R7] @ load current number from numbers into R1 (address R4 + offset R7)
  BL printf @ branch to printf
  CMP R7, R5 @ compare current offset to size of numbers array
  ADD R7, R7, #4 @ increment current offset by one word
  BLT print_sorted_numbers @ branch to print_numbers if R7 < R5 (loop if more numbers to print)
exit:
  @ exit procedure
  mov R0, #0 @ set R0 to 0
  mov R1, #0 @ set R1 to 0
  pop {ip, lr} @ pop link register from stack
set_smallest:
  @ set new smallest number
  MOV R10, R8 @ move the compared number into R10
  MOV R9, R7 @ move the compared number address into R9
  BX lr @ return
swap_smallest:
  LDR R11, [R4, R6] @ load number to swap into R11 (address R4 + offset R6)
  LDR R10, [R4, R9] @ load the smallest number into R10 (address R4 + offset R9)
  STR R11, [R4, R9] @ store the number to swap in the position of the smallest number
  STR R10, [R4, R6] @ store the smallest number in the position of the number to swap