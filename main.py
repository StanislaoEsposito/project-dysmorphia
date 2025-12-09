import curses
import random
import math
import time
import pickle
import os
import sys
import traceback

# Tenta di importare Pygame per l'audio
try:
    import pygame
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

# --- CONFIGURAZIONE ---
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
SAVE_FILE = "dysmorphia_save.dat"
CRASH_LOG = "crash_log.txt"
SCREAM_FILE = "scream.wav" 

# LISTA SUONI JUMPSCARE
JUMP_SOUND_FILES = ["jump1.wav", "jump2.wav", "jump3.wav"]

# MAPPATURA MUSICHE
MUSIC_TRACKS = {
    "MENU": "horror_theme.wav",
    1: "level1.mp3", 
    2: "level2.mp3", 
    3: "level3.mp3", 
    4: "level4.mp3", 
    5: "level5.mp3"  
}
LANG_EN = "EN"
LANG_IT = "IT"
# Caratteri Base
WALL_CHAR = '#'
FLOOR_CHAR = '.'
MIRROR_CHAR = '|'
ENEMY_CHAR = 'S' 
EXIT_CHAR = 'O'  
ITEM_CHAR = '+'  
WEAPON_CHAR = '/' 
BIZARRE_CHAR = '?' 

# --- JUMPSCARE ARTS COLLECTION ---
JUMPSCARE_ARTS = [
    # 1. IL VOLTO (The Face)
    [
        "⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⢀⡿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠄⠀⠀⠀",
        "⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀",
        "⠀⠀⠀⢠⣿⣇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀",
        "⠀⠀⠀⠀⣻⣿⣿⣿⣿⡿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⣿⣿⣿⣿⣷⣭⠀⠀⠀",
        "⠀⠀⠀⠀⣻⣿⠟⠛⠉⠁⠈⠉⠻⢿⣿⣿⣿⡟⠛⠂⠉⠁⠈⠉⠁⠻⣿⠀⠀⠀",
        "⠀⠀⠀⠀⢾⠀⠀⣠⠄⠻⣆⠀⠈⠠⣻⣿⣟⠁⠀⠀⠲⠛⢦⡀⠀⠠⠁⠀⠀⠀",
        "⠀⠀⠀⠀⢱⣄⡀⠘⠀⠸⠉⠀⠀⢰⣿⣷⣿⠂⢀⠀⠓⡀⠞⠀⢀⣀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠠⣿⣷⣶⣶⣶⣾⣿⠀⠸⣿⣿⣿⣶⣿⣧⣴⣴⣶⣶⣿⡟⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣏⠇⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣾⠁⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣟⡿⠂⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠑⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⠀⠀⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠄⢻⣿⣿⣿⡗⠀⠀⠀⠀⠈⠀⢨⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⡞⠷⠿⠿⠀⠀⠀⠀⢀⣘⣤⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠼⠉⠀⠀⠀⠀⠀⠚⢻⠿⠟⠓⠛⠂⠉⠉⠁⠀⡁⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣼⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⡀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢾⠻⠌⣄⡁⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣀⣀⣀⡠⡲⠞⡁⠈⡈⣿⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠘⠛⠻⢯⠟⠩⠀⠀⢠⣣⠈⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⠂⣰⣧⣾⠶⠀⠀⠀⠀⠀⠀⠀"
    ],
    # 2. GLITCH NOISE A (Dense)
    [
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢉⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠄⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣉⣁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣈⡏⠹⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣦⡀⠀⠈⣿⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠃⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⠘⣿⣤⡀⢀⡀⠀⠀⠉⠻⡟⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⢉⣁⣡⣤⣴⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣹⣿⣾⢿⣆⣠⠀⠀⢁⠈⣿⡿⠀⠈⣿⠟⠀⠈⠹⣿⡏⠀⠀⠈⣿⡟⠁⠸⣿⠃⣼⣏⢀⡆⣴⣿⣿⡟⡅⣿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⡿⢿⣶⣷⣼⣷⣟⠁⠀⠀⡟⠀⠀⠀⠀⣽⡇⠀⠀⠀⠨⠄⠀⠀⢙⡀⢃⣸⣾⣿⣼⣿⢸⣧⣷⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣷⡈⣷⡈⣻⣿⣼⣦⣀⣰⠃⠀⠀⠀⠀⠙⠁⠀⡀⠀⠊⣠⣀⣤⣾⣷⡌⣯⣿⢟⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡺⠇⢹⣿⣿⣿⡿⣿⣤⣀⣀⣤⣤⣴⣄⠀⠃⣄⣀⢿⡿⠛⠿⣿⠙⣿⣷⣼⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣾⠹⣿⡿⠁⢹⡃⠈⠉⣿⠁⠊⡿⠀⠈⣿⠀⢸⡇⠀⠀⢿⡄⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣿⠁⣠⣾⠇⠀⢠⣧⠀⢠⡇⠀⢀⣿⡀⢸⣇⠀⢠⣸⣷⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣦⣠⣾⣿⣶⣾⣷⣤⣸⣿⣿⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
    ],
    # 3. GLITCH NOISE B (Scattered)
    [
        "⠀⠀⠀⠋⠛⢻⡟⠋⠉⠁⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⣿⡇⠀⠀⠜⠀⠀⠀⠀⠀⠀⢹",
        "⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠀⠀⠀⠀⠀⣤⠀⠀⠀⢸⠀⠀⣄⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⢈⠀",
        "⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⣗⠀⠀⠀⠸⠀⠀⣿⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⢐⠀⠀⠀",
        "⠀⢤⣀⣀⡀⣐⣇⣤⣤⡀⠀⠀⠀⠀⠀⠀⠳⣀⣀⡠⠃⠣⠄⠔⠃⠀⠀⣧⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠓⠀⠁⠉⠀⠀⠀⠋⠉⠀⠁⠀⠀⠀",
        "                                                                   ",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⠀⠀⠀⢀⡔⠁⠀⠀⣠⠤⣤⡄⣤⣦⠔⠒⠀⠀⠀⣶⠀⠀⠀⠀⠀⠀⠀⠀⡤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣏⡀⠀⣠⠟⠁⠀⠀⠀⠈⠉⠀⠙⡟⠁⠀⠀⠀⠀⠀⡧⠃⠀⠀⠀⠀⠀⠀⠀⠅⣮⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠧⡇⡞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠽⠀⠀⠀⠀⠀⠀⠀⡟⠄⠀⠀⠀⠀⠀⠀⠀⠊⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠟⡗⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠗⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⡋⠀⠀⢭⢧⠀⠀⠀⠀⠀⠀⠀⠀⡯⡆⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⢈⣗⠀⢀⢀⡠⠀⣀⠂⢀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⠀⠈⠁⠷⠀⠀⠤⠤⠞⠒⠊⠚⠛⠗⠓⠀⠀⠦⠿⠿⠟⠟⠷⠆⠀⠀⠙⣷⠷⠛⡺⠍⠣⠕⠁⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀",
        "                                                                   ",
        "⠀⠀⠀⠀⠀⠀⢹⠇⡀⠀⠀⠀⠀⠀⣮⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠰⢎⡅⠀⠀⢀⡞⠀⠀⠀⠀⠠⡶⠢⠋⠂⠁⠃⢧⡂⠀⠀⠀⢼⡅⠀⠀⠀⠀⠀⣏⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠉⡢⡀⢠⣭⠀⠀⠀⠀⠌⡕⠁⠀⠀⠀⠀⠀⠀⠀⠑⡀⠀⠘⡎⠁⠀⠀⠀⠀⢿⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠗⣷⠃⠀⠀⠀⠀⡢⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⡿⡅⠀⠀⠀⠀⢐⠆⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣟⠇⠀⠀⠀⠀⠪⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀⣭⠂⠀⠚⣃⠀⠀⠀⠀⡊⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⣣⠀⠀⠀⠀⠀⠀⢭⠂⡀⠀⠀⠀⠀⠀⠀⢁⠳⠀⠀⢫⡣⡀⠀⠀⡐⢝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣓⠂⠀⠀⠀⠀⠀⠀⠆⣧⣆⡀⡀⠂⢀⡤⠀⠁⠀⠠⢳⣤⣠⠀⡝⡭⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⡿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠘⠋⠁⠀⠀⠀⠀⠀⠈⠑⠌⡀⡤⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
    ],
    # 4. GLITCH ABSTRACT (Da tua richiesta)
    [
        "        ⣿⡅⠀⡀⠀⠀⠀⠀⡄⠀⠄⠀⠠⡁⡘⠀⠀⠀⠠⠀⠀⠤⠠⡎⠄⠀⠀⠀⡄⢂⡇⢀⡀⠀⠂⢦⠀⠐⠀⠁⡐⣀⡀⢀⠀⢘⢀⡠⠂⠀⡀⢀⡀⠀⠘⠋⢙⠀⠀⠁⠀⠁⠀⠠⠀",
        "⣿⡇⠀⠄⠀⠀⠀⠐⡆⠀⠂⠀⠔⢨⡅⠀⠀⠃⠐⠇⠀⠀⠀⣽⣾⣶⠓⢶⡃⢌⠀⠀⠐⠀⠘⣂⠘⠀⠀⡇⠀⢿⢿⠾⠿⠿⠲⠂⡀⠀⡆⠀⣹⠖⠀⠐⠲⠆⠠⡇⠀⡐⠒⠒⠀",
        "⣿⡁⠀⠁⠀⠀⠀⠀⡃⠀⠄⠀⡭⠀⣡⠤⠤⠀⠨⡖⠒⡆⢠⡼⠁⢏⠀⠀⡴⢾⡆⠀⠆⠀⠀⡇⢀⠀⠀⡀⠈⢏⠀⡐⠀⠀⢁⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⡀⠀⡀⠀⡆⠀⠐⠈",
        "⣿⡇⠀⣀⠀⠀⠀⠀⠁⠀⠁⠀⠀⠄⠀⠀⠀⡀⢐⠁⠀⡄⠀⠙⡛⠛⠒⠛⣶⣌⣣⠀⠀⠀⠰⡡⡊⠀⠀⠀⢈⠌⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⢿⠏⠉⡃⠀⠀⠀",
        "⣿⠁⠀⠃⠀⠀⠀⠀⢀⠀⠄⠀⠐⠀⠐⠀⠀⠀⠀⠆⠀⠄⠀⢘⠄⠀⠀⠀⣾⢷⡇⠀⡆⠀⠀⢇⠀⡀⢀⡆⢀⠂⠀⠐⠀⠈⡀⠀⡁⠀⠀⠀⠅⠀⣰⠀⠀⡄⠈⡁⠀⠆⠀⠀⠀",
        "⣿⡂⠀⠀⠀⠀⠀⠆⠈⠀⠂⠀⡀⠠⠀⠀⠀⠀⢈⡃⠀⠂⠀⠒⠄⠀⠀⠀⠀⠬⠁⠀⠁⠀⢀⡇⢀⠀⠀⢄⢀⡞⠀⠀⠀⠀⡁⠈⠁⠀⠀⠀⢄⠀⠀⠐⠠⡶⠶⡏⠙⢃⠀⣠⠀",
        "⣧⡄⠀⠅⠀⢰⡶⢷⠀⠀⠂⠀⡂⠁⢀⠀⠀⠀⠠⡄⠀⡄⠀⡌⠂⠀⠀⠀⠒⡘⡄⠀⠀⠀⠸⠆⠀⡀⠀⠃⠀⡛⠀⠀⠠⠴⡀⠀⡇⠀⠁⠀⣺⠀⠘⠀⠠⡋⣈⡷⠶⢇⠀⡸⠀",
        "⣿⡇⠀⠄⠀⠈⠡⠀⣄⡤⡄⠀⡇⠠⢃⠀⠀⠀⢐⡀⠀⣄⣀⠐⡃⣠⠤⠀⡄⡰⡇⠀⢃⢀⣀⢋⢀⠁⠀⠃⢀⣇⠀⠀⠀⠀⠄⠀⠁⠀⠁⠀⣺⣤⣌⠀⠀⠖⠀⠗⠲⡇⠀⠄⠀",
        "⣿⠆⠀⠀⠀⠀⢀⣴⡿⠥⠳⠀⡆⡁⠀⠀⢀⡤⣦⠁⠀⡁⠀⢐⢠⣤⣄⡀⣧⣟⣿⣥⣼⣷⣾⣶⣶⣴⣶⣦⣬⣁⠠⠀⠀⠀⠦⠀⠀⠀⠆⠀⠀⠘⠙⠁⠈⡄⠠⡅⠀⡂⠀⠈⠀",
        "⣿⠀⠀⠀⠀⢸⠘⠻⠀⠀⠀⠀⠇⠀⢠⠀⠈⠁⢁⣤⣠⣅⣶⣾⣿⣷⣿⣿⣿⡿⡿⠿⡿⠿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣽⣲⡡⡀⠀⠄⠀⡄⠀⠀⠀⠀⠀⠃⠃⠀⠀⠀⠐⠀",
        "⣟⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⡀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⢿⠉⣡⣾⣶⣾⣿⣷⣿⣿⣮⣦⢫⡟⢿⣿⣿⣿⣿⣿⣿⣷⣧⣤⣦⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠅⠀⠘⠀",
        "⣿⣄⡐⠁⠀⠀⠀⠀⠀⠀⠀⣠⣶⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠎⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡦⡷⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣏⣷⡄⣀⠀⡄⠀⠀⠀⠁⠀⠀⠀",
        "⣿⡷⡜⡎⡘⠀⣠⢦⢄⣤⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⣼⣿⣼⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣺⠾⣵⢦⣀⠀⠀⠀⢀⠀",
        "⣿⢺⠽⡇⣾⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢬⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢳⡿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⣿⣜⣆⠀⠀⢰⠠",
        "⡿⠈⡀⠁⠀⠀⠉⠉⠉⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⡆⠚⢿⣿⣿⣿⢿⣿⣿⠻⠀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣏⠟⠉⠉⠀⠖⠀⢀⠘",
        "⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣭⣢⡏⠀⠀⠈⢠⣛⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡺⠁⠀⠉⠀⠀⡀⠀⠨⠀",
        "⣿⠃⠀⠀⠀⠀⢀⠀⡀⠀⠀⠀⡂⠁⠀⠀⠀⠀⢡⠂⠀⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⡟⠀⠙⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⢠",
        "⣿⠈⠀⠀⠀⠀⠀⡄⠀⠀⡄⠀⠃⠀⠀⠀⠀⠒⠠⡄⠀⠀⠀⢲⢈⠀⠈⠀⠃⢋⠛⠙⢿⠿⢻⡿⠿⡿⠿⠿⢿⣟⠋⠏⠀⠀⠉⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⢸",
        "⣿⠃⠀⠀⠀⠀⠠⣖⠀⠀⠀⠀⡀⠂⠀⠀⠀⡀⠠⡅⠀⠀⠠⡼⠀⠈⠀⠀⠀⢸⡀⠀⠀⠀⠌⡒⠀⠀⠀⣄⣈⡎⠀⣠⠤⢤⠈⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠸",
        "⣿⠁⠀⠀⠀⠋⠐⠀⠂⠀⠀⠀⠁⠀⠀⠀⠀⠁⢀⠃⠀⠀⠀⠀⡅⠀⠀⠀⠀⡡⠟⠛⡻⠀⠠⡕⠀⠀⠀⠁⢀⠾⠁⡙⠚⠻⣀⢀⡆⠀⠀⠀⠙⠀⠀⠀⠀⡃⠀⠀⠀⢀⠀⢰⣈",
        "⡧⠆⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⢀⠁⡀⠀⠀⠂⠠⠀⠀⠀⠀⠡⠄⠀⠀⢀⠀⢒⡀⠀⠇⠀⢰⡐⠀⠁⠀⡁⠐⡠⠀⠀⠀⠠⠡⠀⡄⠀⠀⠈⠎⠀⠁⠀⠂⠀⠀⠆⠀⠂⠀⢸⢠",
        "⡟⠄⠀⠀⠀⢀⠀⠀⠀⠀⠔⠀⠈⡀⢰⠀⠀⠀⠠⠅⠀⣇⣀⡼⠀⠰⠀⠀⠿⢂⡅⠀⠄⠀⢀⠇⠀⡀⠀⠁⢀⡧⠀⠀⠀⠀⠄⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⢸⠠",
        "⡯⠀⠀⠀⠀⠀⠀⠁⠀⠀⠄⠀⠅⡀⡀⠀⠀⠀⢐⠃⠀⠀⠀⠂⡁⠀⠀⠀⠀⠌⠆⠀⠃⠀⢀⡋⠀⠀⠀⠁⠠⢀⠀⠀⠀⠀⠆⠀⡅⠀⠁⠀⠀⠀⠀⠀⠀⡆⠀⡀⠀⠆⠀⢰⣻",
        "⡗⠂⠀⠀⠀⠠⠸⠠⡅⠀⠀⠀⢅⠀⠓⠀⠀⠀⡈⠤⠀⠀⠀⠰⠴⢴⠀⠀⠄⢊⡅⠀⢁⠀⡰⡱⠀⡀⠀⡄⠈⠄⠀⢀⠀⢠⠔⠂⠆⠀⠀⠀⠊⠀⠀⠀⠠⠇⠀⠄⠀⡤⠀⣲⣾"
    ]
]

