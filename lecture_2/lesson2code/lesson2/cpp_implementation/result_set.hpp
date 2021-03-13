#include <vector>
#include <string>
#include <unordered_map>

class DistIndex
{
private:
    double m_distance;
    int m_index;

public:
    DistIndex(double distance, int index) : m_distance{distance}, m_index{index}{};
    bool operator<(const DistIndex &other)
    {
        return m_distance < other.m_distance;
    }
    double getDistance() { return m_distance; }
    int getIndex() { return m_index; }
    void setDistance(double distance) { m_distance = distance; }
    void setIndex(int index) { m_index = index; }
};

class KNNResultSet
{
private:
    int m_capacity;
    int m_count;
    double m_worstDist;
    std::vector<DistIndex*> m_distIndexList;
    int m_comparisionCounter;

public:
    KNNResultSet(int capacity);
    int size();
    bool full();
    double worstDist();
    void addPoint(double dist, int index);
};

class RadiusNNResultSet
{
private:
    int m_radius;
    int m_count;
    double m_worstDist;
    std::vector<DistIndex*> m_distIndexList;
    int m_comparisionCounter;

public:
    RadiusNNResultSet(int radius);
    int size();
    bool full();
    double worstDist();
    void addPoint(double dist, int index);
};