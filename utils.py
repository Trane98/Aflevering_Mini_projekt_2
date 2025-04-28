"""Til overskuds funktioner"""

            
import cv2
import numpy as np

def split_billede(image_path):
    """Funktionen her skal bruges til at splitte et billede op i 5x5"""
    img = cv2.imread(image_path)  # Loads image as a NumPy array (BGR format)
    height, width, _ = img.shape

    rows, cols = 5, 5
    tile_width = width // cols
    tile_height = height // rows

    tiles = []

    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = img[upper:lower, left:right]  # Crop using NumPy slicing
            tiles.append(tile)

    return tiles


def seperate_tiles_to_grid(image_path, grid):
    tile_images = split_billede(image_path)
    idx = 0
    for row in grid:
        for tile in row:
            tile.tile_image = tile_images[idx]  # Already in NumPy BGR format
            idx += 1


def visualize_grid(board):
    # Define a width for each cell (you can adjust this to suit your data)
    cell_width = 20  # Adjust the width as needed for a more readable layout
    
    # Print a couple of blank lines to separate previous output
    print("\n" )

    # Set the width for each column (adjust this based on your needs)
    tile_width = 18

    # Print top border of the grid
    print("+" + "-" * (tile_width * len(board.grid[0]) + len(board.grid[0]) + 1) + "+")

    for row in board.grid:
        # Create a list to store the formatted biome and crown values for the current row
        biome_row = []
        
        for tile in row:
            # Get the biome and crown info, then format it with the specified width
            biome_info = f"{tile.labels[tile.biome]}, c:{tile.crowns}"
            # Append the formatted string to the biome_row list
            biome_row.append(biome_info.ljust(cell_width))  # .ljust ensures uniform width

        # Print the formatted row with even separation
        print("".join(biome_row))
        print("+" + "-" * (tile_width * len(board.grid[0]) + len(board.grid[0]) + 1) + "+")