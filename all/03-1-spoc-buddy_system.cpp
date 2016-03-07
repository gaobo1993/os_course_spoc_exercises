#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>

using namespace std;

const int MIN_SIZE = 2 << 5;
const int MEM_SIZE = 2 << 10;

char memory[MEM_SIZE];

struct Node
{
	int size, addr;
	int left, right;
	int maxSize;
};

Node tree[MEM_SIZE/MIN_SIZE*2];

int nodeNum = 0;
void buildTree(int node, int size, int addr)
{
	tree[node].size = size;
	tree[node].maxSize = size;
	tree[node].addr = addr;

	size = size / 2;
	if (size < MIN_SIZE)
	{
		tree[node].left = -1;
		tree[node].right = -1;
		return;
	}
	tree[node].left = ++nodeNum;
	buildTree(tree[node].left, size, addr);
	tree[node].right = ++nodeNum;
	buildTree(tree[node].right, size, addr + size);
}

void printMemTree(int node)
{
	if (node < 0) return;
	printf("node: %d, size: %d, addr: %d, maxSize: %d\n", node, tree[node].size, tree[node].addr, tree[node].maxSize);
	if (tree[node].maxSize == 0) return;
	printMemTree(tree[node].left);
	printMemTree(tree[node].right);
}

// return -1 if fails
int malloc(int node, int size)
{
	if (size > tree[node].maxSize) return -1;

	if (size > tree[node].size / 2) // malloc here
	{
		tree[node].maxSize = 0;
		return tree[node].addr;
	}
	int ret;
	if (tree[tree[node].left].maxSize >= size) {
		ret = malloc(tree[node].left, size);
	} else if (tree[tree[node].right].maxSize >= size) {
		ret = malloc(tree[node].right, size);
	} else {
		ret = -1;
	}
	tree[node].maxSize = max(tree[tree[node].left].maxSize, tree[tree[node].right].maxSize);
	return ret;
}

// 0 for success, -1 for fail
int free(int node, int ptr)
{
	if (node < 0) return -1;
	if (tree[node].maxSize == 0 && tree[node].addr == ptr)
	{
		tree[node].maxSize = tree[node].size;
		return 0;
	}
	if (tree[node].right < 0 || tree[node].left < 0) return -1;
	int ret;
	if (tree[tree[node].right].addr > ptr) ret = free(tree[node].left, ptr);
	else ret = free(tree[node].right, ptr);
	if (tree[tree[node].left].maxSize == tree[tree[node].left].size && \
		tree[tree[node].right].maxSize == tree[tree[node].right].size) {
			tree[node].maxSize = tree[node].size;
		} else {
			tree[node].maxSize = max(tree[tree[node].left].maxSize, tree[tree[node].right].maxSize);
		}
	return ret;
}

int malloc(int size)
{
	return malloc(0, size);
}

int mfree(int ptr)
{
	return free(0, ptr);
}

int main()
{
	freopen("input", "r", stdin);
	buildTree(0, MEM_SIZE, 0);
	while (1) {
		int cmd, argv;
		// cmd: 1 for allocate, 2 for free, 0 for exit
		scanf("%d %d", &cmd, &argv);
		if (cmd == 0) break;
		else if (cmd == 1) {
			int ret = malloc(argv);
			if (ret >= 0) printf("Allocate %d mem in address %d\n", argv, ret);
			else printf("Allocate %d mem failed\n", argv);
		} else if (cmd == 2) {
			int ret = mfree(argv);
			if (argv == -1) printf("Free mem at address %d failed\n", argv);
			else printf("Free mem at address %d succeeded\n", argv);
		}
	}
	printMemTree(0);
	return 0;
}
