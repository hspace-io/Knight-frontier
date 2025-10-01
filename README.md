# Knights Frontier CTF

## 커밋 방법

1. clone
2. `git checkout -b [브랜치 이름]`
3. 문제 파일 업로드
4. `git add * && git commit -m "[커밋 명]"`
5. `git push origin [브랜치 이름]`
6. 그리고 `Pull Requests` 수행

## 문제 폴더 구조

- `[category-challenge_name]` # 예) pwnable 분야면 pwn-challenge
  - `prob/` # 문제 전체 소스코드 및 배포 파일이 담기는 폴더
    - `for_organizer` # 문제 전체의 파일 폴더 ( Dockerfile, docker-compose.yml, Binary, payload 등 )
    - `for_user` # 사용자 배포 파일 폴더 ( 사용자에게만 주어질 문제 파일 )
  - `exploit/` # 익스플로잇 코드 폴더 ( payload )
  - `challenge.yml` # yml 구조에 맞춰 작성
  - `README.md` # 상세한 문제 설명과 풀이

## challenge.yml 포맷

[yaml 문법 cheatsheet](https://quickref.me/yaml.html)

레포 내 challenge.yml 파일 참조 (내용 기입 후 주석은 지워주세요.)

```yaml
name: challenge #문제이름
category: pwn # 문제 분야 (pwn, web, rev, forensic, crypto, misc, ai, web3)
difficulty: medium # 난이도: beginner, easy, medium, hard (자신이 생각하는 난이도로 적어주세요)
port: ~~~~
# 포트가 여러개 일시 - 배열로 작성:
# - 1111
# - 2222
tags: # 문제 컨셉
- ROP
- ARM
description: |
challenge_description
flag: HSKF{test_flag} #플래그
chall_dir: pwn-challenge #문제 폴더 (최상위 폴더 이름 기준으로 작성)
compose_file: pwn-challenge/prob/for_organizer/docker-compose.yml #문제 도커 컴포즈 파일 위치 (상대 경로로 작성)
```

## README.md 포맷

```
# 출제자
- 나이츠

# 컨셉
- ROP, Tcache Poisoning (중요한 기법 및 컨셉 표기)

# 풀이
ROP 기법을 사용하는 문제.
func()에서 BOF가 터져서 return address overwrite가 가능하다
ROP를 통해 system('/bin/sh')를 실행하면 쉘을 딸 수 있다

# 플래그
- flag{aaa}
```
