// gcc ./chal.c -o chal -lseccomp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <sys/syscall.h>
#include <stddef.h>
#include <errno.h>
#include <seccomp.h>
#include <string.h>
#include <sys/mman.h>   // mmap, PROT_*, MAP_*
#include <stdint.h>     // uintptr_t
#include <fcntl.h>     // open
#include <sys/stat.h>  // mkdir
#include <sys/types.h> // pid_t
#include <time.h>     // time
#include <sys/wait.h> // waitpid

void raw_seccomp_init(void) {
    struct sock_filter filter[] = {
        /* 1. Load architecture into A */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
        /* If arch != AUDIT_ARCH_X86_64 then reject */
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* 2. Load syscall number into A */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),

        /* 3. Block execve */
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_execve, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | EACCES),

        /* 4. Block execveat */
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_execveat, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | EACCES),

        /* 5. Allow everything else */
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        perror("prctl(NO_NEW_PRIVS)");
        exit(EXIT_FAILURE);
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) != 0) {
        perror("prctl(SECCOMP)");
        exit(EXIT_FAILURE);
    }
}
typedef struct{
    unsigned int size;
    char *buf;
} note_t;

note_t * notes[10];
char name[16];
char ** buf = NULL;

void setting(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    raw_seccomp_init();
    printf("What is your name?\n");
    read(0, name, 15);
    return;
}

void printMenu(){
    printf("Hello, %s!\n", name);
    puts("1. create note");
    puts("2. edit note");
    puts("3. view note");
    puts("4. delete note");
    puts("5. execve RWX area");
    puts("6. exit");
    printf(">> ");
}


void create_note(){
    int idx;
    printf("index: ");
    if(scanf("%d", &idx) !=1 || idx < 0 || idx > 10){
        puts("Invalid input");
        return;
    }
    notes[idx] = malloc(sizeof(note_t));
    printf("size: ");
    scanf("%u", &notes[idx]->size);
    printf("content: ");
    notes[idx]->buf = malloc(notes[idx]->size);
    read(0, notes[idx]->buf, notes[idx]->size - 1);
    printf("Note %d created!\n", idx);
    return;
}

void edit_note(){
    int idx;
    printf("index: ");
    if(scanf("%d", &idx) !=1 || idx < 0 || idx > 10 || !notes[idx]){
        puts("Invalid input");
        return;
    }
    printf("content: ");
    read(0, notes[idx]->buf, (notes[idx]->size)-1);
    printf("Note %d edited!\n", idx);
    return;
}

void delete_note(){
    int idx;
    printf("index: ");
    if(scanf("%d", &idx) !=1 || idx < 0 || idx > 10 || !notes[idx]){
        puts("Invalid input");
        return;
    }
    free(notes[idx]->buf);
    free(notes[idx]);
    notes[idx] = NULL;
    printf("Note %d deleted!\n", idx);
    return;
}

void execve_rwx(){
    void (*func)() = (void (*)())*buf;
    func();
    return;
}

void view_note(){
    int idx;
    printf("index: ");
    if(scanf("%d", &idx) !=1 || idx < 0 || idx > 10 || !notes[idx]){
        puts("Invalid input");
        return;
    }
    printf("Note %d:\n%s\n", idx, notes[idx]->buf);
    return;
}

int main(){
    setting();
    puts("Hi, This is my first CTF challenge!");
    buf = malloc(sizeof(char*));
    *buf = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    while(1){
        printMenu();
        int choice;
        if(scanf("%d", &choice) != 1){
            puts("Invalid input");
            exit(1);
        }
        switch(choice){
            case 1:
                create_note();
                break;
            case 2:
                edit_note();
                break;
            case 3:
                view_note();
                break;
            case 4:
                delete_note();
                break;
            case 5:
                execve_rwx();
                break;
            case 6:
                puts("bye~");
                exit(0);
            default:
                puts("Invalid choice");
                break;
        }
    }

}