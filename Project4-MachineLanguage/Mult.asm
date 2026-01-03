// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


// Pseudocode solution:
//     R2 = 0
//     iterator = 0

//     label MULTIPLICATION_LOOP
//         if (iterator - R1) >= 0
//             jump to END_PROGRAM
//         else:
//             iterator ++
//             R2 = R2 + R0
// 		jump to MULTIPLICATION_LOOP


// initialize R2 as 0 (probably moot, but just in case)
    @0
    D=A
    @R2
    M=D

    // initialize iterator as 0 (probably moot, but just in case)
    @0
    D=A
    @iterator
    M=D

(MULTIPLICATION_LOOP)

    // stop condition (iterator - R1) >= 0 
    @iterator
    D=M
    @R1
    D=D-M
    @END_MULTIPLICATION_LOOP
    D;JGE

    // iterator ++
    @iterator
    D=M+1
    M=D

    // R2 = R2 + R0
    @R2
    D=M
    @R0
    D=D+M
    @R2
    M=D

    // jump back to the start of the loop
    @MULTIPLICATION_LOOP
    0;JMP

(END_MULTIPLICATION_LOOP)



(END_PROGRAM)
    @END_PROGRAM
    0;JMP