# Animazione Giocatore
PLAYER_DIRS = { (0, -1): '^', (0, 1): 'v', (-1, 0): '<', (1, 0): '>', (0, 0): '@' }

# Animazione Mostri
SHADOW_FRAMES = ['S', 's', '5', '$', 'S', 'S']

# Glitch Visivi
GLITCH_CHARS = ['&', '%', '0', '$', 'M', '?', 'W', '#', 'X']
HALLUCINATION_CHARS = ['S', '!', 'x', '+'] 

# Colori
COLOR_PLAYER = 1
COLOR_WALL = 2
COLOR_MIRROR = 3 
COLOR_GLITCH = 4
COLOR_ENEMY = 5
COLOR_FOG = 6 
COLOR_TEXT = 7
COLOR_TITLE = 8
COLOR_ITEM = 9
COLOR_LORE = 10 
COLOR_BLOOD = 11 
COLOR_WEAPON = 12 
COLOR_NPC = 13 
COLOR_DIALOGUE = 14 
COLOR_BIZARRE = 15 # Colore per oggetti strani

# Stati del Gioco
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
STATE_VICTORY = 3
STATE_INTRO = 4
STATE_ENDING = 5
STATE_DIALOGUE = 6 
STATE_LEVEL_INTRO = 7 # Nuova schermata di introduzione livello

# Costanti di Bilanciamento
MAX_LEVELS = 5
HEAL_AMOUNT = 20
PULSE_COST = 15 
ENEMY_DAMAGE = 10 
MOVE_DELAY = 0.15 

SUPPORTED_LANGS = [LANG_EN, LANG_IT]

LORE_INTRO_LANG = {
    LANG_EN: [
        "PROTOCOL 81: COGNITIVE RESET",
        "SUBJECT: [REDACTED]",
        "STATUS: CRITICAL",
        "",
        "You are diving into your own subconscious.",
        "Layer by layer, peeling back the trauma.",
        "",
        "Find the keys to your memory.",
        "Don't let the shadows consume you.",
        "",
        "[PRESS ENTER TO BEGIN]"
    ],
    LANG_IT: [
        "PROTOCOLLO 81: RESET COGNITIVO",
        "SOGGETTO: [OMISSIS]",
        "STATO: CRITICO",
        "",
        "Ti stai immergendo nel tuo stesso subconscio.",
        "Strato dopo strato, strappi via il trauma.",
        "",
        "Trova le chiavi della tua memoria.",
        "Non lasciare che le ombre ti divorino.",
        "",
        "[PREMI ENTER PER INIZIARE]"
    ]
}

ENDING_TEXT_LANG = {
    "BAD": {
        LANG_EN: [
            "MIND BROKEN",
            "",
            "You couldn't face your demons.",
            "The trauma consumed you.",
            "You remain in the coma forever.",
            "",
            "[R] RESTART"
        ],
        LANG_IT: [
            "MENTE SPEZZATA",
            "",
            "Non sei riuscito ad affrontare i tuoi demoni.",
            "Il trauma ti ha consumato.",
            "Rimani in coma per sempre.",
            "",
            "[R] RICOMINCIA"
        ]
    },
    "NEUTRAL": {
        LANG_EN: [
            "WAKE UP?",
            "",
            "You open your eyes.",
            "The hospital lights are blinding.",
            "You are alive.",
            "But something followed you back.",
            "You see static in the mirror.",
            "",
            "[R] RESTART"
        ],
        LANG_IT: [
            "TI SEI SVEGLIATO?",
            "",
            "Apri gli occhi.",
            "Le luci dell'ospedale ti accecano.",
            "Sei vivo.",
            "Ma qualcosa ti ha seguito fuori.",
            "Vedi la neve nel riflesso dello specchio.",
            "",
            "[R] RICOMINCIA"
        ]
    },
    "TRUE": {
        LANG_EN: [
            "CATHARSIS",
            "",
            "You confronted every shadow.",
            "You accepted the pain.",
            "You walk out of the childhood home.",
            "The sun is shining.",
            "The static is gone.",
            "You are finally free.",
            "",
            "[ESC] END SESSION"
        ],
        LANG_IT: [
            "CATARSI",
            "",
            "Hai affrontato ogni ombra.",
            "Hai accettato il dolore.",
            "Esci dalla casa dell'infanzia.",
            "Il sole splende.",
            "La neve nello specchio è sparita.",
            "Sei finalmente libero.",
            "",
            "[ESC] FINE SESSIONE"
        ]
    }
}


