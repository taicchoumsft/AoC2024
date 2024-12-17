#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>

using namespace std;

int64_t solution1(vector<int64_t>& arr1) {
    return 0;
}

int64_t solution2(vector<int64_t>& arr1) {
    return 0;
}

int main(int argc, char** argv) {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ifstream file(argv[1]);

    if (!file.is_open()) {
        cout << "File not found" << endl;
        return 0;
    }

    int64_t list1;
    vector<int64_t> arr1;

    while (file >> list1) {
        arr1.push_back(list1);
    }

    cout << "Solution 1: " << solution1(arr1) << endl;
    cout << "Solution 2: " << solution2(arr1) << endl;

    return 0;
}
