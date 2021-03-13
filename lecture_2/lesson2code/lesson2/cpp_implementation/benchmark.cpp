#include <iostream>
#include <vector>
#include <array>
#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>
#include <eigen3/Eigen/Core>
#include "result_set.hpp"
using namespace std;
using namespace boost::filesystem;

KNNResultSet bruteForceSearch(std::vector<Eigen::Vector3f> pointCloudData,KNNResultSet& resultSet, Eigen::Vector3f query)
{

}

int main(int argc, char** argv)
{
    namespace po = boost::program_options;
    po::options_description desc("benchmark testing for the kdtree octree and brute force");
    po::variables_map vm;
    desc.add_options()
        ("help,h", "produce help message")
        ("input-bin-file,i", po::value<std::string>(), "Input binfile");
    po::store(po::parse_command_line(argc, argv, desc), vm);

    path inputFile{vm["input-bin-file"].as<string>()};
    if(!exists(inputFile)){
        cout<<"PLEASE provide a valid bin file" << std::endl;
    }
    // read the point cloud data
    float f;
    std::ifstream fin(inputFile.c_str(), std::ios::binary);
    fin.seekg(0, std::ios::end);
    const size_t num_elements = fin.tellg() / sizeof(float);
    fin.seekg(0, std::ios::beg);      
    std::vector<float> data(num_elements);
    
    fin.read(reinterpret_cast<char*>(&data[0]), num_elements*sizeof(float));
    std::vector<Eigen::Vector3f> pointCloudData;
    for(size_t i = 0; i < data.size(); i = i+4)
    {
       Eigen::Vector3f tmpArr{data[i],data[i+1],data[i+2]};
       pointCloudData.emplace_back(tmpArr);
    }

    cout << "brute force search: " << endl;
    for(int i =0; i < pointCloudData.size();i++){
        auto resultSet = KNNResultSet(8);
        brute
    }


}
