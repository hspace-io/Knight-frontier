# 출제자
- 최정우(ch01)

# 컨셉
- Heap overflow , Integer underflow , shellcode , OOB

# 풀이
syscall 의 getdents 를 이용하여 디렉토리의 정보를 읽은 후 flag 파일을 open , read , write 를 이용하여 출력하는 문제.
create_note 에서 index로 10이 입력이 가능하다. 그렇게 heap 을 할당해주면 name 영역에 할당하게 되어 heap leak 이 가능하다.
이후 
edit_note 와 create_note 의 
```read(0, notes[idx]->buf, (notes[idx]->size)-1); 
```
부분에서 이전에 size 를 사용자가 입력하기에 0을 size로 입력하면 integer underflow 가 일어나서 많은 양의 입력이 가능하다 (Heap overflow)
이후 edit_note 를 통해 구조체 내의 * 를 덮기가 가능하다. 이를 통해 aar , aaw 를 만들 수 있다.
그렇게 rwx 영역의 주소를 획득, rwx 에 쓰기가 가능한 포인터를 만든 후 , getdents syscall 을 이용하여 디렉토리의 이름, flag 의 이름을 얻은 후 
open, read, write 를 이용해 flag를 출력하는 문제이다.

# 플래그
- HSKF{p1z_1eak_urand0m_val}