# --- SISTEMA LORE E LIVELLI AGGIORNATO ---
LEVEL_DATA = {
    1: {
        "name": "THE HOSPITAL",
        "intro_text": {
            LANG_EN: [
                "LAYER 1: PHYSICAL TRAUMA",
                "The smell of antiseptic. The beeping machines.",
                "They said the surgery was a success.",
                "But when I looked in the mirror...",
                "The face looking back wasn't mine."
            ],
            LANG_IT: [
                "LAYER 1: TRAUMA FISICO",
                "L'odore di disinfettante. Il bip delle macchine.",
                "Hanno detto che l'operazione è andata bene.",
                "Ma quando ho guardato nello specchio...",
                "Il volto che mi fissava non era il mio."
            ]
        },
        "music": "level1.mp3",
        "lore_char": 'C',
        "lore_desc": {
            LANG_EN: "Medical Chart",
            LANG_IT: "Cartella clinica"
        },
        "npcs": [
            {
                "name": "Bandaged Patient",
                "dialogue": {
                    "title": {
                        LANG_EN: "Bandaged Patient",
                        LANG_IT: "Paziente bendato"
                    },
                    "intro": {
                        LANG_EN: "Do I look normal to you?",
                        LANG_IT: "Ti sembro normale?"
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "You look fine.",
                                LANG_IT: "Sembri a posto."
                            },
                            "a": {
                                LANG_EN: "Liar. I see the static in your eyes.",
                                LANG_IT: "Bugiardo. Vedo la neve nei tuoi occhi."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "We are all broken.",
                                LANG_IT: "Siamo tutti rotti."
                            },
                            "a": {
                                LANG_EN: "Maybe fixing us is the mistake. Take this.",
                                LANG_IT: "Forse cercare di aggiustarci è l'errore. Tieni."
                            },
                            "sanity": 15
                        },
                        {
                            "q": {
                                LANG_EN: "Where is the exit?",
                                LANG_IT: "Dov'è l'uscita?"
                            },
                            "a": {
                                LANG_EN: "Follow the blood trail. It goes North.",
                                LANG_IT: "Segui la scia di sangue. Va a Nord."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "Head Nurse",
                "dialogue": {
                    "title": {
                        LANG_EN: "Lost Boy",
                        LANG_IT: "Bambino smarrito"
                    },
                    "intro": {
                        LANG_EN: "Visiting hours are over. Forever.",
                        LANG_IT: "L'orario di visita è finito. Per sempre."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I need to leave.",
                                LANG_IT: "Devo andare via."
                            },
                            "a": {
                                LANG_EN: "No discharge papers for the damned.",
                                LANG_IT: "Nessuna lettera di dimissione per i dannati."
                            }
                        },
                        {
                            "q": {
                                LANG_EN: "What is this place?",
                                LANG_IT: "Che cos'è questo posto?"
                            },
                            "a": {
                                LANG_EN: "A waiting room for the end.",
                                LANG_IT: "Una sala d'attesa per la fine."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "Help me.",
                                LANG_IT: "Aiutami."
                            },
                            "a": {
                                LANG_EN: "Take your pills.",
                                LANG_IT: "Prendi le tue pillole."
                            },
                            "sanity": 10
                        }
                    ]
                }
            },
            {
                "name": "The Janitor",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Janitor",
                        LANG_IT: "Custode"
                    },
                    "intro": {
                        LANG_EN: "I keep mopping, but the stains won't come out.",
                        LANG_IT: "Continuo a pulire, ma le macchie non vanno via."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "It looks clean.",
                                LANG_IT: "Sembra pulito."
                            },
                            "a": {
                                LANG_EN: "Look closer. It's under the floor.",
                                LANG_IT: "Guarda meglio. È sotto il pavimento."
                            },
                            "sanity": -10
                        },
                        {
                            "q": {
                                LANG_EN: "Let me help.",
                                LANG_IT: "Lascia che ti aiuti."
                            },
                            "a": {
                                LANG_EN: "Don't touch it! It spreads.",
                                LANG_IT: "Non toccarlo! Si diffonde."
                            },
                            "sanity": 5
                        },
                        {
                            "q": {
                                LANG_EN: "Exit?",
                                LANG_IT: "Uscita?"
                            },
                            "a": {
                                LANG_EN: "Down the hall. Mind the wet floor.",
                                LANG_IT: "In fondo al corridoio. Attento al pavimento bagnato."
                            },
                            "hint": True
                        }
                    ]
                }
            }
        ],
        "bizarre_objects": [
            {
                LANG_EN: "A bleeding IV stand",
                LANG_IT: "Una flebo che sanguina"
            },
            {
                LANG_EN: "A jar of eyes",
                LANG_IT: "Un barattolo di occhi"
            },
            {
                LANG_EN: "A wheelchair moving alone",
                LANG_IT: "Una sedia a rotelle che si muove da sola"
            }
        ]
    },

    2: {
        "name": "PRIMARY SCHOOL",
        "intro_text": {
            LANG_EN: [
                "LAYER 2: SOCIAL ANXIETY",
                "The laughter of children.",
                "The eyes staring at you in the hallway.",
                "You wanted to disappear.",
                "So you started erasing yourself."
            ],
            LANG_IT: [
                "LAYER 2: ANSIA SOCIALE",
                "Le risate dei bambini.",
                "Gli sguardi fissi su di te nel corridoio.",
                "Volevi scomparire.",
                "Così hai iniziato a cancellarti."
            ]
        },
        "music": "level2.mp3",
        "lore_char": 'P',
        "lore_desc": {
            LANG_EN: "Torn Drawing",
            LANG_IT: "Disegno strappato"
        },
        "npcs": [
            {
                "name": "Lost Boy",
                "dialogue": {
                    "title": {
                    LANG_EN: "Lost Boy",
                    LANG_IT: "Bambino smarrito"
                    },
                    "intro": {
                        LANG_EN: "Hide! The teacher is angry.",
                        LANG_IT: "Nasconditi! L'insegnante è arrabbiata."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Why?",
                                LANG_IT: "Perché?"
                            },
                            "a": {
                                LANG_EN: "Because we drew monsters instead of flowers.",
                                LANG_IT: "Perché abbiamo disegnato mostri invece di fiori."
                            }
                        },
                        {
                            "q": {
                                LANG_EN: "Where is she?",
                                LANG_IT: "Dov'è?"
                            },
                            "a": {
                                LANG_EN: "Everywhere. In the chalk, in the walls.",
                                LANG_IT: "Ovunque. Nel gesso, nei muri."
                            }
                        },
                        {
                            "q": {
                                LANG_EN: "Come with me.",
                                LANG_IT: "Vieni con me."
                            },
                            "a": {
                                LANG_EN: "I can't leave the corner. I'm in timeout forever.",
                                LANG_IT: "Non posso lasciare l'angolo. Sono in castigo per sempre."
                            }
                        }
                    ]
                }
            },
            {
                "name": "The Bully",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Bully",
                        LANG_IT: "Bullo"
                    },
                    "intro": {
                        LANG_EN: "Look at him. He doesn't even have a face.",
                        LANG_IT: "Guardalo. Non ha nemmeno un volto."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Leave me alone.",
                                LANG_IT: "Lasciami in pace."
                            },
                            "a": {
                                LANG_EN: "Or what? You'll cry static?",
                                LANG_IT: "E se no? Piangerai neve?"
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "I am strong.",
                                LANG_IT: "Sono forte."
                            },
                            "a": {
                                LANG_EN: "We'll see about that.",
                                LANG_IT: "Vedremo se è vero."
                            },
                            "sanity": 10
                        },
                        {
                            "q": {
                                LANG_EN: "Move.",
                                LANG_IT: "Spostati."
                            },
                            "a": {
                                LANG_EN: "Fine. The door is that way, freak.",
                                LANG_IT: "Va bene. La porta è da quella parte, mostro."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "The Principal",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Principal",
                        LANG_IT: "Preside"
                    },
                    "intro": {
                        LANG_EN: "You are late for class.",
                        LANG_IT: "Sei in ritardo per la lezione."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I graduated.",
                                LANG_IT: "Mi sono diplomato."
                            },
                            "a": {
                                LANG_EN: "You never leave this school.",
                                LANG_IT: "Da questa scuola non esci mai."
                            },
                            "sanity": -10
                        },
                        {
                            "q": {
                                LANG_EN: "I'm sorry.",
                                LANG_IT: "Mi dispiace."
                            },
                            "a": {
                                LANG_EN: "Apologies don't fix grades.",
                                LANG_IT: "Le scuse non aggiustano i voti."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "Let me pass.",
                                LANG_IT: "Fammi passare."
                            },
                            "a": {
                                LANG_EN: "Proceed to the next lesson.",
                                LANG_IT: "Procedi alla lezione successiva."
                            },
                            "hint": True
                        }
                    ]
                }
            }
        ],

        "bizarre_objects": [
            "A chalkboard screaming",
            "Desks floating",
            "Raining chalk"
        ]
    },

    3: {
        "name": "THE APARTMENT",
        "intro_text": {
            LANG_EN: [
                "LAYER 3: ISOLATION",
                "The silence of an empty room.",
                "The phone that never rings.",
                "You locked the door to keep them out.",
                "But you locked yourself in with IT."
            ],
            LANG_IT: [
                "LAYER 3: ISOLAMENTO",
                "Il silenzio di una stanza vuota.",
                "Il telefono che non squilla mai.",
                "Hai chiuso la porta per tenerli fuori.",
                "Ma ti sei chiuso dentro con LUI."
            ]
        },
        "music": "level3.mp3",
        "lore_char": 'L',
        "lore_desc": {
            LANG_EN: "Love Letter",
            LANG_IT: "Lettera d'amore"
        },
        "npcs": [
            {
                "name": "The Ex",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Ex",
                        LANG_IT: "Ex"
                    },
                    "intro": {
                        LANG_EN: "I loved you before the change.",
                        LANG_IT: "Ti amavo prima del cambiamento."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I'm still me.",
                                LANG_IT: "Sono sempre io."
                            },
                            "a": {
                                LANG_EN: "No. You are just a shell now.",
                                LANG_IT: "No. Ora sei solo un guscio."
                            },
                            "sanity": -10
                        },
                        {
                            "q": {
                                LANG_EN: "I'm sorry I changed.",
                                LANG_IT: "Mi dispiace di essere cambiato."
                            },
                            "a": {
                                LANG_EN: "It wasn't your fault. Forgive yourself.",
                                LANG_IT: "Non è stata colpa tua. Perdonati."
                            },
                            "sanity": 20
                        },
                        {
                            "q": {
                                LANG_EN: "Where do I go?",
                                LANG_IT: "Dove devo andare?"
                            },
                            "a": {
                                LANG_EN: "Leave the key under the mat. Go East.",
                                LANG_IT: "Lascia la chiave sotto lo zerbino. Vai a est."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "The Landlord",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Landlord",
                        LANG_IT: "Padrone di casa"
                    },
                    "intro": {
                        LANG_EN: "Rent is due. Pay with your memories.",
                        LANG_IT: "L'affitto è dovuto. Paga con i tuoi ricordi."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I have none left.",
                                LANG_IT: "Non me ne restano."
                            },
                            "a": {
                                LANG_EN: "Then we take your skin.",
                                LANG_IT: "Allora prenderemo la tua pelle."
                            },
                            "sanity": -15
                        },
                        {
                            "q": {
                                LANG_EN: "Take this letter.",
                                LANG_IT: "Prendi questa lettera."
                            },
                            "a": {
                                LANG_EN: "Worthless sentiment.",
                                LANG_IT: "Sentimento senza valore."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "I'm leaving.",
                                LANG_IT: "Me ne vado."
                            },
                            "a": {
                                LANG_EN: "Lease terminated. Get out.",
                                LANG_IT: "Contratto terminato. Fuori."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "The Neighbor",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Neighbor",
                        LANG_IT: "Vicino"
                    },
                    "intro": {
                        LANG_EN: "Stop screaming at night.",
                        LANG_IT: "Smetti di urlare la notte."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "It wasn't me.",
                                LANG_IT: "Non ero io."
                            },
                            "a": {
                                LANG_EN: "It was your shadow then.",
                                LANG_IT: "Allora era la tua ombra."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "I'll be quiet.",
                                LANG_IT: "Starò zitto."
                            },
                            "a": {
                                LANG_EN: "The walls are thin. We hear your thoughts.",
                                LANG_IT: "I muri sono sottili. Sentiamo i tuoi pensieri."
                            },
                            "sanity": -10
                        },
                        {
                            "q": {
                                LANG_EN: "Did you see an exit?",
                                LANG_IT: "Hai visto un'uscita?"
                            },
                            "a": {
                                LANG_EN: "Through the vents.",
                                LANG_IT: "Attraverso le prese d'aria."
                            },
                            "hint": True
                        }
                    ]
                }
            }
        ],
        "bizarre_objects": [
            "A TV watching you",
            "Walls breathing",
            "A mirror that shows nothing"
        ]
    },

    4: {
        "name": "THE CEMETERY",
        "intro_text": {
            LANG_EN: [
                "LAYER 4: GRIEF",
                "The cold earth. The smell of rain.",
                "You buried your old self here.",
                "But some things refuse to stay dead.",
                "Dig it up."
            ],
            LANG_IT: [
                "LAYER 4: LUTTO",
                "La terra fredda. L'odore di pioggia.",
                "Hai seppellito il tuo vecchio io qui.",
                "Ma alcune cose si rifiutano di restare morte.",
                "Dissotterrale."
            ]
        },
        "music": "level4.mp3",
        "lore_char": 'T',
        "lore_desc": {
            LANG_EN: "Grave Rubbing",
            LANG_IT: "Calco di tomba"
        },
        "npcs": [
            {
                "name": "Mourner",
                "dialogue": {
                    "title": {
                        LANG_EN: "Mourner",
                        LANG_IT: "Piangente"
                    },
                    "intro": {
                        LANG_EN: "It should have been you in that box.",
                        LANG_IT: "Avresti dovuto esserci tu in quella cassa."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Who died?",
                                LANG_IT: "Chi è morto?"
                            },
                            "a": {
                                LANG_EN: "The person you used to be.",
                                LANG_IT: "La persona che eri un tempo."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "I'm alive.",
                                LANG_IT: "Sono vivo."
                            },
                            "a": {
                                LANG_EN: "Are you sure? Check your pulse.",
                                LANG_IT: "Ne sei sicuro? Controlla il polso."
                            },
                            "sanity": 10
                        },
                        {
                            "q": {
                                LANG_EN: "Move aside.",
                                LANG_IT: "Spostati."
                            },
                            "a": {
                                LANG_EN: "Respect the dead, ghost.",
                                LANG_IT: "Rispetta i morti, fantasma."
                            }
                        }
                    ]
                }
            },
            {
                "name": "The Undertaker",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Undertaker",
                        LANG_IT: "Becchino"
                    },
                    "intro": {
                        LANG_EN: "I have a plot reserved for you.",
                        LANG_IT: "Ho una fossa riservata per te."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Not yet.",
                                LANG_IT: "Non ancora."
                            },
                            "a": {
                                LANG_EN: "Soon. Very soon.",
                                LANG_IT: "Presto. Molto presto."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "I refuse to die.",
                                LANG_IT: "Mi rifiuto di morire."
                            },
                            "a": {
                                LANG_EN: "Death is not a choice.",
                                LANG_IT: "La morte non è una scelta."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "Where is the gate?",
                                LANG_IT: "Dov'è il cancello?"
                            },
                            "a": {
                                LANG_EN: "Past the mausoleum.",
                                LANG_IT: "Oltre il mausoleo."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "The Ghost",
                "dialogue": {
                    "title": {
                        LANG_EN: "The Ghost",
                        LANG_IT: "Fantasma"
                    },
                    "intro": {
                        LANG_EN: "I can't find my name on the stones.",
                        LANG_IT: "Non riesco a trovare il mio nome sulle lapidi."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "You are forgotten.",
                                LANG_IT: "Sei stato dimenticato."
                            },
                            "a": {
                                LANG_EN: "And so are you.",
                                LANG_IT: "E anche tu lo sarai."
                            },
                            "sanity": -20
                        },
                        {
                            "q": {
                                LANG_EN: "I remember you.",
                                LANG_IT: "Io ti ricordo."
                            },
                            "a": {
                                LANG_EN: "Thank you. I feel... lighter.",
                                LANG_IT: "Grazie. Mi sento... più leggero."
                            },
                            "sanity": 20
                        },
                        {
                            "q": {
                                LANG_EN: "Follow the light.",
                                LANG_IT: "Segui la luce."
                            },
                            "a": {
                                LANG_EN: "The light burns.",
                                LANG_IT: "La luce brucia."
                            },
                            "sanity": -5
                        }
                    ]
                }
            }
        ],

        "bizarre_objects": [
            "An open grave",
            "A weeping statue",
            "Flowers that wilt instantly"
        ]
    },

    5: {
        "name": "CHILDHOOD HOME",
        "intro_text": {
            LANG_EN: [
                "LAYER 5: THE ORIGIN",
                "This is where it started.",
                "The first time you felt wrong in your skin.",
                "Your brother is here.",
                "The cat is here.",
                "Confront the core."
            ],
            LANG_IT: [
                "LAYER 5: L'ORIGINE",
                "È qui che tutto è iniziato.",
                "La prima volta che ti sei sentito sbagliato nella tua pelle.",
                "Tuo fratello è qui.",
                "Il gatto è qui.",
                "Affronta il nucleo."
            ]
        },
        "music": "level5.mp3",
        "lore_char": 'o',
        "lore_desc": {
            LANG_EN: "Old Toy",
            LANG_IT: "Vecchio giocattolo"
        },
        "npcs": [
            {
                "name": "Brother",
                "dialogue": {
                    "title": {
                        LANG_EN: "Brother",
                        LANG_IT: "Fratello"
                    },
                    "intro": {
                        LANG_EN: "You're almost there! Don't listen to the static.",
                        LANG_IT: "Ci sei quasi! Non ascoltare la neve."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I'm scared.",
                                LANG_IT: "Ho paura."
                            },
                            "a": {
                                LANG_EN: "I know. But you are strong. You survived.",
                                LANG_IT: "Lo so. Ma sei forte. Sei sopravvissuto."
                            },
                            "sanity": 20
                        },
                        {
                            "q": {
                                LANG_EN: "Is this real?",
                                LANG_IT: "È tutto reale?"
                            },
                            "a": {
                                LANG_EN: "It's the memory of what was real. Wake up.",
                                LANG_IT: "È il ricordo di ciò che era reale. Svegliati."
                            },
                            "sanity": 10
                        },
                        {
                            "q": {
                                LANG_EN: "Where is the end?",
                                LANG_IT: "Dov'è la fine?"
                            },
                            "a": {
                                LANG_EN: "The door to your room. It's the final exit.",
                                LANG_IT: "La porta della tua stanza. È l'uscita finale."
                            },
                            "hint": True
                        }
                    ]
                }
            },
            {
                "name": "Cat",
                "dialogue": {
                    "title": {
                        LANG_EN: "Cat",
                        LANG_IT: "Gatto"
                    },
                    "intro": {
                        LANG_EN: "Meow.",
                        LANG_IT: "Miao."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Pet cat.",
                                LANG_IT: "Accarezza il gatto."
                            },
                            "a": {
                                LANG_EN: "Purr... The cat anchors you to reality.",
                                LANG_IT: "Fusa... Il gatto ti ancora alla realtà."
                            },
                            "sanity": 15
                        },
                        {
                            "q": {
                                LANG_EN: "Meow?",
                                LANG_IT: "Miao?"
                            },
                            "a": {
                                LANG_EN: "The cat blinks. It knows.",
                                LANG_IT: "Il gatto sbatte le palpebre. Sa tutto."
                            },
                            "sanity": 0
                        },
                        {
                            "q": {
                                LANG_EN: "Ignore.",
                                LANG_IT: "Ignora."
                            },
                            "a": {
                                LANG_EN: "The cat walks away.",
                                LANG_IT: "Il gatto se ne va."
                            }
                        }
                    ]
                }
            },
            {
                "name": "Mother's Shadow",
                "dialogue": {
                    "title": {
                        LANG_EN: "Mother's Shadow",
                        LANG_IT: "Ombra della madre"
                    },
                    "intro": {
                        LANG_EN: "You were such a beautiful child.",
                        LANG_IT: "Eri un bambino così bello."
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "I'm hideous.",
                                LANG_IT: "Sono orribile."
                            },
                            "a": {
                                LANG_EN: "Shhh. Let me fix you.",
                                LANG_IT: "Shhh. Lascia che ti aggiusti."
                            },
                            "sanity": -20
                        },
                        {
                            "q": {
                                LANG_EN: "I am enough.",
                                LANG_IT: "Sono abbastanza."
                            },
                            "a": {
                                LANG_EN: "...",
                                LANG_IT: "..."
                            },
                            "sanity": 20
                        },
                        {
                            "q": {
                                LANG_EN: "Go away.",
                                LANG_IT: "Vattene."
                            },
                            "a": {
                                LANG_EN: "I am always with you.",
                                LANG_IT: "Sono sempre con te."
                            }
                        }
                    ]
                }
            },
            {
                "name": "Father's Chair",
                "dialogue": {
                    "title": {
                        LANG_EN: "Father's Chair",
                        LANG_IT: "Sedia del padre"
                    },
                    "intro": {
                        LANG_EN: "(The chair creaks, but no one is there)",
                        LANG_IT: "(La sedia scricchiola, ma non c'è nessuno)"
                    },
                    "options": [
                        {
                            "q": {
                                LANG_EN: "Sit down.",
                                LANG_IT: "Siediti."
                            },
                            "a": {
                                LANG_EN: "You feel cold hands on your shoulders.",
                                LANG_IT: "Senti mani fredde sulle spalle."
                            },
                            "sanity": -10
                        },
                        {
                            "q": {
                                LANG_EN: "Stare at it.",
                                LANG_IT: "Fissala."
                            },
                            "a": {
                                LANG_EN: "The newspaper rustles.",
                                LANG_IT: "Il giornale fruscia."
                            },
                            "sanity": -5
                        },
                        {
                            "q": {
                                LANG_EN: "Leave.",
                                LANG_IT: "Vai via."
                            },
                            "a": {
                                LANG_EN: "Wise choice.",
                                LANG_IT: "Saggia scelta."
                            }
                        }
                    ]
                }
            }
        ],

        "bizarre_objects": [
            "A burning crib",
            "Photos with no faces",
            "The clock stuck at 3:00"
        ]
    }
}


