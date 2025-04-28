
import unittest   # The test framework
import grid


class Test_Grid(unittest.TestCase):

    def setUp(self):
        """Create a fresh grid before each test"""
        self.board = grid.Grid()
    
    def test_grid_size(self):
        """Ensure the grid is exactly 5x5"""
        self.assertEqual(len(self.board.grid), 5)  # Check rows
        for row in self.board.grid:
            self.assertEqual(len(row), 5)  # Check columns in each row

    def test_get_neighbors_center(self):
        """Test get_neighbors for a middle cell"""
        neighbors = self.board.get_neighbors((2, 2))
        expected = [(3, 2), (1, 2), (2, 3), (2, 1)]  # All within bounds
        self.assertCountEqual(neighbors, expected)

    def test_get_neighbors_corner(self):
        """Test get_neighbors for a corner (0,0)"""
        neighbors = self.board.get_neighbors((0, 0))
        expected = [(1, 0), (0, 1)]  # No negative coordinates
        self.assertCountEqual(neighbors, expected)

    def test_get_neighbors_edge(self):
        """Test get_neighbors for an edge cell (4,2)"""
        neighbors = self.board.get_neighbors((4, 2))
        expected = [(3, 2), (4, 3), (4, 1)]  
        self.assertCountEqual(neighbors, expected)

    def test_get_neighbors_corner_opposite(self):
        """Test get_neighbors for opposite corner (4,4)"""
        neighbors = self.board.get_neighbors((4, 4))
        expected = [(3, 4), (4, 3)]  
        self.assertCountEqual(neighbors, expected)

    def test_calculator_find_connected_tiles_01(self):

        self.board.grid[0][0].set_biome(3)  # Forest
        self.board.grid[0][1].set_biome(3)  # Forest
        self.board.grid[1][1].set_biome(3)  # Forest
        self.board.grid[2][1].set_biome(3)  # Forest
        self.board.grid[1][2].set_biome(3)  # Forest
        self.board.grid[2][0].set_biome(3)  # Forest
        self.board.grid[1][3].set_biome(3)  # Forest

        line_of_tiles = self.board.find_connected_tiles((0,0))
        expected = {self.board.grid[0][0], 
                    self.board.grid[0][1], 
                    self.board.grid[1][1], 
                    self.board.grid[2][1], 
                    self.board.grid[1][2], 
                    self.board.grid[2][0], 
                    self.board.grid[1][3]}

        self.assertCountEqual(line_of_tiles, expected)


    def test_calculator_find_connected_tiles_02(self):

        self.board.grid[0][0].set_biome(3)  # Forest
        self.board.grid[0][1].set_biome(3)  # Forest
        #self.board.grid[1][1].set_biome(3)  # Forest
        self.board.grid[2][1].set_biome(3)  # Forest
        self.board.grid[1][2].set_biome(3)  # Forest
        self.board.grid[2][0].set_biome(3)  # Forest
        self.board.grid[1][3].set_biome(3)  # Forest

        line_of_tiles = self.board.find_connected_tiles((0,0))
        expected = {self.board.grid[0][0], self.board.grid[0][1]}

        self.assertCountEqual(line_of_tiles, expected)

    def test_calculator_find_connected_tiles_03(self):

        self.board.grid[0][0].set_biome(3)  # Forest
        self.board.grid[0][1].set_biome(3)  # Forest
        self.board.grid[1][1].set_biome(3)  # Forest
        #self.board.grid[2][1].set_biome(3)  # Forest
        self.board.grid[1][2].set_biome(3)  # Forest
        self.board.grid[2][0].set_biome(3)  # Forest
        self.board.grid[1][3].set_biome(3)  # Forest

        line_of_tiles = self.board.find_connected_tiles((0,0))
        expected = {self.board.grid[0][0], 
                    self.board.grid[0][1], 
                    self.board.grid[1][1], 
                    self.board.grid[1][2], 
                    self.board.grid[1][3]}

        self.assertCountEqual(line_of_tiles, expected)

    def test_all_connected_tiles(self):
        # Set biomes for the grid (5x5 grid)

        # Row 0 - Fields
        self.board.grid[0][0].set_biome(2)  
        self.board.grid[0][1].set_biome(2) 
        self.board.grid[0][2].set_biome(2)  
        self.board.grid[0][3].set_biome(2)  
        self.board.grid[0][4].set_biome(2) 

        # Row 1 - Forest
        self.board.grid[1][0].set_biome(3)  
        self.board.grid[1][1].set_biome(3)  
        self.board.grid[1][2].set_biome(3) 
        self.board.grid[1][3].set_biome(3)  
        self.board.grid[1][4].set_biome(3)  

        # Row 2 - Grasslands
        self.board.grid[2][0].set_biome(4)  
        self.board.grid[2][1].set_biome(4)  
        self.board.grid[2][2].set_biome(4)  
        self.board.grid[2][3].set_biome(4)  
        self.board.grid[2][4].set_biome(4)  

        # Row 3 - Lakes
        self.board.grid[3][0].set_biome(5)  
        self.board.grid[3][1].set_biome(5) 
        self.board.grid[3][2].set_biome(5)  
        self.board.grid[3][3].set_biome(5)  
        self.board.grid[3][4].set_biome(5) 

        # Row 4 - Mine
        self.board.grid[4][0].set_biome(6) 
        self.board.grid[4][1].set_biome(6)  
        self.board.grid[4][2].set_biome(6)
        self.board.grid[4][3].set_biome(6) 
        self.board.grid[4][4].set_biome(6)  


        # Now call the method to get all connected tiles
        tile_connections = self.board.all_connected_tiles()

        #expected connections
        expected_field = {self.board.grid[0][i] for i in range(5)}
        expected_forest = {self.board.grid[1][i] for i in range(5)}
        expected_grasslands = {self.board.grid[2][i] for i in range(5)}
        expected_lakes = {self.board.grid[3][i] for i in range(5)}
        expected_mine = {self.board.grid[4][i] for i in range(5)}

        # We expect five separate sets: one for each biome (field, forest, gasslands, lakes, mine)
        expected = [
            expected_field,
            expected_forest,
            expected_grasslands,
            expected_lakes,
            expected_mine
        ]
        # Assert that the sets are equal, order doesn't matter in sets
        self.assertCountEqual(tile_connections, expected)

    def test_calc_connected_tiles_total_sum_01(self):
        """Tests that the calc can sum the resaults of a single tile connection"""

        # Row 0 - Fields
        self.board.grid[0][0].set_biome(2)  
        self.board.grid[0][1].set_biome(2) 
        self.board.grid[0][2].set_biome(2)  
        self.board.grid[0][3].set_biome(2)  
        self.board.grid[0][4].set_biome(2) 

        # Row 1 - Forest
        self.board.grid[1][0].set_biome(3)  
        self.board.grid[1][1].set_biome(3)  
        self.board.grid[1][2].set_biome(3) 
        self.board.grid[1][3].set_biome(3)  
        self.board.grid[1][4].set_biome(3)  

        # Row 2 - Grasslands
        self.board.grid[2][0].set_biome(4)  
        self.board.grid[2][1].set_biome(4)  
        self.board.grid[2][2].set_biome(4)  
        self.board.grid[2][3].set_biome(4)  
        self.board.grid[2][4].set_biome(4)  

        # Row 3 - Lakes
        self.board.grid[3][0].set_biome(5)  
        self.board.grid[3][1].set_biome(5) 
        self.board.grid[3][2].set_biome(5)  
        self.board.grid[3][3].set_biome(5)  
        self.board.grid[3][4].set_biome(5) 

        # Row 4 - Mine
        self.board.grid[4][0].set_biome(6) 
        self.board.grid[4][1].set_biome(6)  
        self.board.grid[4][2].set_biome(6)
        self.board.grid[4][3].set_biome(6) 
        self.board.grid[4][4].set_biome(6)
 

        self.board.grid[4][4].set_crowns(1)
        self.board.grid[4][3].set_crowns(1)
        
        total_sum = self.board.calc_connected_tiles_total_sum()
        expected = 10
        self.assertEqual(total_sum, expected)

    def test_calc_connected_tiles_total_sum_02(self):
        """Tests that the calc can sum the resaults of two diffrent connections"""

        # Row 0 - Fields
        self.board.grid[0][0].set_biome(2)  
        self.board.grid[0][1].set_biome(2) 
        self.board.grid[0][2].set_biome(2)  
        self.board.grid[0][3].set_biome(2)  
        self.board.grid[0][4].set_biome(2) 

        # Row 1 - Forest
        self.board.grid[1][0].set_biome(3)  
        self.board.grid[1][1].set_biome(3)  
        self.board.grid[1][2].set_biome(3) 
        self.board.grid[1][3].set_biome(3)  
        self.board.grid[1][4].set_biome(3)  

        # Row 2 - Grasslands
        self.board.grid[2][0].set_biome(4)  
        self.board.grid[2][1].set_biome(4)  
        self.board.grid[2][2].set_biome(4)  
        self.board.grid[2][3].set_biome(4)  
        self.board.grid[2][4].set_biome(4)  

        # Row 3 - Lakes
        self.board.grid[3][0].set_biome(5)  
        self.board.grid[3][1].set_biome(5) 
        self.board.grid[3][2].set_biome(5)  
        self.board.grid[3][3].set_biome(5)  
        self.board.grid[3][4].set_biome(5) 

        # Row 4 - Mine
        self.board.grid[4][0].set_biome(6) 
        self.board.grid[4][1].set_biome(6)  
        self.board.grid[4][2].set_biome(6)
        self.board.grid[4][3].set_biome(6) 
        self.board.grid[4][4].set_biome(6)
 

        self.board.grid[1][1].set_crowns(1)
        self.board.grid[4][3].set_crowns(1)
        
        total_sum = self.board.calc_connected_tiles_total_sum()
        expected = 10
        self.assertEqual(total_sum, expected)



if __name__ == '__main__':
    unittest.main()