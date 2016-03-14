#include <iostream>
#include <cstdio>
#include <cstdlib>
using namespace std;

typedef unsigned int UINT;

#define va2pde_idx(va) ((va & 0xcffc0000) >> 22)
#define pde_idx2pde_ctx(pde_idx) (((pde_idx - 0x300 + 1) << 12)+0x3)
#define va2pte_idx(va) ((va & 0x003ff000) >> 12)
#define pa2pte_ctx(pa) ((pa & 0xfffff000) | (0x3))

int main() {
    UINT va, pa;
    freopen("03-1-4-input.txt","r",stdin);
    while (scanf("va 0x%x, pa 0x%x\n", &va, &pa) != EOF)
    {
        printf("va 0x%08x, pa 0x%08x, ", va, pa);
        UINT pde_idx = va2pde_idx(va);
        printf("pde_idx 0x%08x, ", pde_idx);
        UINT pde_ctx = pde_idx2pde_ctx(pde_idx);
        printf("pde_ctx 0x%08x, ", pde_ctx);
        UINT pte_idx = va2pte_idx(va);
        printf("pte_idx 0x%08x, ", pte_idx);
        UINT pte_ctx = pa2pte_ctx(pa);
        printf("pte_ctx 0x%08x\n", pte_ctx);
    }
    return 0;
}
