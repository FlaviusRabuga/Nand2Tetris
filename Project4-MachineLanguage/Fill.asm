// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.


// Pseudocode solution:
// label INFINITE_LOOP
//     if (key_pressed == 0):
//         fill_with = 0
//     else:
//         fill_with = -1

//     iterator = SCREEN
//     label FILL_LOOP
//         if (iterator >= KBD):
//             jump to END_FILL_LOOP
//         else:
//             RAM[iterator] = fill_with
//             iterator ++
//             jump to FILL_LOOP
//     label END_FILL_LOOP

//     jump to INFINITE_LOOP


(INFINITE_LOOP)
    // if (key_pressed == 0):
    @KBD
    D=M
    @SET_FILL_TO_0
    D;JEQ

    // fill_with = -1
    @fill_with
    M=-1
    @END_KEYBOARD_READ
    0;JMP

    // fill_with = 0
    (SET_FILL_TO_0)
    @fill_with
    M=0

    (END_KEYBOARD_READ)

    // iterator = SCREEN
    @SCREEN
    D=A
    @iterator
    M=D

    (FILL_LOOP)
        // if (iterator >= KBD) jump to END_FILL_LOOP
        @iterator
        D=M
        @KBD
        D=D-A
        @END_FILL_LOOP
        D;JGE

        // RAM[iterator] = fill_with
        @fill_with
        D=M
        @iterator
        A=M
        M=D

        // iterator ++
        @iterator
        D=M+1
        M=D

        @FILL_LOOP
        0;JMP

    (END_FILL_LOOP)

@INFINITE_LOOP
    0;JMP