LORE_INTRO = [
    "PROTOCOL 81: COGNITIVE RESET",
    "SUBJECT: [REDACTED]",
    "STATUS: CRITICAL",
    "",
    "You are diving into your own subconscious.",
    "Layer by layer, peeling back the trauma.",
    "",
    "Find the keys to your memory.",
    "Don't let the shadows consume you.",
    "",
    "[PRESS ENTER TO BEGIN]"
]

ENDING_BAD = [
    "MIND BROKEN",
    "",
    "You couldn't face your demons.",
    "The trauma consumed you.",
    "You remain in the coma forever.",
    "",
    "[R] RESTART"
]

ENDING_NEUTRAL = [
    "WAKE UP?",
    "",
    "You open your eyes.",
    "The hospital lights are blinding.",
    "You are alive.",
    "But something followed you back.",
    "You see static in the mirror.",
    "",
    "[R] RESTART"
]

ENDING_TRUE = [
    "CATHARSIS",
    "",
    "You confronted every shadow.",
    "You accepted the pain.",
    "You walk out of the childhood home.",
    "The sun is shining.",
    "The static is gone.",
    "You are finally free.",
    "",
    "[ESC] END SESSION"
]

def log_crash(e):
    try:
        with open(CRASH_LOG, "w") as f:
            f.write(traceback.format_exc())
    except: pass

class SoundManager:
    def __init__(self):
        self.active = False
        self.status_msg = "Audio Init..."
        self.current_track = None
        self.scream_sound = None
        
        if HAS_AUDIO:
            try:
                # Tenta inizializzazione standard senza pre-configurazione (più compatibile)
                pygame.mixer.init()
                self.active = True
                self.status_msg = "Pygame Active"
                
                # Check for any jump sound availability
                found_sounds = [f for f in JUMP_SOUND_FILES if os.path.exists(f)]
                if found_sounds:
                    self.status_msg = f"{len(found_sounds)} Jumpscares"
                else:
                    self.status_msg = "No Jump Snds"

            except Exception as e:
                self.status_msg = f"Err: {str(e)[:15]}" # Capture specific error
        else:
            self.status_msg = "Pygame Missing"

    def play_music(self, track_name):
        if self.active and track_name != self.current_track:
            try:
                if os.path.exists(track_name):
                    pygame.mixer.music.load(track_name)
                    pygame.mixer.music.play(-1) 
                    pygame.mixer.music.set_volume(0.4)
                    self.current_track = track_name
                # Se manca il file, aggiorna il messaggio di status per debug
                else:
                    self.status_msg = f"Missing: {track_name}"
            except: pass
    
    def stop_music(self):
        if self.active:
            try:
                pygame.mixer.music.stop()
                self.current_track = None
            except: pass

    def play_scream(self):
        if self.active:
            try:
                # Pick a random sound file
                available_files = [f for f in JUMP_SOUND_FILES if os.path.exists(f)]
                if available_files:
                    choice = random.choice(available_files)
                    pygame.mixer.Sound(choice).play()
            except: pass

class Particle:
    def __init__(self, x, y, char, color, life):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.life = life

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class NPC:
    def __init__(self, x, y, name, dialogue_data):
        self.x = x
        self.y = y
        self.name = name
        self.dialogue_data = dialogue_data # Dict {intro, options}
        self.char = name[0]

class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.stun_timer = 0 
        self.anim_offset = random.randint(0, len(SHADOW_FRAMES)-1)

    def get_display_char(self, tick):
        idx = (tick + self.anim_offset) // 2 % len(SHADOW_FRAMES)
        return SHADOW_FRAMES[idx]

    def move_towards(self, target_x, target_y, map_data, entities):
        if self.stun_timer > 0:
            self.stun_timer -= 1
            return

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            if abs(dx) > abs(dy):
                step_x = 1 if dx > 0 else -1
                step_y = 0
            else:
                step_x = 0
                step_y = 1 if dy > 0 else -1
            
            dest_x = self.x + step_x
            dest_y = self.y + step_y

            if (dest_x, dest_y) in map_data:
                blocked = False
                for e in entities:
                    if e.x == dest_x and e.y == dest_y:
                        blocked = True
                        break
                if not blocked:
                    self.x = dest_x
                    self.y = dest_y

LANG_EN = "EN"
LANG_IT = "IT"

UI_TEXT = {
    LANG_EN: {
        # MENU
        "MENU_TITLE": "PROJECT: DYSMORPHIA",
        "MENU_SUB": "Are you Human (@) or Monster (%)?",
        "MENU_NEW": "[ENTER] New Game",
        "MENU_CONT": "[C] Continue",
        "MENU_DEBUG": "[D] Debug Room",
        "MENU_QUIT": "[ESC] Quit",
        "MENU_CONTROLS": "CONTROLS:",
        "MENU_CONTROLS_LINE": "[ARROWS] Move  [SPACE] Scream  [T] Debug  [M] Menu",
        "MENU_LANGUAGE": "Language",
        "AUDIO_LABEL": "AUDIO",

        "PRESS_ENTER": "[PRESS ENTER]",
        "PRESS_START": "[PRESS ENTER TO BEGIN]",

        "DIALOGUE_CLOSE": "[SPACE] Close",

        "GAMEOVER_RESTART": "[R] RESTART",
        "ENDING_EXIT": "[ESC] END SESSION",

        # HUD
        "HUD_SANITY": "SANITY",
        "HUD_LAYER": "LAYER",
        "HUD_WEAPON": "WEAPON",
        "HUD_HUMAN": "HUMAN",
        "HUD_MONSTER": "MONSTER",
        "HUD_WEAPON_NONE": "[NONE]",
        "HUD_WEAPON_SPIKE": "[KNIFE /]",

        # Messaggi gameplay
        "MSG_SPIKE_ACQUIRED": "GLITCH SPIKE ACQUIRED.",
        "MSG_SPIKE_ACTIVATED": "SPIKE ACTIVATED. THREATS NEUTRALIZED.",
        "MSG_MENTAL_SCREAM": "MENTAL SCREAM RELEASED!",
        "MSG_STUNNED_ENTITIES": "STUNNED {count} ENTITIES.",
        "MSG_SCREAM_VOID": "SCREAM ECHOED IN VOID.",
        "MSG_NOT_ENOUGH_SANITY": "NOT ENOUGH SANITY!",
        "MSG_REALITY_STABILIZED": "REALITY STABILIZED. (+20 SANITY)",
        "MSG_SHADOW_HURTS": "THE SHADOW HURTS YOU!",
        "MSG_FOUND_LORE": "Found: {lore}",

        # Oggetti / specchi
        "MSG_MIRROR_FACE": "A distorted face stares back...",
        "MSG_MIRROR_STATIC": "Your reflection dissolves into static.",

        "MSG_YOU_SEE": "You see: {obj}",
    },

    LANG_IT: {
        # MENU
        "MENU_TITLE": "PROJECT: DYSMORPHIA",
        "MENU_SUB": "Sei Umano (@) o Mostro (%)?",
        "MENU_NEW": "[ENTER] Nuova Partita",
        "MENU_CONT": "[C] Continua",
        "MENU_DEBUG": "[D] Stanza Debug",
        "MENU_QUIT": "[ESC] Esci",
        "MENU_CONTROLS": "COMANDI:",
        "MENU_CONTROLS_LINE": "[FRECCE] Muovi  [SPAZIO] Urla  [T] Debug  [M] Menu",
        "MENU_LANGUAGE": "Lingua",
        "AUDIO_LABEL": "AUDIO",

        "PRESS_ENTER": "[PREMI ENTER]",
        "PRESS_START": "[PREMI ENTER PER INIZIARE]",

        "DIALOGUE_CLOSE": "[SPAZIO] Chiudi",

        "GAMEOVER_RESTART": "[R] RICOMINCIA",
        "ENDING_EXIT": "[ESC] FINE SESSIONE",

        # HUD
        "HUD_SANITY": "SANITÀ",
        "HUD_LAYER": "LIVELLO",
        "HUD_WEAPON": "ARMA",
        "HUD_HUMAN": "UMANO",
        "HUD_MONSTER": "MOSTRO",
        "HUD_WEAPON_NONE": "[NESSUNA]",
        "HUD_WEAPON_SPIKE": "[COLTELLO /]",

        # Messaggi gameplay
        "MSG_SPIKE_ACQUIRED": "GLITCH SPIKE ACQUISITO.",
        "MSG_SPIKE_ACTIVATED": "SPINA ATTIVATA. MINACCE NEUTRALIZZATE.",
        "MSG_MENTAL_SCREAM": "URLO MENTALE RILASCIATO!",
        "MSG_STUNNED_ENTITIES": "STORDITE {count} ENTITÀ.",
        "MSG_SCREAM_VOID": "L'URLO SI PERDE NEL VUOTO.",
        "MSG_NOT_ENOUGH_SANITY": "SANITÀ INSUFFICIENTE!",
        "MSG_REALITY_STABILIZZATA": "REALTÀ STABILIZZATA. (+20 SANITÀ)",  # se vuoi mantieni il nome chiave uguale
        "MSG_REALITY_STABILIZED": "REALTÀ STABILIZZATA. (+20 SANITÀ)",    # oppure usa questa chiave, come in EN
        "MSG_SHADOW_HURTS": "L'OMBRA TI FERISCE!",
        "MSG_FOUND_LORE": "Trovato: {lore}",

        # Oggetti / specchi
        "MSG_MIRROR_FACE": "Un volto distorto ti fissa...",
        "MSG_MIRROR_STATIC": "Il tuo riflesso si dissolve nella neve.",

        "MSG_YOU_SEE": "Vedi: {obj}",
    }
}


