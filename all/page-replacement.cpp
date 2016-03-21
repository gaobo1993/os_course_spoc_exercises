#include <cstdio>
#include <vector>
using namespace std;

#define SIZE 2
#define TOTAL 5

bool pages[TOTAL];
bool use[TOTAL];
int last = -1;

void process(int order, int pageno) {
    use[pageno] = true;
    if (pages[pageno]) {
        printf("Access page %d.\n", pageno);
        return;
    }

    if ((last < 0) || ((order - last)<=SIZE)) {
        pages[pageno] = true;
        printf("Add into set %d.\n", pageno);
        last = order;
        return;
    }
    for (int i=0; i<TOTAL; i++) {
        if (pages[i] && !use[i]) printf("%d ", i);
        pages[i] = use[i];
        use[i] = false;
    }
    printf(" replaced.\n");
    last = order;
    return;
}
int main() {
    freopen("page-replacement.txt", "r", stdin);
    pages[0] = true;
    pages[3] = true;
    pages[4] = true;
    pages[1] = pages[2] = false;
    for (int i=0; i<TOTAL; i++) use[i] = false;
    int pageno, order;
    order = 0;
    while (scanf("%d", &pageno) != EOF) {
        process(++order, pageno);
    }
    return 0;
}
