# NAME

Geo::H3::FFI - Perl FFI binding to H3 library functions

# SYNOPSIS

    use Geo::H3::FFI;

# DESCRIPTION

Perl FFI binding to H3 library functions

# Indexing Functions

These function are used for finding the H3 index containing coordinates, and for finding the center and boundary of H3 indexes.

## geoToH3

    H3Index geoToH3(const GeoCoord *g, int res);

Indexes the location at the specified resolution, returning the index of the cell containing the location.

    my $H3Index = geoToH3($GeoCoord, $resolution);

Returns 0 on error.

## h3ToGeo

    void h3ToGeo(H3Index h3, GeoCoord *g);

Finds the centroid of the index.

    my $Geo = h3ToGeo($H3Index);

## h3ToGeoBoundary

    void h3ToGeoBoundary(H3Index h3, GeoBoundary *gp);

Finds the boundary of the index.

    my $Boundary = h3ToGeoBoundary($H3Index);

# Index Inspection Functions

These functions provide metadata about an H3 index, such as its resolution or base cell, and provide utilities for converting into and out of the 64-bit representation of an H3 index.

## h3GetResolution

Returns the resolution of the index.

## h3GetBaseCell

Returns the base cell number of the index.

## stringToH3

Converts the string representation to H3Index (uint64\_t) representation.

Returns 0 on error.

## h3ToString

Converts the H3Index representation of the index to the string representation. str must be at least of length 17.

## h3IsValid

Returns non-zero if this is a valid H3 index.

## h3IsResClassIII

Returns non-zero if this index has a resolution with Class III orientation.

## h3IsPentagon

Returns non-zero if this index represents a pentagonal cell.

## h3GetFaces

Find all icosahedron faces intersected by a given H3 index and places them in the array out. out must be at least of length maxFaceCount(h).

Faces are represented as integers from 0-19, inclusive. The array is sparse, and empty (no intersection) array values are represented by -1.

## maxFaceCount

Returns the maximum number of icosahedron faces the given H3 index may intersect.

# Grid traversal functions

Grid traversal allows finding cells in the vicinity of an origin cell, and determining how to traverse the grid from one cell to another.

## kRing

    void kRing(H3Index origin, int k, H3Index* out);

k-rings produces indices within k distance of the origin index.

k-ring 0 is defined as the origin index, k-ring 1 is defined as k-ring 0 and all neighboring indices, and so on.

Output is placed in the provided array in no particular order. Elements of the output array may be left zero, as can happen when crossing a pentagon.

## maxKringSize

Maximum number of indices that result from the kRing algorithm with the given k.

## kRingDistances

k-rings produces indices within k distance of the origin index.

k-ring 0 is defined as the origin index, k-ring 1 is defined as k-ring 0 and all neighboring indices, and so on.

Output is placed in the provided array in no particular order. Elements of the output array may be left zero, as can happen when crossing a pentagon.

## hexRange

hexRange produces indexes within k distance of the origin index. Output behavior is undefined when one of the indexes returned by this function is a pentagon or is in the pentagon distortion area.

k-ring 0 is defined as the origin index, k-ring 1 is defined as k-ring 0 and all neighboring indexes, and so on.

Output is placed in the provided array in order of increasing distance from the origin.

Returns 0 if no pentagonal distortion is encountered.

## hexRangeDistances

hexRange produces indexes within k distance of the origin index. Output behavior is undefined when one of the indexes returned by this function is a pentagon or is in the pentagon distortion area.

k-ring 0 is defined as the origin index, k-ring 1 is defined as k-ring 0 and all neighboring indexes, and so on.

Output is placed in the provided array in order of increasing distance from the origin. The distances in hexagons is placed in the distances array at the same offset.

Returns 0 if no pentagonal distortion is encountered.

## hexRanges

hexRanges takes an array of input hex IDs and a max k-ring and returns an array of hexagon IDs sorted first by the original hex IDs and then by the k-ring (0 to max), with no guaranteed sorting within each k-ring group.

Returns 0 if no pentagonal distortion was encountered. Otherwise, output is undefined

## hexRing

Produces the hollow hexagonal ring centered at origin with sides of length k.

Returns 0 if no pentagonal distortion was encountered.

## h3Line

Given two H3 indexes, return the line of indexes between them (inclusive).

This function may fail to find the line between two indexes, for example if they are very far apart. It may also fail when finding distances for indexes on opposite sides of a pentagon.

Notes:

    - The specific output of this function should not be considered stable across library versions. The only guarantees the library provides are that the line length will be h3Distance(start, end) + 1 and that every index in the line will be a neighbor of the preceding index.

    - Lines are drawn in grid space, and may not correspond exactly to either Cartesian lines or great arcs.

## h3LineSize

Number of indexes in a line from the start index to the end index, to be used for allocating memory. Returns a negative number if the line cannot be computed.

## h3Distance

Returns the distance in grid cells between the two indexes.

Returns a negative number if finding the distance failed. Finding the distance can fail because the two indexes are not comparable (different resolutions), too far apart, or are separated by pentagonal distortion. This is the same set of limitations as the local IJ coordinate space functions.

## experimentalH3ToLocalIj

Produces local IJ coordinates for an H3 index anchored by an origin.

This function is experimental, and its output is not guaranteed to be compatible across different versions of H3.

## experimentalLocalIjToH3

Produces an H3 index from local IJ coordinates anchored by an origin.

This function is experimental, and its output is not guaranteed to be compatible across different versions of H3.

