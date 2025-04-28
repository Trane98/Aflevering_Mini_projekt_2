# Advanced Detection Program ;-) 

import grid
import utils
from models import tile_detector as td
from models import crown_analyser as ca
import cv2
board = grid.Grid()

# import picture
# devide picture by 5x5
# place tile image in its coresponding grid cell. 
# run HSV/HOG model on each grid cell -> predicting the tile biome
# run SIFT model on each grid cell -> predicting amount of crowns on each tile 
# do calculation of final score.
# representation of the grid

# Path to King Domino board image:
#image_path = r"C:\Users\Daniel K\Desktop\DAKI\2. Semester\DUAS_mini_proj\Mini_projekt_2\Program_AD\5.jpg"
image_path = r"C:\Program Files (x86)\2 Semester python work\Aflevering_kan_slettes_efter\Aflevering_Mini_projekt_2\1.png"

# Seperate each tile of the board image into its corresponding coordinate in the grid:
utils.seperate_tiles_to_grid(image_path, board.grid)

# Run tile_detector to label all tiles AND crown_analyser to label the amount of crowns on each tile.
board.run_models()

# Show score and visualize the grid: 
print("\n" * 2)  # Add two blank lines for spacing
print(f"King Domino: Total points scored is {board.calc_connected_tiles_total_sum()}!")
utils.visualize_grid(board) #visualize the grid with the tiles and their crowns
print("\n" * 2)  # Add two blank lines for spacing
