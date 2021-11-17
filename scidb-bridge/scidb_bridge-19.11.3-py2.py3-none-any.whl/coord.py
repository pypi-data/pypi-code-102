import numpy
import pandas


def get_chunk_length(dims, chunk_coords, i):
    return min(dims[i].chunk_length, dims[i].high_value - chunk_coords[i] + 1)


def coord2delta(data, dims, chunk_coords):
    n_dims = len(dims)

    if n_dims == 1:
        res = data[dims[0].name] - chunk_coords[0]
    elif n_dims == 2:
        res = ((data[dims[0].name] - chunk_coords[0])
               * get_chunk_length(dims, chunk_coords, 1)
               + data[dims[1].name] - chunk_coords[1])
    else:
        res = pandas.Series(numpy.zeros(len(data)), dtype=numpy.int64)
        for i in range(n_dims):
            res *= get_chunk_length(dims, chunk_coords, i)
            res += data[dims[i].name] - chunk_coords[i]

    df = pandas.DataFrame(res)
    df.columns = ('pos', )
    delta = df['pos'] - df.shift(1, fill_value=-1)['pos']
    return delta.to_list()


def delta2coord(data, dims, chunk_coords):
    n_dims = len(dims)
    pos = data['@delta'].copy()
    pos[0] -= 1
    pos = pos.cumsum()

    res = None
    if n_dims == 1:
        res = (pos + chunk_coords[0], )
    elif n_dims == 2:
        coord1 = pos % dims[1].chunk_length + chunk_coords[1]
        pos = pos // dims[1].chunk_length
        coord0 = pos + chunk_coords[0]
        res = (coord0, coord1)
    else:
        res = []
        for i in range(n_dims - 1, -1, -1):
            res.insert(0, pos % dims[i].chunk_length + chunk_coords[i])
            pos = pos // dims[i].chunk_length

    df = pandas.DataFrame(res)
    df = df.transpose()
    df.columns = [d.name for d in dims]
    return df


# util/ArrayCoordinatesMapper.h
#
# /**
#  * Convert array coordinates to the logical chunk position (in row-major
#  * order)
#  */
# position_t coord2pos(CoordinateCRange coord) const
# {
#     assert(coord.size() == _nDims);
#     position_t pos(-1);
#     if (_nDims == 1) {
#         pos = coord[0] - _origin[0];
#         assert(pos < _chunkIntervals[0]);
#     } else if (_nDims == 2) {
#         pos = (coord[0] - _origin[0])*_chunkIntervals[1] +
#             (coord[1] - _origin[1]);
#     } else {
#         pos = 0;
#         for (size_t i = 0, n = _nDims; i < n; i++) {
#             pos *= _chunkIntervals[i];
#             pos += coord[i] - _origin[i];
#         }
#     }
#     assert(pos >= 0 && static_cast<uint64_t>(pos)<_logicalChunkSize);
#     return pos;
# }
#
# /**
#  * Convert logical chunk position (in row-major order)  to array coordinates
#  */
# void pos2coord(position_t pos,CoordinateRange coord) const
# {
#     assert(pos >= 0);
#     assert(coord.size() == _nDims);
#     if (_nDims == 1) {
#         coord[0] = _origin[0] + pos;
#         assert(pos < _chunkIntervals[0]);
#     } else if (_nDims == 2) {
#         coord[1] = _origin[1] + (pos % _chunkIntervals[1]);
#         pos /= _chunkIntervals[1];
#         coord[0] = _origin[0] + pos;
#         assert(pos < _chunkIntervals[0]);
#     } else {
#         for (int i=safe_static_cast<int>(_nDims); --i>=0;) {
#             coord[i] = _origin[i] + (pos % _chunkIntervals[i]);
#             pos /= _chunkIntervals[i];
#         }
#         assert(pos == 0);
#     }
# }