# Hierarchical grid functions

These functions permit moving between resolutions in the H3 grid system. The functions produce parent (coarser) or children (finer) cells.

## h3ToParent

Returns the parent (coarser) index containing h.

## h3ToChildren

Populates children with the indexes contained by h at resolution childRes. children must be an array of at least size maxH3ToChildrenSize(h, childRes).

## maxH3ToChildrenSize

## h3ToCenterChild

Returns the center child (finer) index contained by h at resolution childRes.

## compact

Compacts the set h3Set of indexes as best as possible, into the array compactedSet. compactedSet must be at least the size of h3Set in case the set cannot be compacted.

Returns 0 on success.

## uncompact

Uncompacts the set compactedSet of indexes to the resolution res. h3Set must be at least of size maxUncompactSize(compactedSet, numHexes, res).

Returns 0 on success.

## maxUncompactSize

Returns the size of the array needed by uncompact.

# Region functions

These functions convert H3 indexes to and from polygonal areas.

## polyfill

polyfill takes a given GeoJSON-like data structure and preallocated, zeroed memory, and fills it with the hexagons that are contained by the GeoJSON-like data structure.

Containment is determined by the cells' centroids. A partioning using the GeoJSON-like data structure, where polygons cover an area without overlap, will result in a partitioning in the H3 grid, where cells cover the same area without overlap.

## maxPolyfillSize

maxPolyfillSize returns the number of hexagons to allocate space for when performing a polyfill on the given GeoJSON-like data structure.

## h3SetToLinkedGeo

Create a LinkedGeoPolygon describing the outline(s) of a set of hexagons. Polygon outlines will follow GeoJSON MultiPolygon order: Each polygon will have one outer loop, which is first in the list, followed by any holes.

It is the responsibility of the caller to call destroyLinkedPolygon on the populated linked geo structure, or the memory for that structure will not be freed.

It is expected that all hexagons in the set have the same resolution and that the set contains no duplicates. Behavior is undefined if duplicates or multiple resolutions are present, and the algorithm may produce unexpected or invalid output.

## h3SetToMultiPolygon

## destroyLinkedPolygon

Free all allocated memory for a linked geo structure. The caller is responsible for freeing memory allocated to the input polygon struct.

# Unidirectional edge functions

Unidirectional edges allow encoding the directed edge from one cell to a neighboring cell.

## h3IndexesAreNeighbors

Returns whether or not the provided H3Indexes are neighbors.

Returns 1 if the indexes are neighbors, 0 otherwise.

## getH3UnidirectionalEdge

Returns a unidirectional edge H3 index based on the provided origin and destination.

Returns 0 on error.

## h3UnidirectionalEdgeIsValid

Determines if the provided H3Index is a valid unidirectional edge index.

Returns 1 if it is a unidirectional edge H3Index, otherwise 0.

## getOriginH3IndexFromUnidirectionalEdge

Returns the origin hexagon from the unidirectional edge H3Index.

## getDestinationH3IndexFromUnidirectionalEdge

Returns the destination hexagon from the unidirectional edge H3Index.

## getH3IndexesFromUnidirectionalEdge

Returns the origin, destination pair of hexagon IDs for the given edge ID, which are placed at originDestination\[0\] and originDestination\[1\] respectively.

## getH3UnidirectionalEdgesFromHexagon

Provides all of the unidirectional edges from the current H3Index. edges must be of length 6, and the number of undirectional edges placed in the array may be less than 6.

## getH3UnidirectionalEdgeBoundary

Provides the coordinates defining the unidirectional edge.

# Miscellaneous H3 functions

These functions include descriptions of the H3 grid system.

## degsToRads

Converts degrees to radians.

## radsToDegs

Converts radians to degrees.

## hexAreaKm2

Average hexagon area in square kilometers at the given resolution.

## hexAreaM2

Average hexagon area in square meters at the given resolution.

## cellAreaM2

Exact area of specific cell in square meters.

## cellAreaRads2

Exact area of specific cell in square radians.

## edgeLengthKm

Average hexagon edge length in kilometers at the given resolution.

## edgeLengthM

Average hexagon edge length in meters at the given resolution.

## exactEdgeLengthKm

Exact edge length of specific unidirectional edge in kilometers.

## exactEdgeLengthM

Exact edge length of specific unidirectional edge in meters.

## exactEdgeLengthRads

Exact edge length of specific unidirectional edge in radians.

## numHexagons

Number of unique H3 indexes at the given resolution.

## getRes0Indexes

All the resolution 0 H3 indexes. out must be an array of at least size res0IndexCount().

## res0IndexCount

Number of resolution 0 H3 indexes.

## getPentagonIndexes

All the pentagon H3 indexes at the specified resolution. out must be an array of at least size pentagonIndexCount().

## pentagonIndexCount

Number of pentagon H3 indexes per resolution. This is always 12, but provided as a convenience.

## pointDistKm

Gives the "great circle" or "haversine" distance between pairs of GeoCoord points (lat/lng pairs) in kilometers.

## pointDistM

Gives the "great circle" or "haversine" distance between pairs of GeoCoord points (lat/lng pairs) in meters.

## pointDistRads

Gives the "great circle" or "haversine" distance between pairs of GeoCoord points (lat/lng pairs) in radians.

# SEE ALSO

# AUTHOR

Michael R. Davis

# COPYRIGHT AND LICENSE

MIT License

Copyright (c) 2020 Michael R. Davis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
