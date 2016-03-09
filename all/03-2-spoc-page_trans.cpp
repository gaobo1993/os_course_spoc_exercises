#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cstring>

using namespace std;

char memory[128][32];

void readmemory() {
    string s1, s2;
    for (int i=0; i<0x80; i++) {
        cin >> s1 >> s2;
        for (int j=0; j<32; j++) {
            int temp;
            cin >> hex >> temp;
            memory[i][j] = char(temp);
        }
    }
}
int PDBR = 0x220;
char getmemory(int addr) {
    int page = (addr & 0x00000fe0) >> 5; // 第6到第12位, 2^7 = 128
    int pos = (addr & 0x0000001f); // 第1到第5位, 2^5 = 32
    return memory[page][pos];
}
void transfer(int va) {
    int pd = (va & 0x00000c00) >> 10; // 第11到第12位
    int pteOffset = (va & 0x000003e0) >> 5; // 第6到第10位
    int pageOfffset = (va & 0x0000001f); // 第1到第5位

    char pde = getmemory(PDBR+pd);
    int pde_v = pde >> 7;
    int pde_c = pde & 0x0000007f;

    int pte = memory[pde_c][pteOffset];
    int pte_v = pte >> 7;
    int pte_c = pte & 0x0000007f;

    int phyaddr = (pte_c << 5) + pageOfffset;

    cout << "Virtual Address 0x" << hex << setw(4) << va << ":" << endl;
    cout << "  --> pde index:0x" << hex << setw(2) << setfill('0') << pd;
    cout << "  pde contents:(valid " << pde_v << ", pfn 0x" << hex << setw(2) << setfill('0') << pde_c << ")" << endl;
    if (pde_v == 0) {
        cout << "      --> Fault (page directory entry not valid)" << endl;
        return;
    }
    cout << "     --> pte index:0x" << hex << setw(2) << setfill('0') << pteOffset;
    cout << " pte contents:(valid " << pte_v << ", pfn 0x" << hex << setw(2) << setfill('0') << pte_c << ")" << endl;
    if (pte_v == 0) {
        cout << "        --> Fault (page table entry not valid)" << endl;
        return;
    }
    cout << "       --> Translate to Physical Address 0x" << hex << phyaddr;
    cout << " --> Value:0x" << hex << setw(2) << (int)getmemory(phyaddr) << endl;
}

int main() {
    freopen("03-2-spoc-input.txt", "r", stdin);
    readmemory();
    string s1, s2;
    int vaddr;
    while (cin >> s1 >> s2 >> hex >> vaddr) {
        transfer(vaddr);
        cout << endl;
    }
    return 0;
}
