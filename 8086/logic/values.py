registers = {
    'ah': "00", 'al': "00",
    'bh': "00", 'bl': "00",
    'ch': "00", 'cl': "00",
    'dh': "00", 'dl': "00",
    # 'ss': "0000", 'ds': "0000", 
    # 'es': "0000",
    # 'sp': "0000", 'bp': "0000", 
    # 'si': "0000", 'di': "0000"
}

flags = {
    'CF': 0,  # Carry Flag
    'ZF': 0,  # Zero Flag
    'SF': 0,  # Sign Flag
    'OF': 0,  # Overflow Flag
    'PF': 0,  # Parity Flag
    'AF': 0,  # Auxiliary Flag
    'IF': 1,  # Interrupt enable Flag
    'DF': 0   # Direction Flag
}


# Carry Flag (CF) - this flag is set to 1 when there is an unsigned overflow. 
# For example when you add bytes 255 + 1 (result is not in range 0...255). When there is no overflow this flag is set to 0.
# Zero Flag (ZF) - set to 1 when result is zero.
# Sign Flag (SF) - set to 1 when result is negative. When result is positive it is set to 0. 
# Actually this flag take the value of the most significant bit.
# Overflow Flag (OF) - set to 1 when there is a signed overflow. For example, when you add bytes 100 + 50 (result is not in range -128...127).
# Parity Flag (PF) - this flag is set to 1 when there is even number of one bits in result, and to 0 when there is odd number of one bits. 
# Even if result is a word only 8 low bits are analyzed!
# Auxiliary Flag (AF) - set to 1 when there is an unsigned overflow for low nibble (4 bits).
# Interrupt enable Flag (IF) - when this flag is set to 1 CPU reacts to interrupts from external devices.
# Direction Flag (DF) - this flag is used by some instructions to process data chains, 
# when this flag is set to 0 - the processing is done forward, when this flag is set to 1 the processing is done backward.

is_userinput_21h = '0'
is_screen = '0'
userInput = ''
screenContent = ''
being_in_data_segment = '0'
codeData = []  # [data_name, type (db/dw), value, len]
leastr = ''
is_animation_running = '0'

predefined_codes = {
    "funny regex": [
        "MoV Al, 3H",
        "MOv bL 13",
        "AdD aL, BL"
    ],
    "check flags update and negative outcome handle": [
        "MOV AL, 3h",
        "MOV BL, 13",
        "SUB AL, BL"
    ],
    "perform animation": [
        "MOV BL, 06H",
        "MOV CL, 05H",
        "ADD BL, CL"
    ],
    "Get a character and print": [
        ".Model Small",
        ".Stack 100H",
        ".Data",
        "   crlf db 13, 10, '$'",
        "   char db ?",
        ".Code",
        "Main Proc",
        "   mov ax, @data",
        "   mov ds, ax",
        "",
        "   mov ah, 1",
        "   int 21h",
        "   mov char, al",
        "",
        "   mov ah, 9",
        "   lea dx, crlf",
        "   int 21h",
        "",
        "   mov dl, char",
        "   mov ah, 2",
        "   int 21h",
        "",
        "   mov ah, 4ch",
        "   int 21h",
        "Main endp",
        "END MAIN"
    ],
    "Get string and print": [
        ".model small",
        ".stack 100",
        ".data",
        "msg1 db 'enter a string below: $'",
        "msg2 db 'the string is: $'",
        "CRLF db 13, 10, '$'",
        "str  db 100 dup('$')",
        ".code",
        "MAIN proc",
        "    mov ax, @data",
        "    mov ds, ax",
        "",
        "    mov ah, 9",
        "    lea dx, msg1",
        "    int 21h",
        "",
        "    mov ah, 10",
        "    lea dx, str",
        "    int 21h",
        "",
        "    mov ah, 9",
        "    lea dx, CRLF",
        "    int 21h",
        "    lea dx, msg2",
        "    int 21h",
        "",
        "    lea dx, str + 2",
        "    int 21h",
        "",
        "    mov ah, 4ch",
        "    int 21h",
        "MAIN endp",
        "end"
    ],
    "Get a character and print its uppercase": [
        ".Model Small",
        ".Stack 100H",
        ".Data",
        "    crlf db 13, 10, '$'",
        "    dis db 32",
        "    char db ?",
        ".Code",
        "Main Proc",
        "    mov ax, @data",
        "    mov ds, ax",
        "",
        "    mov ah, 1",
        "    int 21h",
        "    sub al, dis",
        "    mov char, al",
        "",
        "    mov ah, 9",
        "    lea dx, crlf",
        "    int 21h",
        "",
        "    mov dl, char",
        "    mov ah, 2",
        "    int 21h",
        "",
        "Main endp",
        "END MAIN"
    ],
    "chao tay chao ta": [
        ".Model Small",
        ".Stack 100",
        ".Data",
        "    CRLF    DB 13, 10, '$'",
        "    chaotay DB 'hello there!$'",
        "    chaota  DB 'chao ban!$'",
        ".Code",
        "MAIN Proc",
        "    MOV AX, @Data",
        "    MOV DS, AX",
        "",
        "    MOV AH, 9",
        "    LEA DX, chaotay",
        "    INT 21H",
        "",
        "    LEA DX, CRLF",
        "    INT 21H",
        "",
        "    LEA DX, chaota",
        "    INT 21H",
        "",
        "    MOV AH, 4CH",
        "    INT 21H",
        "MAIN Endp",
        "END MAIN"
    ]
}
