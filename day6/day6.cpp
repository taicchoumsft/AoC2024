#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <string>
#include <utility>
#include <set>

using namespace std;

pair<int, int> next_dir(int dir_i, int dir_j) {
    int new_i, new_j;
    if (dir_i == -1 && dir_j == 0) {
        new_i = 0;
        new_j = 1;
    } else if (dir_i == 0 && dir_j == 1) {
        new_i = 1;
        new_j = 0;
    } else if (dir_i == 1 && dir_j == 0) {
        new_i = 0;
        new_j = -1;
    } else {
        new_i = -1;
        new_j = 0;
    }

    return {new_i, new_j};
}

bool path2(vector<string>& arr, int i, int j, int dir_i, int dir_j, int dim_i, int dim_j, int cnt) {
    if (i < 0 or i >= dim_i or j < 0 or j >= dim_j) {
        return false;
    };
    // heuristic loop control
    if (cnt > 10000) return true;

    //if ((i + dir_i == start_i) && (j + dir_j == start_j) && start_dir_i == dir_i && start_dir_j == dir_j) return true;

    if (i + dir_i >= 0 && i + dir_i < dim_i &&
        j + dir_j >= 0 && j + dir_j < dim_j &&
        arr[i + dir_i][j + dir_j] == '#') {
        auto [new_i, new_j] = next_dir(dir_i, dir_j);
        return path2(arr, i, j, new_i, new_j, dim_i, dim_j, cnt + 1);
    }

    return path2(arr, i + dir_i, j + dir_j, dir_i, dir_j, dim_i, dim_j, cnt + 1);
}

set<pair<int, int>> blocked_st;
set<pair<int, int>> already;

int64_t path(vector<string>& arr, int i, int j, int dir_i, int dir_j, int dim_i, int dim_j, vector<vector<bool>>& seen) {
    if (i < 0 or i >= dim_i or j < 0 or j >= dim_j) {
        int64_t total = 0;
        for (int m=0; m<dim_i; ++m) {
            for (int n=0; n<dim_j; ++n) {
                if (seen[m][n]) total++;
            }
        }
        return total;
    };

    seen[i][j] = true;
    already.insert({i, j});

    // artificially place barrier in front, then remove
    // also got to be sure to not even try to place a barrier
    // we've placed before - placing a barrier at this point
    // would interrup the flow of the guard, and will change
    // the entire flow anyway, thus double counting.
    // remember that we place this single obstruction BEFORE
    // the guard moves
    if (i + dir_i >= 0 && i + dir_i < dim_i &&
        j + dir_j >= 0 && j + dir_j < dim_j &&
        arr[i + dir_i][j + dir_j] == '.' &&
        !(already.count({i + dir_i, j + dir_j}))) {

        arr[i + dir_i][j + dir_j] = '#';

        if (path2(arr, i, j, dir_i, dir_j, dim_i, dim_j, 0)) {
            //block_cnt++;
            blocked_st.insert({i + dir_i, j + dir_j});
        }

        arr[i + dir_i][j + dir_j] = '.';
    }

    if (arr[i + dir_i][j + dir_j] == '#') {
        auto [new_i, new_j] = next_dir(dir_i, dir_j);

        return path(arr, i, j, new_i, new_j, dim_i, dim_j, seen);
    }

    return path(arr, i + dir_i, j + dir_j, dir_i, dir_j, dim_i, dim_j, seen);
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

    string list1;
    vector<string> arr;

    while (file >> list1) {
        arr.push_back(list1);
    }

    int dim_i = arr.size(), dim_j = arr[0].size();
    int start_i, start_j;

    for (int i=0; i<dim_i; ++i) {
        for (int j=0; j<dim_j; ++j) {
            if (arr[i][j] == '^') {
                start_i = i;
                start_j = j;
                break;
            }
        }
    }

    vector<vector<bool>> seen(dim_i, vector<bool>(dim_j));

    cout << "Solution 1: " << path(arr, start_i, start_j, -1, 0, dim_i, dim_j, seen) << endl;
    cout << "Solution 2: " << blocked_st.size() << endl;

    return 0;
}
