// Copyright 2023 Yuqi Jin yuqijin8@bu.edu
// Copyright 2023 Shivam Goyal sgoyal15@bu.edu

#include <iostream>
#include <vector>
#include <map>
#include <stdexcept>
#include <fstream>
#include <string>
#include <iomanip>
#include "json.hpp"
using nlohmann::json;
using std::cout;

// part 1
std::vector<std::string> translate(const std::vector<std::string> msg, const std::map<std::string, std::string> convert) {
    std::vector<std::string> ans_list;

    for (const auto str: msg) {
        try {
            if (convert.find(str) != convert.end()) {
                ans_list.push_back(convert.at(str));
            } else {
                ans_list.push_back(str);
            }
        } catch (...) {
            if (convert.empty()) {
                for (const auto& element : msg) {
                    ans_list.push_back(element);
                }
            }
        }
    }
    return ans_list;
}
// int main() {
//     const std::vector<std::string> message = {"I", "am", "Paul"}; // Use string literals instead of integers
//     const std::map<std::string, std::string> convert = {};

//     std::vector<std::string> translated = translate(message, convert);

//     for (const auto& word : translated) {
//         std::cout << word << " ";
//     }
//     std::cout << std::endl;

//     return 0;
// }

// Part 2
class SmartBulb {
public:
    SmartBulb(const std::array<int, 4>& ip, int port) {
        if (!isValidIP(ip)) {
            throw std::invalid_argument("IPv4 address must be a 4-tuple of 8-bit integers");
        }
        if (!isValidPort(port)) {
            throw std::invalid_argument("Port number must be an int16 value [0, 65535]");
        }

        this->ip = ip;
        this->port = port;
        this->lightState = "undeclared";
        this->brightnessLevel = 0.0;
    }
    // turn on
    void on() {
        lightState = "on";
    }
    // turn off
    void off() {
        lightState = "off";
    }

    void dim(double brightness) {
        if (!isValidBrightness(brightness)) {
            throw std::invalid_argument("Brightness value must be [0,1]");
        }
        lightState = "dim";
        brightnessLevel = brightness;
    }

    double brightness() const {
        if (lightState == "on") {
            return 1.0;
        } else if (lightState == "dim") {
            return brightnessLevel;
        } else {
            return 0.0;
        }
    }

    operator bool() const {
        if (lightState == "on" || lightState == "dim") {
            return true;
        } else if (lightState == "off") {
            return false;
        } else {
            throw std::logic_error("Light state is undeclared");
        }
    }

private:
    std::array<int, 4> ip;
    int port;
    std::string lightState;
    double brightnessLevel;

    bool isValidIP(const std::array<int, 4>& ip) const {
        for (const auto& octet : ip) {
            if (!(0 <= octet && octet <= 255)) {
                return false;
            }
        }
        return true;
    }

    bool isValidPort(int port) const {
        return 0 <= port && port <= 65535;
    }

    bool isValidBrightness(double brightness) const {
        return 0 <= brightness && brightness <= 1;
    }
};



// part 3
std::string lstrip(const std::string& s, char characterToStrip) {
    size_t start = 0;
    while (start < s.size() && s[start] == characterToStrip) {
        start++;
    }
    return s.substr(start);
}
struct Dataframe {
  int sl;
  std::string id;
  std::string last;
  std::string first;
  std::string middle;
};
struct FinalDataframe {
  std::string id;
  std::string last;
  std::string first;
  std::string middle;
};

std::string student_merge(std::string fname, int* p_n_students) {
  json j;
  std::ifstream jin;
  jin.open(fname);
  jin >> j;

  int arr_size = j.size();
  int sl = 0;

  std::string id_arr[arr_size];
  std::vector<Dataframe> data;
  std::map<int, std::string> ids;

  for (int i = 0; i < arr_size; i++) {
      std::string temp_str = j[i][0];
    if(temp_str[1]== '0'){
      temp_str = temp_str.substr(1);
      temp_str = lstrip(temp_str,'0');
      temp_str = 'u' + temp_str;
    }

    if (j[i].size() == 4) {
      data.push_back({sl, temp_str, j[i][1], j[i][2], j[i][3]});
    }
    else {
      data.push_back({sl, temp_str, j[i][1], j[i][2], ""});
    }
    id_arr[i] = temp_str;
    ids[sl] = temp_str;
    sl++;
  }

  std::unordered_map<std::string, int> lastOccurrences;

    // Iterate through the original map and update the last occurrences
  for (auto it = ids.begin(); it != ids.end(); ++it) {
      lastOccurrences[it->second] = it->first;
  }

    // Rebuild the map with only the last occurrences
  std::map<int, std::string> resultMap;
  for (const auto& entry : ids) {
      if (entry.first == lastOccurrences[entry.second]) {
          resultMap[entry.first] = entry.second;
      }
  }
  // Formatting to U-xxx-yyy-zzz format
  for (auto it = resultMap.begin(); it != resultMap.end(); ++it) {
        int len = it->second.length();
        int target = 10 - len;
        std::string pad(target, '0');
        std::string fs = "U" + pad + it->second.substr(1);
        std::string id = fs.substr(0, 4) + '-' + fs.substr(4, 3) + '-' + fs.substr(7);
        it->second = id;
  }

  std::vector<FinalDataframe> df;

  //Removing duplicates and only keeping the values added last along with the rest.
  for (const auto& record : data) {
    int slValue = record.sl;
    auto it = resultMap.find(slValue);
    if (it != resultMap.end()) {
      df.push_back({resultMap[slValue], record.last, record.first, record.middle});
    }
  }

  *p_n_students = df.size();        //Final Count of the df
  json student_df;
  for(const auto& student : df) { 
    student_df.push_back({
      {"id", student.id},
      {"last", student.last},
      {"first", student.first},
      {"middle", student.middle}
    });
  }
  std::string student_database = student_df.dump();     //JSON of the df
  
  jin.close();
  return student_database;
}

