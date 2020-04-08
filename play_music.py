import os

def music_list(index):
    file = os.listdir('./music/')
    if index >= len(file):
        index = 0
    return file[index]

