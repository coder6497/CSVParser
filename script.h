#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>
#include <chrono>

using namespace std;

vector<vector<string>> read_file(string, char);
map<string, vector<string>> convert_to_map(vector<vector<string>>);
bool isNumber(const std::string&);
map<string, string> get_values(map<string, vector<string>>, string);
void print_data(map<string, vector<string>>, map<string, string>);
