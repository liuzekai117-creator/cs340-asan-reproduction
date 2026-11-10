#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int));
    if (p == NULL) return 1;

    *p = 42;
    free(p);
    return *p;  // 故意读取已经释放的内存
}
