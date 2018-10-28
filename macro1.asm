%macro add1 2
	mov ebx,%1
	mov ebx,%2
	add eax,ebx
	push eax

%endmacro

%macro add1 2
	mov eax,%1
	mov eax,%2
	sub eax,ebx
	push eax

%endmacro

%macro add2 2
	mov eax,%1
	mov eax,%2
	sub eax,ebx
	push eax

%endmacro

%macro add1 1
	mov eax,%1
	push eax
	push dword[msg2]
	call printf
%endmacro

section .data
	a   dd 10
	b   dd 20
	msg db "result=",0,10

section .bss
	c resd 1

section .text
	global main
	extern printf

main:
	mov esi,50
	mov edi,20
	add1 10,20
  add2 10,30
	add1 10
