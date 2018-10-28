section .data
	a dd 10,20,30
	b db "ABC",10,0
section .text
	global main
main: 	
	mov eax,10
	mov ebx,20
	add eax,ebx
	mov eax,ebx
	mov eax,eax
	sub eax,ecx
	add eax,10
	add ebx,10
	sub ebx,10
	sub edi,20
	sub eax,30
	mov eax,dword[b]
	mov ebx,dword[a]
	mov ecx,dword[a]
	mov edx,dword[b]
	mov eax,a
	mov ecx,a
	mov ebx,a
	mov ecx,dword[ebx+4*1]
	mov eax,dword[eax+4*1]
	mov ebx,dword[ebx+4*1]
	add eax,ecx
