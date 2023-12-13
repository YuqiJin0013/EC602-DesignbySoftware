// Copyright 2023 Yuqi Jin yuqijin8@bu.edu
/* TEST FOR TILE ROTATE */
#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <unordered_map>
#include <unordered_set>
// allowed includes
// tuple, utility, vector, map, set, unordered_map,
// unordered_set, algorithm

using std::cin;
using std::cout;
using std::string;
using std::vector;
void rotate(vector<string>& tile){
    int n = tile.size();
    // create a temp tile to store the rotated one
    vector <string> temp (n, std::string(n, ' '));
    // rotate counter-clock wise
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        temp[n - 1 - j][i] = tile[i][j];
      }
    }
    // Update the original vector with the rotated values from the temporary vector
    for (int i = 0; i < n; ++i) {
        tile[i] = temp[i];
    }

    // Display the rotated tile
    for (int i = 0; i < n; ++i) {
        std::cout << tile[i] << std::endl;
    }
  }
  int main() {
    // Populate the vector of strings to represent the tile
    std::vector<std::string> inputTile;
    inputTile.push_back("..*");
    inputTile.push_back("..*");
    inputTile.push_back("..*");

    rotate(inputTile);
    return 0;
}