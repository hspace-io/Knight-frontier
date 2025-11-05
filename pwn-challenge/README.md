# 출제자
- 박정우

# 컨셉
- **UAF**, **environ**, shellcode, OOB  

# 풀이
## 코드로 확인되는 취약점
### OOB
create_mission 함수에서 MISSION_CLASS ,PRIORITY_CLASS에 관한 정보를 입력할 때 범위를 제한하는 코드가 존재하지 않아서 OOB가 가능하다. <br>
이를 print_mission 함수를 통해 OOB된 값을 읽어올 수 있어 libc_base를 구할 수 있는 단서와 random_key 값을 가져올 수 있다.

### UAF
Mission, Admin 구조체의 크기가 같다. <br>
-> 만약 Mission이 free가 되면 같은 주소에 Admin이 free된 주소에 그대로 할당된다. <br>
delete_mission을 보면 free를 하고 NULL로 초기화를 하지 않아 기존에 있던 값이 그대로 남아 이를 이용해서 Exploit을 진행할 수 있다. 

### 풀이과정
1. codename에 shellcode를 입력한다.
2. create_mission, print_mission을 통해서 위에서 언급한 OOB를 사용해서 random_key와 libc_base를 구한다.
3. 그 후에 123456789을 입력해서 Admin 메뉴로 넘어간다. 
4. Admin 메뉴에 manage_mission을 사용해서 libc_base를 통해 얻은 environ 주소를 넣어서 그 안에 값을 구한다. 
5. environ의 값에는 스택 주소가 있기 때문에 이를 통해서 codename 주소를 구한다.
6. create_mission 함수에서 key에 codename을 넣고 다시 delete_mission을 한다.
-> 이 때 key에 넣을 때 random_key와 XOR연산한 값을 넣어야 한다. 
7. 그 admin_create 함수를 사용하면 exploit에 성공한다. 

# 플래그
- HSKF{W4KU_W4KU}