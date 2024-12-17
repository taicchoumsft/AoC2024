#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <unordered_map>

using namespace std;

int64_t solution1(vector<int64_t>& arr1, vector<int64_t>& arr2) {
    sort(arr1.begin(), arr1.end());
    sort(arr2.begin(), arr2.end());

    int64_t diff = 0;

    for (int i=0; i<arr1.size(); ++i) {
        diff += abs(arr1[i] - arr2[i]);
    }
    return diff;
}

int64_t solution2(vector<int64_t>& arr1, vector<int64_t>& arr2) {
    unordered_map<int64_t, int64_t> cnt2;
    for (const auto& a: arr2) {
        cnt2[a]++;
    }

    int64_t total = 0;
    for (const auto& a: arr1) {
        if (cnt2.count(a)) {
            total += a * cnt2[a];
        }
    }
    return total;
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
    int64_t list2;
    vector<int64_t> arr1, arr2;

    while (file >> list1 >> list2) {
        arr1.push_back(list1);
        arr2.push_back(list2);
    }

    cout << "Solution 1: " << solution1(arr1, arr2) << endl;
    cout << "Solution 2: " << solution2(arr1, arr2) << endl;

    return 0;
}