class Game:
        def __init__(self, stdscr):
            self.language = LANG_EN
            self.stdscr = stdscr
            self.height, self.width = stdscr.getmaxyx()
            self.state = STATE_MENU
            self.sound_manager = SoundManager()
            self.sound_manager.play_music(MUSIC_TRACKS["MENU"])

            self.map_data = {}
            self.rooms = []
            self.mirrors = []
            self.enemies = []
            self.items = []
            self.lore_items = []
            self.weapons = []
            self.npcs = []          # Lista NPC
            self.bizarre_objs = []  # Oggetti bizzarri
            self.particles = []
            self.memory_map = set()
            self.exit_pos = None

            self.player_x = 0
            self.player_y = 0
            self.player_facing = (0, 1)
            self.player_form = '@'
            self.has_weapon = False
            self.sanity = 100.0
            self.level = 1
            self.message = ""
            self.collected_lore = []

            self.god_mode = False
            self.debug_mode = False      # <- flag run di debug
            self.debug_reveal = False    # <- toggle R in debug

            self.last_move_time = 0      # Per delay movimento
            self.shake_intensity = 0
            self.turn_counter = 0
            self.global_tick = 0

            # JUMPSCARE SYSTEM
            self.jumpscare_timer = 0
            self.jumpscare_active = False
            self.jumpscare_cooldown = 0
            self.current_jumpscare_art = []
            self.final_text = []
            self.final_color = COLOR_TEXT

            # DIALOGUE SYSTEM
            self.active_npc = None
            self.dialogue_selection = 0
            self.dialogue_response = ""


        def start_new_game(self):
            self.sanity = 100.0
            self.level = 1
            self.player_facing = (0, 1)
            self.has_weapon = False
            self.god_mode = False
            self.debug_mode = False      # esci dalla debug mode
            self.debug_reveal = False
            self.message = ""
            self.collected_lore = []
            self.state = STATE_INTRO

        def start_debug_mode(self):
            self.sanity = 100.0
            self.level = 0
            self.player_facing = (0, 1)
            self.has_weapon = True
            self.god_mode = False
            self.debug_mode = True       # entri in debug mode
            self.debug_reveal = False
            self.message = "DEBUG: 'G' God Mode, 'J' Jumpscare, 'R' Reveal."
            self.collected_lore = []
            self.setup_debug_level()
            self.state = STATE_PLAYING

        def save_game(self):
            data = {
                'map_data': self.map_data,
                'rooms': self.rooms,
                'enemies': self.enemies,
                'items': self.items,
                'lore_items': self.lore_items,
                'weapons': self.weapons,
                'memory_map': self.memory_map,
                'exit_pos': self.exit_pos,
                'player_x': self.player_x,
                'player_y': self.player_y,
                'player_facing': self.player_facing,
                'has_weapon': self.has_weapon,
                'sanity': self.sanity,
                'level': self.level,
                'collected_lore': self.collected_lore
            }
            try:
                with open(SAVE_FILE, 'wb') as f:
                    pickle.dump(data, f)
                return True
            except Exception as e:
                self.message = f"SAVE ERROR: {e}"
                return False

        def load_game(self):
            if not os.path.exists(SAVE_FILE):
                return False
            try:
                with open(SAVE_FILE, 'rb') as f:
                    data = pickle.load(f)
                
                self.map_data = data['map_data']
                self.rooms = data['rooms']
                self.enemies = data['enemies']
                self.items = data['items']
                self.lore_items = data['lore_items']
                self.weapons = data.get('weapons', [])
                self.memory_map = data['memory_map']
                self.exit_pos = data['exit_pos']
                self.player_x = data['player_x']
                self.player_y = data['player_y']
                self.player_facing = data.get('player_facing', (0, 1))
                self.has_weapon = data.get('has_weapon', False)
                self.sanity = data['sanity']
                self.level = data['level']
                self.collected_lore = data['collected_lore']
                
                self.message = "GAME LOADED."
                self.setup_level(loading=True) 
                self.state = STATE_PLAYING
                return True
            except Exception as e:
                self.message = f"LOAD ERROR: Corrupted File."
                return False

        def setup_level(self, loading=False):
            # NOTA: La musica ora parte in STATE_LEVEL_INTRO
            if loading: 
                return

            self.map_data = {} 
            self.rooms = []
            self.mirrors = []
            self.enemies = []
            self.items = []
            self.lore_items = []
            self.weapons = []
            self.npcs = []
            self.bizarre_objs = []
            self.particles = []
            self.memory_map = set()
            self.exit_pos = None
            self.player_x = 0
            self.player_y = 0
            
            self.make_map()
            
            # Start music for this level IMMEDIATELY for the intro screen
            track = MUSIC_TRACKS.get(self.level, MUSIC_TRACKS[1])
            self.sound_manager.play_music(track)
            
            self.state = STATE_LEVEL_INTRO # Vai alla schermata di lore del livello

        def setup_debug_level(self):
            self.map_data = {}
            self.rooms = []
            self.mirrors = []
            self.enemies = []
            self.items = []
            self.lore_items = []
            self.weapons = []
            self.npcs = []
            self.bizarre_objs = []
            self.particles = []
            self.memory_map = set()
            self.exit_pos = None

            room_w = 60
            room_h = 20
            x1 = (self.width - room_w) // 2
            y1 = (self.height - room_h) // 2

            debug_room = Room(x1, y1, room_w, room_h)
            self.create_room(debug_room)
            self.rooms.append(debug_room)

            cx, cy = debug_room.center()
            self.player_x = x1 + 3
            self.player_y = cy

            # ARMI E ITEM base
            self.weapons.append((self.player_x + 2, self.player_y))
            self.items.append((self.player_x + 2, self.player_y + 2))
            self.mirrors.append((self.player_x + 2, self.player_y - 2))

            # NEMICO di test
            self.enemies.append(Entity(x1 + room_w - 5, cy, ENEMY_CHAR, COLOR_ENEMY))

            # --- TUTTI GLI NPC DI TUTTI I LIVELLI ---
            npc_x = x1 + 8
            npc_y = y1 + 3
            for lvl in range(1, 6):
                theme = LEVEL_DATA[lvl]
                for npc_data in theme['npcs']:
                    if npc_x < x1 + room_w - 2:
                        self.npcs.append(NPC(npc_x, npc_y, npc_data['name'], npc_data['dialogue']))
                        npc_x += 3
                npc_x += 2

            # --- OGGETTI BIZZARRI DI TUTTI I LIVELLI ---
            obj_x = x1 + 8
            obj_y = y1 + room_h - 3
            for lvl in range(1, 6):
                theme = LEVEL_DATA[lvl]
                if 'bizarre_objects' in theme:
                    self.bizarre_objs.append((obj_x, obj_y))
                    obj_x += 4

            # --- LORE ITEMS DI TUTTI I LIVELLI ---
            lore_x = x1 + 15
            lore_y = cy + 2
            for lvl in range(1, 6):
                self.lore_items.append((lore_x, lore_y))
                lore_x += 3

            # Uscita della debug room
            self.exit_pos = (x1 + room_w - 2, cy)
            self.map_data[self.exit_pos] = EXIT_CHAR

            # Svela tutta la stanza in memoria
            for x in range(x1, x1 + room_w):
                for y in range(y1, y1 + room_h):
                    self.memory_map.add((x, y))

        def next_level(self):
            if self.level >= MAX_LEVELS:
                self.check_ending() 
                if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
            else:
                self.level += 1
                self.sanity = min(100, self.sanity + 15)
                self.sound_manager.stop_music() # Stop musica precedente
                self.setup_level() # Prepara e va in STATE_LEVEL_INTRO
                self.save_game()

        def create_room(self, room):
            for x in range(room.x1 + 1, room.x2):
                for y in range(room.y1 + 1, room.y2):
                    self.map_data[(x, y)] = FLOOR_CHAR

        def create_h_tunnel(self, x1, x2, y):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map_data[(x, y)] = FLOOR_CHAR

        def create_v_tunnel(self, y1, y2, x):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map_data[(x, y)] = FLOOR_CHAR

        def make_map(self):
            MAX_ROOMS = 15
            ROOM_MIN_SIZE = 5
            ROOM_MAX_SIZE = 12

            for _ in range(MAX_ROOMS):
                w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                x = random.randint(1, self.width - w - 2)
                y = random.randint(1, self.height - h - 2)

                new_room = Room(x, y, w, h)

                failed = False
                for other_room in self.rooms:
                    if new_room.intersect(other_room):
                        failed = True
                        break

                if not failed:
                    self.create_room(new_room)
                    (new_x, new_y) = new_room.center()

                    if len(self.rooms) == 0:
                        self.player_x = new_x
                        self.player_y = new_y
                    else:
                        (prev_x, prev_y) = self.rooms[-1].center()
                        if random.randint(0, 1) == 1:
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    enemy_chance = min(0.9, 0.3 + (self.level * 0.1))
                    item_chance = max(0.1, 0.4 - (self.level * 0.05))
                    weapon_chance = max(0.15, 0.45 - (self.level * 0.075))

                    if len(self.rooms) > 0 and random.random() < enemy_chance:
                        self.spawn_enemy(new_room)
                    if random.random() < item_chance:
                        self.spawn_feature(new_room, self.items)
                    if random.random() < 0.2:
                        self.spawn_feature(new_room, self.lore_items)
                    if random.random() < weapon_chance:
                        self.spawn_feature(new_room, self.weapons)
                    if random.random() < 0.3:
                        self.spawn_feature(new_room, self.mirrors)

                    # Oggetti bizzarri random
                    if random.random() < 0.2:
                        self.spawn_bizarre(new_room)

                    self.rooms.append(new_room)

            # --- SOLO UNA VOLTA DOPO IL FOR ---
            if self.rooms:
                last_room = self.rooms[-1]
                ex, ey = last_room.center()
                self.exit_pos = (ex, ey)
                self.map_data[(ex, ey)] = EXIT_CHAR

                # Spawn degli NPC fissi del livello corrente (3 circa)
                self.spawn_story_npcs()




            if self.rooms:
                last_room = self.rooms[-1]
                ex, ey = last_room.center()
                self.exit_pos = (ex, ey)
                self.map_data[(ex, ey)] = EXIT_CHAR

        def spawn_story_npcs(self):
            """Crea solo gli NPC di storia del livello corrente (tipicamente 3)."""

            # NIENTE NPC DI STORIA IN DEBUG ROOM
            if self.level <= 0:
                return

            theme = LEVEL_DATA.get(self.level)
            if not theme or 'npcs' not in theme:
                return
            if not self.rooms:
                return

            rooms_pool = self.rooms[:]
            random.shuffle(rooms_pool)
            room_index = 0

            for npc_data in theme['npcs']:
                room = rooms_pool[room_index % len(rooms_pool)]
                room_index += 1

                cx, cy = room.center()
                placed = False
                attempts = 0

                # Prova a metterlo vicino al centro stanza, evitando sovrapposizioni
                while not placed and attempts < 30:
                    rx = cx + random.randint(-2, 2)
                    ry = cy + random.randint(-2, 2)
                    attempts += 1

                    if (rx, ry) not in self.map_data:
                        continue
                    if (rx, ry) == (self.player_x, self.player_y):
                        continue
                    if any(npc.x == rx and npc.y == ry for npc in self.npcs):
                        continue

                    self.npcs.append(NPC(rx, ry, npc_data['name'], npc_data['dialogue']))
                    placed = True



        def spawn_feature(self, room, feature_list):
            (cx, cy) = room.center()
            rx = cx + random.randint(-2, 2)
            ry = cy + random.randint(-2, 2)
            if (rx, ry) in self.map_data and (rx, ry) != (cx, cy):
                feature_list.append((rx, ry))
        
        def spawn_bizarre(self, room):
            (cx, cy) = room.center()
            rx = cx + random.randint(-2, 2)
            ry = cy + random.randint(-2, 2)
            if (rx, ry) in self.map_data and (rx, ry) != (self.player_x, self.player_y):
                self.bizarre_objs.append((rx, ry))

        def spawn_enemy(self, room):
            (cx, cy) = room.center()
            rx = cx + random.randint(-2, 2)
            ry = cy + random.randint(-2, 2)
            if (rx, ry) in self.map_data and (rx, ry) != (self.player_x, self.player_y):
                self.enemies.append(Entity(rx, ry, ENEMY_CHAR, COLOR_ENEMY))
        
        def spawn_npc(self, room):
            (cx, cy) = room.center()
            rx = cx + random.randint(-2, 2)
            ry = cy + random.randint(-2, 2)
            if (rx, ry) in self.map_data and (rx, ry) != (self.player_x, self.player_y):
                theme = LEVEL_DATA.get(self.level, LEVEL_DATA[1])
                # Avoid duplicate NPCs if possible
                existing_names = [n.name for n in self.npcs]
                available_npcs = [n for n in theme['npcs'] if n['name'] not in existing_names]
                
                if not available_npcs: available_npcs = theme['npcs'] # Fallback
                
                npc_data = random.choice(available_npcs)
                self.npcs.append(NPC(rx, ry, npc_data['name'], npc_data['dialogue']))

        def add_particles(self, x, y, count=5, color=COLOR_BLOOD):
            chars = ['*', '.', ',', '`']
            for _ in range(count):
                px = x + random.randint(-1, 1)
                py = y + random.randint(-1, 1)
                if (px, py) in self.map_data:
                    life = random.randint(3, 8)
                    self.particles.append(Particle(px, py, random.choice(chars), color, life))

        def update_particles(self):
            self.particles = [p for p in self.particles if p.life > 0]
            for p in self.particles:
                p.life -= 1

        def trigger_jumpscare(self):
            """Attiva l'evento Jumpscare con immagine casuale"""
            self.jumpscare_active = True
            self.jumpscare_timer = 3 
            self.jumpscare_cooldown = 50 
            self.current_jumpscare_art = random.choice(JUMPSCARE_ARTS) 
            self.sound_manager.play_scream() 
            self.sanity -= 5 

        def draw_jumpscare(self):
            self.stdscr.clear()
            if self.jumpscare_timer % 2 == 0:
                self.stdscr.bkgd(curses.color_pair(COLOR_BLOOD)) 
                color = curses.color_pair(COLOR_WALL) | curses.A_BOLD
            else:
                self.stdscr.bkgd(curses.color_pair(0)) 
                color = curses.color_pair(COLOR_BLOOD) | curses.A_BOLD

            art = self.current_jumpscare_art
            start_y = (self.height - len(art)) // 2
            for i, line in enumerate(art):
                safe_line = line[:self.width-1]
                start_x = (self.width - len(safe_line)) // 2
                try:
                    self.stdscr.addstr(start_y + i, start_x, safe_line, color)
                except: pass
            
            msg = "I SEE YOU"
            self.stdscr.addstr(self.height - 5, (self.width - len(msg))//2, msg, curses.color_pair(COLOR_GLITCH) | curses.A_BLINK)
            self.stdscr.refresh()

        def handle_input(self, key):
            if self.state == STATE_MENU:
                if key == 10:
                    self.start_new_game()
                elif key == ord('c') or key == ord('C'):
                    self.load_game()
                elif key == ord('d') or key == ord('D'):
                    self.start_debug_mode()
                elif key in (ord('l'), ord('L')):  # toggle lingua
                    self.language = LANG_IT if self.language == LANG_EN else LANG_EN
                elif key == 27:
                    return False
                return True

            elif self.state == STATE_INTRO:
                if key == 10 or key == 27:
                    self.setup_level()  # va in STATE_LEVEL_INTRO
                return True

            elif self.state == STATE_LEVEL_INTRO:
                if key == 10 or key == 27:
                    self.state = STATE_PLAYING
                return True

            elif self.state == STATE_ENDING:
                if key == ord('r') or key == ord('R'):
                    # Svela Mappa Base
                    for k in self.map_data.keys():
                        self.memory_map.add(k)
                    # Svela Entità e Oggetti
                    for enemy in self.enemies:
                        self.memory_map.add((enemy.x, enemy.y))
                    for npc in self.npcs:
                        self.memory_map.add((npc.x, npc.y))
                    for item in self.items:
                        self.memory_map.add(item)
                    for weapon in self.weapons:
                        self.memory_map.add(weapon)
                    for lore in self.lore_items:
                        self.memory_map.add(lore)
                    for mirror in self.mirrors:
                        self.memory_map.add(mirror)
                    for biz in self.bizarre_objs:
                        self.memory_map.add(biz)
                    self.message = "DEBUG: FULL MAP REVEALED"
                    return True
                return True

            elif self.state == STATE_DIALOGUE:
                # CHIUSURA DIALOGO:
                # - ESC sempre
                # - SPACE solo quando c'è già una risposta mostrata
                if key == 27 or (key == ord(' ') and self.dialogue_response):
                    self.state = STATE_PLAYING
                    self.active_npc = None
                    self.dialogue_response = ""
                    self.dialogue_selection = 0
                    return True

                # SELEZIONE OPZIONE (1, 2, 3, ...)
                if key in (ord('1'), ord('2'), ord('3')):
                    idx = key - ord('1')
                    if not self.active_npc:
                        return True

                    data = self.active_npc.dialogue_data
                    options = data['options']

                    if 0 <= idx < len(options):
                        self.dialogue_selection = idx
                        chosen = options[idx]

                        # Risposta localizzata EN/IT
                        a_data = chosen["a"]
                        if isinstance(a_data, dict):
                            self.dialogue_response = a_data[self.language]
                        else:
                            self.dialogue_response = a_data

                        # Modifica sanità se presente
                        if "sanity" in chosen:
                            self.sanity = max(0, min(100, self.sanity + chosen["sanity"]))

                        # Hint: rivela l'uscita come faceva il vecchio codice
                        if chosen.get("hint") and self.exit_pos is not None:
                            self.memory_map.add(self.exit_pos)
                            ex, ey = self.exit_pos
                            for rx in range(ex - 2, ex + 3):
                                for ry in range(ey - 2, ey + 3):
                                    self.memory_map.add((rx, ry))

                    return True


            elif self.state == STATE_PLAYING:

                # --- JUMPSCARE CHECK SE ATTIVO ---
                if self.jumpscare_active:
                    self.jumpscare_timer -= 1
                    if self.jumpscare_timer <= 0:
                        self.jumpscare_active = False
                        self.stdscr.bkgd(curses.color_pair(0))
                    return True

                # --- INPUT SPECIFICI DI DEBUG (valido su TUTTI i livelli) ---
                if self.debug_mode:
                    if key == ord('g') or key == ord('G'):
                        self.god_mode = not self.god_mode
                        self.message = f"GOD MODE: {'ON' if self.god_mode else 'OFF'}"
                        if self.god_mode:
                            self.has_weapon = True  # auto-equip spike
                        return True

                    if key == ord('j') or key == ord('J'):
                        self.trigger_jumpscare()
                        return True

                    if key == ord('r') or key == ord('R'):
                        self.debug_reveal = not self.debug_reveal
                        if self.debug_reveal:
                            # opzionale: svela comunque tutta la mappa base attuale
                            for k in self.map_data.keys():
                                self.memory_map.add(k)
                            self.message = "DEBUG: FULL REVEAL ON"
                        else:
                            self.message = "DEBUG: FULL REVEAL OFF"
                        return True

                # --- JUMPSCARE RANDOM (solo run normali, NON in debug_mode) ---
                if not self.god_mode and not self.debug_mode:
                    if self.jumpscare_cooldown > 0:
                        self.jumpscare_cooldown -= 1
                    else:
                        level_base = (self.level - 1) * 0.005
                        jumpscare_chance = 0.0 + level_base
                        if self.sanity < 70:
                            jumpscare_chance += 0.005
                        if self.sanity < 40:
                            jumpscare_chance += 0.01
                        if self.sanity < 15:
                            jumpscare_chance += 0.03
                        if random.random() < jumpscare_chance:
                            self.trigger_jumpscare()
                            return True

                # NESSUN R GENERICO QUI: fuori da debug_mode R non fa nulla in PLAYING

                if key == ord('m') or key == ord('M'):
                    self.save_game()
                    self.sound_manager.play_music(MUSIC_TRACKS["MENU"])
                    self.state = STATE_MENU
                    return True

                if key == ord('t') or key == ord('T'):
                    for _ in range(3):
                        ex = self.player_x + random.randint(-4, 4)
                        ey = self.player_y + random.randint(-4, 4)
                        if (ex, ey) in self.map_data:
                            self.enemies.append(Entity(ex, ey, ENEMY_CHAR, COLOR_ENEMY))
                    self.sanity = 100
                    self.message = "DEBUG: ENEMIES SPAWNED"
                    return True

                if key == 32:
                    self.use_pulse()
                    return True

                if key == 27:
                    self.save_game()
                    self.sound_manager.play_music(MUSIC_TRACKS["MENU"])
                    self.state = STATE_MENU
                    return True

                # --- MOVIMENTO ---
                dx, dy = 0, 0
                if key == curses.KEY_DOWN:
                    dy = 1
                elif key == curses.KEY_UP:
                    dy = -1
                elif key == curses.KEY_LEFT:
                    dx = -1
                elif key == curses.KEY_RIGHT:
                    dx = 1

                # MOVEMENT DELAY (Anti-Speedrun)
                current_time = time.time()
                if dx != 0 or dy != 0:
                    if current_time - self.last_move_time < MOVE_DELAY:
                        dx, dy = 0, 0
                    else:
                        self.last_move_time = current_time

                # AURA ATTACK (prima del movimento)
                enemies_killed = False
                if self.has_weapon:
                    enemies_to_remove = []
                    for enemy in self.enemies:
                        dist = math.sqrt((enemy.x - self.player_x) ** 2 + (enemy.y - self.player_y) ** 2)
                        if dist <= 1.5:
                            enemies_to_remove.append(enemy)
                    if enemies_to_remove:
                        for e in enemies_to_remove:
                            self.enemies.remove(e)
                            self.add_particles(e.x, e.y, 15, COLOR_GLITCH)
                        if not self.god_mode:
                            self.has_weapon = False
                        self.message = "SPIKE ACTIVATED. THREATS NEUTRALIZED."
                        self.shake_intensity = 4
                        try:
                            self.stdscr.bkgd(curses.color_pair(COLOR_BLOOD))
                            self.stdscr.refresh()
                            time.sleep(0.05)
                            self.stdscr.bkgd(curses.color_pair(0))
                        except:
                            pass
                        enemies_killed = True

                if dx == 0 and dy == 0:
                    self.update_particles()
                    if self.shake_intensity > 0:
                        self.shake_intensity -= 1
                    return True

                self.player_facing = (dx, dy)
                nx, ny = self.player_x + dx, self.player_y + dy

                enemy_block = False
                for enemy in self.enemies:
                    if enemy.x == nx and enemy.y == ny:
                        self.message = "BLOCKED BY SHADOW. FIND A WEAPON!"
                        enemy_block = True
                        break

                if enemy_block:
                    self.turn_counter += 1
                    if not enemies_killed:
                        self.update_enemies()
                    return True

                if (nx, ny) in self.map_data:
                    if (nx, ny) == self.exit_pos:
                        self.next_level()
                    elif (nx, ny) in self.mirrors:
                        t = UI_TEXT[self.language]
                        self.message = t["MSG_MIRROR_FACE"]
                        self.sanity += 1
                    elif (nx, ny) in self.items:
                        self.consume_item((nx, ny))
                        self.player_x, self.player_y = nx, ny
                    elif (nx, ny) in self.lore_items:
                        self.collect_lore((nx, ny))
                        self.player_x, self.player_y = nx, ny
                    elif (nx, ny) in self.weapons:
                        self.pickup_weapon((nx, ny))
                        self.player_x, self.player_y = nx, ny
                    elif (nx, ny) in self.bizarre_objs:
                        theme = LEVEL_DATA.get(self.level, LEVEL_DATA[1])
                        raw_obj = random.choice(theme["bizarre_objects"])

                        # Scegli descrizione in base alla lingua
                        if isinstance(raw_obj, dict):
                            obj_desc = raw_obj[self.language]
                        else:
                            obj_desc = raw_obj  # compatibilità se in altri livelli non hai ancora messo i dict

                        t = UI_TEXT[self.language]
                        self.message = t["MSG_YOU_SEE"].format(obj=obj_desc)
                    else:
                        # Check NPC Collision
                        npc_hit = False
                        for npc in self.npcs:
                            if npc.x == nx and npc.y == ny:
                                self.active_npc = npc
                                self.state = STATE_DIALOGUE
                                npc_hit = True
                                break
                        if not npc_hit:
                            self.player_x, self.player_y = nx, ny

                # Post-Movimento Aura Check
                if self.has_weapon:
                    enemies_to_remove = []
                    for enemy in self.enemies:
                        dist = math.sqrt((enemy.x - self.player_x) ** 2 + (enemy.y - self.player_y) ** 2)
                        if dist <= 1.5:
                            enemies_to_remove.append(enemy)
                    if enemies_to_remove:
                        for e in enemies_to_remove:
                            self.enemies.remove(e)
                            self.add_particles(e.x, e.y, 15, COLOR_GLITCH)
                        if not self.god_mode:
                            self.has_weapon = False
                        self.message = "SPIKE ACTIVATED. THREATS NEUTRALIZED."
                        self.shake_intensity = 4
                        enemies_killed = True

                self.turn_counter += 1
                if not enemies_killed:
                    self.update_enemies()
                self.update_particles()
                if self.shake_intensity > 0:
                    self.shake_intensity -= 1

                if not self.god_mode:
                    self.sanity -= 0.05
                    if self.sanity <= 0:
                        self.final_text = ENDING_BAD
                        self.final_color = COLOR_ENEMY
                        self.state = STATE_ENDING
                        if os.path.exists(SAVE_FILE):
                            os.remove(SAVE_FILE)
                return True

            elif self.state in [STATE_GAMEOVER, STATE_VICTORY]:
                if key == ord('r') or key == ord('R'):
                    self.start_new_game()
                elif key == 27 or key == ord('m') or key == ord('M'):
                    self.state = STATE_MENU
                return True


            return True

        def pickup_weapon(self, pos):
            if pos in self.weapons:
                self.weapons.remove(pos)
                self.has_weapon = True
                t = UI_TEXT[self.language]
                self.message = t["MSG_SPIKE_ACQUIRED"]

        def animate_pulse(self):
            wave_chars = ['*', 'o', '0', '.', ' ']
            max_radius = 6
            self.shake_intensity = 2

            for r in range(1, max_radius + 1):
                self.draw(animation_frame=True)
                for angle in range(0, 360, 15):
                    rad = math.radians(angle)
                    x = int(self.player_x + r * math.cos(rad) * 1.8)
                    y = int(self.player_y + r * math.sin(rad))
                    if 0 <= x < self.width and 0 <= y < self.height:
                        try:
                            char = random.choice(wave_chars)
                            off_x = random.randint(-1, 1)
                            off_y = random.randint(-1, 1)
                            self.stdscr.addch(
                                y + off_y,
                                x + off_x,
                                char,
                                curses.color_pair(COLOR_GLITCH) | curses.A_BOLD
                            )
                        except:
                            pass
                self.stdscr.refresh()
                time.sleep(0.04)

        def use_pulse(self):
            t = UI_TEXT[self.language]
            if self.sanity > PULSE_COST:
                self.sanity -= PULSE_COST
                self.message = t["MSG_MENTAL_SCREAM"]
                self.sound_manager.play_scream()
                self.animate_pulse()

                count = 0
                for enemy in self.enemies:
                    dist = math.sqrt((enemy.x - self.player_x)**2 + (enemy.y - self.player_y)**2)
                    if dist < 6:
                        enemy.stun_timer = 5
                        push_x = 1 if enemy.x > self.player_x else -1
                        push_y = 1 if enemy.y > self.player_y else -1
                        if (enemy.x + push_x, enemy.y + push_y) in self.map_data:
                            enemy.x += push_x
                            enemy.y += push_y
                        count += 1

                if count > 0:
                    self.message = t["MSG_STUNNED_ENTITIES"].format(count=count)
                else:
                    self.message = t["MSG_SCREAM_VOID"]
            else:
                self.message = t["MSG_NOT_ENOUGH_SANITY"]

        def consume_item(self, pos):
            if pos in self.items:
                self.items.remove(pos)
                self.sanity = min(100, self.sanity + HEAL_AMOUNT)
                t = UI_TEXT[self.language]
                self.message = t["MSG_REALITY_STABILIZED"]

        def consume_item(self, pos):
            if pos in self.items:
                self.items.remove(pos)
                self.sanity = min(100, self.sanity + HEAL_AMOUNT)
                t = UI_TEXT[self.language]
                self.message = t["MSG_REALITY_STABILIZED"]


        def collect_lore(self, pos):
            if pos in self.lore_items:
                self.lore_items.remove(pos)
                self.sanity = min(100, self.sanity + 10)
                
                # Use level lore
                theme = LEVEL_DATA.get(self.level, LEVEL_DATA[1])
                lore_desc = theme["lore_desc"][self.language]

                t = UI_TEXT[self.language]
                # aggiungeremo MSG_FOUND_LORE in UI_TEXT
                lore_msg = t["MSG_FOUND_LORE"].format(lore=lore_desc)

                self.collected_lore.append(lore_msg)
                self.message = lore_msg


        def update_enemies(self):
            for enemy in self.enemies:
                dist = math.sqrt((enemy.x - self.player_x)**2 + (enemy.y - self.player_y)**2)
                
                if dist < 1.5:
                    if not self.god_mode:
                        self.sanity -= ENEMY_DAMAGE 
                    
                    t = UI_TEXT[self.language]
                    self.message = t["MSG_SHADOW_HURTS"]
                    self.shake_intensity = 3
                    self.add_particles(self.player_x, self.player_y, 8, COLOR_BLOOD)
                    
                    enemy.stun_timer = 2 
                    next_x, next_y = self.player_x, self.player_y
                    if self.player_x != enemy.x: next_x -= (enemy.x - self.player_x)
                    if self.player_y != enemy.y: next_y -= (enemy.y - self.player_y)
                    
                    if (next_x, next_y) in self.map_data:
                        self.player_x = next_x
                        self.player_y = next_y
                
                elif dist < 8:
                    enemy.move_towards(self.player_x, self.player_y, self.map_data, self.enemies)

        # 
        def trigger_mirror_event(self):
            t = UI_TEXT[self.language]
            self.message = t["MSG_MIRROR_FACE"]

        def is_visible(self, x, y):
            # VISIBILITY RANGE SCALING:
            # Level 1: Radius 6, Level 5: Radius 3.5
            level_reduction = (self.level - 1) * 0.6
            base_radius = max(3.5, 6 - level_reduction)
            
            breathing = math.sin(self.global_tick * 0.15) * 1.5
            radius = base_radius + breathing
            
            dist = math.sqrt((x - self.player_x)**2 + (y - self.player_y)**2)
            return dist <= radius

        def draw(self, animation_frame=False):
            # Se c'è un jumpscare attivo, disegna SOLO quello
            if self.jumpscare_active:
                self.draw_jumpscare()
                return

            self.stdscr.clear()

            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_INTRO:
                self.draw_intro()
            elif self.state == STATE_LEVEL_INTRO:
                self.draw_level_intro()
            elif self.state == STATE_ENDING:
                self.draw_ending()
            elif self.state == STATE_PLAYING:
                self.draw_game()
            elif self.state == STATE_DIALOGUE:
                # Disegna gioco sotto, poi box del dialogo
                self.draw_game()
                self.draw_dialogue()
            elif self.state == STATE_GAMEOVER:
                self.draw_gameover()
            elif self.state == STATE_VICTORY:
                self.draw_victory()

            if not animation_frame:
                self.stdscr.refresh()


        def draw_menu(self):
            h, w = self.height, self.width
            t = UI_TEXT[self.language]

            self.stdscr.addstr(h//2 - 6, w//2 - 10,
                            t["MENU_TITLE"], curses.color_pair(COLOR_TITLE) | curses.A_BOLD)
            self.stdscr.addstr(h//2 - 4, w//2 - 20,
                            t["MENU_SUB"], curses.color_pair(COLOR_TEXT))
            self.stdscr.addstr(h//2 - 1, w//2 - 12,
                            t["MENU_NEW"], curses.color_pair(COLOR_PLAYER) | curses.A_BOLD)

            status_color = curses.color_pair(COLOR_LORE)
            if "Missing" in self.sound_manager.status_msg or "Fail" in self.sound_manager.status_msg:
                status_color = curses.color_pair(COLOR_ENEMY)

            if os.path.exists(SAVE_FILE):
                self.stdscr.addstr(h//2 + 1, w//2 - 12,
                                t["MENU_CONT"], curses.color_pair(COLOR_MIRROR) | curses.A_BLINK)
            else:
                self.stdscr.addstr(h//2 + 1, w//2 - 12,
                                t["MENU_CONT"], curses.color_pair(COLOR_FOG))

            self.stdscr.addstr(h//2 + 2, w//2 - 12,
                            t["MENU_DEBUG"], curses.color_pair(COLOR_ITEM))
            self.stdscr.addstr(h//2 + 4, w//2 - 12,
                            t["MENU_QUIT"], curses.color_pair(COLOR_WALL))

            # label lingua
            lang_label = "ITALIANO" if self.language == LANG_IT else "ENGLISH"
            self.stdscr.addstr(h//2 + 3, w//2 - 12,
                            f"[L] {t['MENU_LANGUAGE']}: {lang_label}",
                            curses.color_pair(COLOR_TEXT))

            self.stdscr.addstr(h - 3, 2, t["MENU_CONTROLS"], curses.color_pair(COLOR_FOG))
            self.stdscr.addstr(h - 2, 2, t["MENU_CONTROLS_LINE"], curses.color_pair(COLOR_FOG))
            self.stdscr.addstr(h//2 + 5, w//2 - 10,f"AUDIO: [{self.sound_manager.status_msg}]",status_color)
            
        def draw_intro(self):
            h, w = self.height, self.width
            lines = LORE_INTRO_LANG[self.language]
            start_y = max(0, h//2 - len(lines)//2)
            for i, line in enumerate(lines):
                x = max(0, w//2 - len(line)//2)
                color = curses.color_pair(COLOR_TEXT)
                if "PROTOCOL" in line or "PROTOCOLLO" in line or "SUBJECT" in line or "SOGGETTO" in line:
                    color = curses.color_pair(COLOR_LORE) | curses.A_BOLD
                try:
                    self.stdscr.addstr(start_y + i, x, line, color)
                except:
                    pass

                
        def draw_level_intro(self):
            h, w = self.height, self.width
            theme = LEVEL_DATA.get(self.level, LEVEL_DATA[1])
            intro_map = theme.get("intro_text", {})
            intro_text = intro_map.get(self.language, intro_map.get(LANG_EN, ["Unknown Layer"]))
            
            start_y = max(0, h//2 - len(intro_text)//2)
            for i, line in enumerate(intro_text):
                x = max(0, w//2 - len(line)//2)
                color = curses.color_pair(COLOR_TEXT)
                if "LAYER" in line: color = curses.color_pair(COLOR_LORE) | curses.A_BOLD
                try:
                    self.stdscr.addstr(start_y + i, x, line, color)
                except: pass
                
            self.stdscr.addstr(h - 2, (w - 20)//2, "[PRESS ENTER]", curses.color_pair(COLOR_FOG) | curses.A_BLINK)

        def draw_ending(self):
            h, w = self.height, self.width
            lines = self.final_text
            start_y = max(0, h//2 - len(lines)//2)
            for i, line in enumerate(lines):
                x = max(0, w//2 - len(line)//2)
                try:
                    self.stdscr.addstr(start_y + i, x, line, curses.color_pair(self.final_color) | curses.A_BOLD)
                except: pass

        def draw_gameover(self): # Legacy, ora usato per mostrare bad ending se necessario
            self.draw_ending()

        def draw_victory(self): # Legacy
            self.draw_ending()

        def draw_dialogue(self):
            h, w = self.height, self.width

            # Box dimensions
            box_h = 8
            box_y = h - box_h

            # Draw Box Background
            for y in range(box_y, h):
                self.stdscr.addstr(
                    y,
                    0,
                    " " * (w - 1),
                    curses.color_pair(0) | curses.A_REVERSE
                )

            # NPC attivo?
            if self.active_npc:
                data = self.active_npc.dialogue_data

                # --- NOME NPC LOCALIZZATO ---
                title = self.active_npc.name
                if isinstance(data, dict) and "title" in data:
                    title_data = data["title"]
                    if isinstance(title_data, dict):
                        title = title_data.get(self.language, title)

                self.stdscr.addstr(
                    box_y,
                    2,
                    f" {title} ",
                    curses.color_pair(COLOR_NPC) | curses.A_BOLD | curses.A_REVERSE
                )

                # --- CONTENUTO ---
                if self.dialogue_response:
                    # Mostra la risposta già scelta
                    self.stdscr.addstr(
                        box_y + 2,
                        2,
                        f"> {self.dialogue_response}",
                        curses.color_pair(COLOR_TEXT) | curses.A_REVERSE,
                    )
                    t = UI_TEXT[self.language]
                    self.stdscr.addstr(
                        box_y + 6,
                        2,
                        t["DIALOGUE_CLOSE"],
                        curses.color_pair(COLOR_FOG) | curses.A_REVERSE,
                    )
                else:
                    # Intro + opzioni localizzate
                    intro_data = data["intro"]
                    if isinstance(intro_data, dict):
                        intro = intro_data[self.language]
                    else:
                        intro = intro_data  # compatibilità vecchi NPC

                    self.stdscr.addstr(
                        box_y + 1,
                        2,
                        intro,
                        curses.color_pair(COLOR_TEXT) | curses.A_REVERSE,
                    )

                    options = data["options"]
                    for i, opt in enumerate(options):
                        q_data = opt["q"]
                        if isinstance(q_data, dict):
                            q_text = q_data[self.language]
                        else:
                            q_text = q_data

                        self.stdscr.addstr(
                            box_y + 3 + i,
                            2,
                            f"[{i+1}] {q_text}",
                            curses.color_pair(COLOR_LORE) | curses.A_REVERSE,
                        )


        def draw_game(self):
            offset_x = 0
            offset_y = 0

            if self.shake_intensity > 0:
                offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                offset_y = random.randint(-self.shake_intensity // 2, self.shake_intensity // 2)

            def draw_at(y, x, char, color):
                dy, dx = y + offset_y, x + offset_x
                if 0 <= dx < self.width and 0 <= dy < self.height:
                    try:
                        self.stdscr.addch(dy, dx, char, color)
                    except:
                        pass

            # TILE DI MAPPA
            for (x, y), char in self.map_data.items():
                visible = self.is_visible(x, y) or self.debug_reveal
                char_to_draw = char

                if visible and self.sanity < 40 and random.random() < 0.05:
                    char_to_draw = random.choice(HALLUCINATION_CHARS)

                if char == EXIT_CHAR and not visible and (x, y) not in self.memory_map:
                    continue

                if visible:
                    self.memory_map.add((x, y))
                    color = curses.color_pair(COLOR_WALL)
                    if char == EXIT_CHAR:
                        color = curses.color_pair(COLOR_MIRROR) | curses.A_BOLD
                    draw_at(y, x, char_to_draw, color)
                elif (x, y) in self.memory_map:
                    draw_at(y, x, char_to_draw, curses.color_pair(COLOR_FOG))

            # PARTICELLE
            for p in self.particles:
                if self.is_visible(p.x, p.y) or self.debug_reveal:
                    draw_at(p.y, p.x, p.char, curses.color_pair(p.color))

            # SPECCHI
            for (mx, my) in self.mirrors:
                if self.is_visible(mx, my) or self.debug_reveal:
                    draw_at(my, mx, MIRROR_CHAR, curses.color_pair(COLOR_MIRROR) | curses.A_BOLD)
                elif (mx, my) in self.memory_map:
                    draw_at(my, mx, MIRROR_CHAR, curses.color_pair(COLOR_FOG))

            # ITEMS
            for (ix, iy) in self.items:
                if self.is_visible(ix, iy) or self.debug_reveal:
                    draw_at(iy, ix, ITEM_CHAR, curses.color_pair(COLOR_ITEM) | curses.A_BOLD)

            # LORE ITEMS (carattere per livello)
            for (lx, ly) in self.lore_items:
                theme = LEVEL_DATA.get(self.level, LEVEL_DATA[1])
                char = theme['lore_char']
                if self.is_visible(lx, ly) or self.debug_reveal:
                    draw_at(ly, lx, char, curses.color_pair(COLOR_LORE) | curses.A_BOLD)

            # OGGETTI BIZZARRI
            for (bx, by) in self.bizarre_objs:
                if self.is_visible(bx, by) or self.debug_reveal:
                    draw_at(by, bx, BIZARRE_CHAR, curses.color_pair(COLOR_BIZARRE) | curses.A_BOLD)

            # ARMI A TERRA
            for (wx, wy) in self.weapons:
                if self.is_visible(wx, wy) or self.debug_reveal:
                    draw_at(wy, wx, WEAPON_CHAR, curses.color_pair(COLOR_WEAPON) | curses.A_BOLD)

            # NPC
            for npc in self.npcs:
                if self.is_visible(npc.x, npc.y) or self.debug_reveal:
                    draw_at(npc.y, npc.x, npc.char, curses.color_pair(COLOR_NPC) | curses.A_BOLD)

            # NEMICI
            for enemy in self.enemies:
                if self.is_visible(enemy.x, enemy.y) or self.debug_reveal:
                    color = curses.color_pair(COLOR_ENEMY)
                    if enemy.stun_timer > 0:
                        color = curses.color_pair(COLOR_FOG)
                    glitch_char = enemy.get_display_char(self.global_tick)
                    draw_at(enemy.y, enemy.x, glitch_char, color | curses.A_BOLD)

            # GIOCATORE
            render_color = curses.color_pair(COLOR_PLAYER)
            player_char = PLAYER_DIRS.get(self.player_facing, '@')
            player_attr = curses.A_BOLD
            if self.has_weapon:
                render_color = curses.color_pair(COLOR_WEAPON)
                player_attr = curses.A_BOLD | curses.A_REVERSE
            try:
                draw_at(self.player_y, self.player_x, player_char, render_color | player_attr)
            except Exception:
                pass

                        # --- HUD TRADOTTA MA CON I COLORI VECCHI ---

            h, w = self.height, self.width
            t = UI_TEXT[self.language]

            # SANITÀ a sinistra
            sanity_blocks = int(self.sanity / 10)
            sanity_blocks = max(0, min(10, sanity_blocks))
            sanity_color = curses.color_pair(1) if self.sanity > 30 else curses.color_pair(COLOR_ENEMY)
            sanity_label = t["HUD_SANITY"]
            self.stdscr.addstr(
                0,
                0,
                f"{sanity_label}: [{'#' * sanity_blocks:<10}]",
                sanity_color,
            )

            # [UMANO]/[MOSTRO]
            form_label = t["HUD_HUMAN"] if self.player_form == '@' else t["HUD_MONSTER"]
            self.stdscr.addstr(0, 20, f"[{form_label}]", render_color)

            # SCREAM (lasciato com’era, puoi localizzare dopo se vuoi)
            pulse_status = "RDY" if self.sanity > PULSE_COST else "NO EGY"
            self.stdscr.addstr(0, 40, f"SCREAM: {pulse_status}", curses.color_pair(COLOR_LORE))

            # LIVELLO / DEBUG ROOM a destra
            if self.level == 0:
                self.stdscr.addstr(0, 60, "DEBUG ROOM", curses.color_pair(COLOR_WEAPON))
            else:
                layer_label = t["HUD_LAYER"]
                self.stdscr.addstr(
                    0,
                    60,
                    f"{layer_label}: {self.level}/{MAX_LEVELS}",
                    curses.color_pair(COLOR_ITEM),
                )

            # RIGA 1: ARMA + GOD MODE + messaggio
            weapon_str = t["HUD_WEAPON_SPIKE"] if self.has_weapon else t["HUD_WEAPON_NONE"]
            weapon_label = t["HUD_WEAPON"]
            weapon_text = f"{weapon_label}: {weapon_str}"
            weapon_color = curses.color_pair(COLOR_WEAPON) if self.has_weapon else curses.color_pair(COLOR_FOG)
            self.stdscr.addstr(1, 60, weapon_text, weapon_color)

            if self.god_mode:
                self.stdscr.addstr(
                    1,
                    40,
                    "GOD MODE",
                    curses.color_pair(COLOR_GLITCH) | curses.A_BLINK,
                )

            # Messaggio in basso a sinistra (come prima)
            self.stdscr.addstr(
                1,
                0,
                self.message,
                curses.color_pair(COLOR_GLITCH) if "HURT" in self.message or "NEED" in self.message
                else curses.color_pair(COLOR_TEXT),
            )




def main(stdscr):
    # Setup Curses con input non bloccante per animazioni
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True) 
    stdscr.timeout(100)  
    
    # Palette Horror
    curses.init_pair(COLOR_PLAYER, curses.COLOR_WHITE, -1)
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, -1)
    curses.init_pair(COLOR_MIRROR, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_GLITCH, curses.COLOR_MAGENTA, -1)
    curses.init_pair(COLOR_ENEMY, curses.COLOR_RED, -1)
    
    if hasattr(curses, 'COLOR_BLACK'):
        curses.init_pair(COLOR_FOG, curses.COLOR_BLUE, -1)
        curses.init_pair(COLOR_TEXT, curses.COLOR_GREEN, -1)
        curses.init_pair(COLOR_TITLE, curses.COLOR_RED, -1)
        curses.init_pair(COLOR_ITEM, curses.COLOR_YELLOW, -1) 
        curses.init_pair(COLOR_LORE, curses.COLOR_CYAN, -1) 
        curses.init_pair(COLOR_BLOOD, curses.COLOR_RED, -1)
        curses.init_pair(COLOR_WEAPON, curses.COLOR_YELLOW, -1) 
        curses.init_pair(COLOR_NPC, curses.COLOR_GREEN, -1) # NPC Color
        curses.init_pair(COLOR_DIALOGUE, curses.COLOR_WHITE, curses.COLOR_BLUE) # Dialogue Box
        curses.init_pair(COLOR_BIZARRE, curses.COLOR_MAGENTA, -1) # Bizarre Objects
    else:
        curses.init_pair(COLOR_FOG, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_TEXT, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_TITLE, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_ITEM, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_LORE, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_BLOOD, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_WEAPON, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_NPC, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_DIALOGUE, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_BIZARRE, curses.COLOR_WHITE, -1)

    game = Game(stdscr)

    while True:
        game.draw()
        key = stdscr.getch()
        
        if key == -1:
            game.global_tick += 1
            game.update_particles() 
            if game.shake_intensity > 0: game.shake_intensity -= 1
            # AURA CHECK ANCHE DA FERMI (IDLE)
            if game.state == STATE_PLAYING and game.has_weapon:
                enemies_to_remove = []
                for enemy in game.enemies:
                    dist = math.sqrt((enemy.x - game.player_x)**2 + (enemy.y - game.player_y)**2)
                    if dist <= 1.5:
                        enemies_to_remove.append(enemy)
                if enemies_to_remove:
                    for e in enemies_to_remove:
                        game.enemies.remove(e)
                        game.add_particles(e.x, e.y, 15, COLOR_GLITCH)
                    
                    if not game.god_mode:
                        game.has_weapon = False
                    
                    game.message = "SPIKE ACTIVATED. THREATS NEUTRALIZED."
                    game.shake_intensity = 4
            
            # --- JUMPSCARE CHECK (IDLE) ---
            if game.jumpscare_active:
                game.jumpscare_timer -= 1
                if game.jumpscare_timer <= 0:
                    game.jumpscare_active = False
                    stdscr.bkgd(curses.color_pair(0)) # Reset sfondo dopo il jumpscare
            elif game.state == STATE_PLAYING and not game.god_mode:
                if game.jumpscare_cooldown > 0:
                    game.jumpscare_cooldown -= 1
                else:
                    # Base chance increases with level depth
                    # Level 1: 0% base, Level 5: 2% base per tick
                    level_base = (game.level - 1) * 0.005 
                    
                    jumpscare_chance = 0.0 + level_base
                    
                    if game.sanity < 70: jumpscare_chance += 0.005 # Ridotto da 0.01
                    if game.sanity < 40: jumpscare_chance += 0.01  # Ridotto da 0.03
                    if game.sanity < 15: jumpscare_chance += 0.03  # Ridotto da 0.08
                    
                    if random.random() < jumpscare_chance:
                        game.trigger_jumpscare()
            continue
            
        if not game.handle_input(key):
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        log_crash(e) 
        print(f"Errore Fatale: {e}")
        print(f"Log salvato in {CRASH_LOG}")