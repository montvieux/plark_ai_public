from ..classes.map import Map
from ..classes.panther import Panther
from ..classes.sonobuoy import Sonobuoy

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

def test_oddq_to_cube():
    map_width = 10
    map_height = 10
    testMap = Map(map_width, map_height)

    oddq = [0, 0]
    cube = testMap.oddq_to_cube(oddq[0], oddq[1])
    assert cube == {
        'x': 0,
        'y': 0,
        'z': 0
    }


def test_cube_to_oddq():
    map_width = 10
    map_height = 10
    testMap = Map(map_width, map_height)
    
    cube = {
        'x': 0,
        'y': 0,
        'z': 0
    }
    oddq = testMap.cube_to_oddq(cube)
    assert oddq == (0, 0)


def test_map_distance():
    map_width = 10
    map_height = 10
    testMap = Map(map_width, map_height)
    
    point_1_col = 0 
    point_1_row = 0
    point_2_col = 0 
    point_2_row = 9

    testDistance = testMap.distance(point_1_col, point_1_row, point_2_col, point_2_row)
    assert testDistance == 9


def test_get_edges():
    map_width = 3
    map_height = 3
    testMap = Map(map_width, map_height)
        
    results = testMap.get_edges()

    edgeResults = [
        {'col': 0, 'row': 0},
        {'col': 0, 'row': 1},
        {'col': 0, 'row': 2},
        {'col': 1, 'row': 0},
        {'col': 1, 'row': 2},
        {'col': 2, 'row': 0},
        {'col': 2, 'row': 1},
        {'col': 2, 'row': 2}
 ]
    assert results == edgeResults

def test_get_radius():
    map_width = 10
    map_height = 10
    testMap = Map(map_width, map_height)
    
    start_col = 4
    start_row = 0
    results = testMap.getRadius(start_col, start_row,1)
    expected_radius = [
        {'col': 3, 'row': 0},
        {'col': 4, 'row': 1},
        {'col': 4, 'row': 0},
        {'col': 5, 'row': 0}]

    assert results == expected_radius


def test_search_radius():
    map_width = 10
    map_height = 10
    testMap = Map(map_width, map_height)
    
    search_col = 4 
    search_row = 4 

    sb = Sonobuoy(4)
    sb_start_col = 4
    sb_start_row = 2

    sb.setLocation(sb_start_col, sb_start_row)
    testMap.addItem(sb.col, sb.row, sb)

    p = Panther()
    panther_start_col = 4
    panther_start_row = 1

    p.setLocation(panther_start_col, panther_start_row)
    testMap.addItem(p.col, p.row ,p)

    expected_results = [sb, p]
    results = testMap.searchRadius(search_col, search_row, sb.range , [sb.type,p.type])
    assert results == expected_results

def test_path_planning():
    map_width = 5
    map_height = 5
    testMap = Map(map_width, map_height)
    
    start_location_col = 0
    start_location_row = 0
    end_location_col = map_width -1
    end_location_row = map_height -1

    testMap.get_path(start_location_col, start_location_row, end_location_col, end_location_row)

    expected_results = [{'col': 0, 'row': 1}, {'col': 0, 'row': 2}, {'col': 1, 'row': 2}, {'col': 2, 'row': 3}, {'col': 3, 'row': 3}, {'col': 4, 'row': 4}]
    results = testMap.get_path(start_location_col, start_location_row, end_location_col, end_location_row)

    assert results == expected_results
