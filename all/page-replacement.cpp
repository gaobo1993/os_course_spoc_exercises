#include <cstdio>
#include <cstring>

using namespace std;

#define T 2
#define PAGE_SIZE 5

bool pages[PAGE_SIZE];
bool use[PAGE_SIZE];

int last = -1;
int visitNo = 0;

void process(int pageno) {
    ++visitNo;
    use[pageno] = true;
    if (pages[pageno]) {
        printf("Access page %d.\n", pageno);
        return;
    }

    if ((last < 0) || ((visitNo - last)<=T)) {
        pages[pageno] = true;
        printf("Add %d into set.\n", pageno);
        last = visitNo;
        return;
    }
    printf("page ");
    for (int i=0; i<PAGE_SIZE; i++) {
        if (pages[i] && !use[i]) printf("%d ", i);
        pages[i] = use[i];
        use[i] = false;
    }
    printf("replaced.\n");
    last = visitNo;
    return;
}
int main() {
    freopen("page-replacement.txt", "r", stdin);
    pages[0] = true;
    pages[3] = true;
    pages[4] = true;
    pages[1] = pages[2] = false;
    memset(use, 0, sizeof(use));
    int pageno;
    while (scanf("%d", &pageno) != EOF) {
        process(pageno);
    }
    return 0;
}
