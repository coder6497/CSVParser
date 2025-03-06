#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;

namespace py = pybind11;


vector<vector<string>> read_file(string filename, char delimeter)
{
    vector<vector<string>> data;
    if (delimeter == ',' || delimeter == ';')
    {
        ifstream in(filename);
        string read;
        while (getline(in, read))
        {
            vector<string> row;
            string elem;
            stringstream ss(read);
            while (getline(ss, elem, delimeter))
            {
                row.push_back(elem);
            }
            data.push_back(row);
        }
        in.close();
        return data;
    }
    else
    {
        cout << "Wrong format for delimeter" << endl;
    }
    return data;
}

map<string, vector<string>> convert_to_map(vector<vector<string>> data_table)
{
    map<string, vector<string>> map_data;
    if (!data_table.empty())
    {
        vector<vector<string>> transvec(data_table[0].size(), vector<string>(data_table.size()));
        for (int i = 0; i < data_table.size(); i++)
        {
            for (int j = 0; j < data_table[i].size(); j++)
            {
                transvec[j][i] = data_table[i][j];
            }
        }
        for (int i = 0; i < transvec.size(); i++)
        {
            vector<string> without_first_el = transvec[i];
            without_first_el.erase(without_first_el.begin());
            map_data[transvec[i][0]] = without_first_el;
        }
        return map_data;
    }
    else
    {
        cout << "Vector is empty" << endl;
    }
    return map_data;
}


bool isNumber(const std::string& str) 
{
    std::stringstream ss(str);
    double doubleValue;
    ss >> doubleValue;
    return ss.eof() && !ss.fail();
}

map<string, string> get_values(map<string, vector<string>> data_map, string key_t)
{
    map<string, string> data;
    auto it = data_map.find(key_t);
    if (it != data_map.end())
    {
        auto min = *min_element(data_map[key_t].begin(), data_map[key_t].end());
        auto max = *max_element(data_map[key_t].begin(), data_map[key_t].end());
        long double sum = 0, mid;
        for (int i = 0; i < data_map[key_t].size(); i++)
        {
            if (isNumber(data_map[key_t][i]))
            {
                sum += stod(data_map[key_t][i]);
                mid = sum / data_map[key_t].size();
            }
        }
        data["Min element"] = min;
        data["Max element"] = max;
        data["Sum(is number)"] = to_string(sum);
        data["Element count"] = to_string(data_map[key_t].size());
        data["Middle element(if number)"] = to_string(mid);
        return data;
    }
    else
    {
        cout << "Wrong data" << endl;
    }
    return data;

}

PYBIND11_MODULE(csvparse, m)
{
    m.doc() = "csvparse plugin";
    m.def("get_data_table", &read_file, "function which get data table from file");
    m.def("get_dict_from_table", &convert_to_map, "function which get dictonaty grom data table");
    m.def("get_parse_result", &get_values, "function which get result from data processing");
}