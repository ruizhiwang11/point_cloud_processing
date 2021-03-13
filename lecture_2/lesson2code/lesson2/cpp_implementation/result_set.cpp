#include "result_set.hpp"

KNNResultSet::KNNResultSet(int capacity) : m_capacity{capacity},
                                           m_count{0},
                                           m_worstDist{2147483647.0},
                                           m_comparisionCounter{0},
                                           m_distIndexList{[this] {
                                               std::vector<DistIndex*> distList;
                                               distList.reserve(m_capacity);
                                               for (int i = 0; i < distList.size(); i++)
                                               {
                                                   auto tmpDist = DistIndex(m_worstDist, 0);
                                                   distList[i] = &tmpDist;
                                               }
                                               return distList;
                                           }()}
{
}

int KNNResultSet::size()
{
    return m_count;
}

bool KNNResultSet::full()
{
    return m_count == m_capacity;
}

double KNNResultSet::worstDist()
{
    return m_worstDist;
}

void KNNResultSet::addPoint(double dist, int index)
{
    m_comparisionCounter++;
    if (dist > m_worstDist)
        return;
    if (m_count < m_capacity)
        m_count++;
    int i = m_count - 1;
    while (i > 0)
    {
        if (m_distIndexList[i - 1]->getDistance() > dist)
        {
            m_distIndexList[i] = m_distIndexList[i - 1];
            i--;
        }
        else
        {
            break;
        }
    }
    m_distIndexList[i]->setDistance(dist);
    m_distIndexList[i]->setIndex(index);
    m_worstDist = m_distIndexList[m_capacity - 1]->getDistance();
}

RadiusNNResultSet::RadiusNNResultSet(int radius) : m_radius{radius},
                                                   m_count{0},
                                                   m_worstDist{static_cast<double>(m_radius)},
                                                   m_comparisionCounter{0},
                                                   m_distIndexList{[this] {
                                                       std::vector<DistIndex*> distList(0);
                                                       return distList;
                                                   }()}
{
}

int RadiusNNResultSet::size()
{
    return m_count;
}


double RadiusNNResultSet::worstDist()
{
    return m_worstDist;
}

void RadiusNNResultSet::addPoint(double dist, int index)
{
    m_comparisionCounter++;
    if (dist > m_worstDist)
        return;
    m_count++;
    auto tmpDist = DistIndex(dist, index);
    m_distIndexList.emplace_back(&tmpDist);
}