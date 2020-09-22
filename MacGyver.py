#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MacGyver.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import json
from random import sample
import pygame


class Board:
    """objet plateau qui regroupe les coordonnées des différents éléments du
       jeu (murs, depart, arrivée, guarde, equipements...)"""
    def __init__(self, x_tile, y_tile, tile_size):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.tile_size = tile_size
        self.walls = []
        self.corridors = []

    @property
    def width(self):
        """largeur plateau en px"""
        return self.x_tile * self.tile_size

    @property
    def height(self):
        """hauteur plateau en px"""
        return self.y_tile * self.tile_size

    def read_map(self, map_path):
        """lit un .json : 'w'=wall, 's'=start, 'e'=end, 'g'=guard, ' '=empty"""
        with open(map_path) as file:
            data = json.load(file)
        # iter sur 2 boucle pour avoir ligne et colonnes soit
        # un tuple de coordonnées une fois multiplier par la largeur d'une case
        for y_index,line in enumerate(data):
            for x_index,char in enumerate(line):
                coord = ((x_index * self.tile_size,y_index * self.tile_size))
                if char == 'w':
                    self.walls.append(coord)
                else:
                    self.corridors.append(coord)
                    if char == 's':
                        setattr(self, 'start', coord)
                    elif char == 'e':
                        setattr(self, 'end', coord)
                    elif char == 'g':
                        setattr(self, 'guard', coord)

    def set_components(self):
        """recupère 3 coordonnées aleatoire parmis les cases libres"""
        setattr(self, 'components', sample(list(self.available()), 3))


    def available(self):
        """renvoi un emplacement qui peu recevoir un objet"""
        for coord in self.corridors:
            if coord != self.start and coord != self.end and coord != self.guard:
                yield coord

class Macgyver:
    """objet MacGyver sa position, ses possesions, il se deplace..."""
    def __init__(self, start):
        self.coord = start
        self.backpack = 0

    def move(self, vector_x, vector_y, board):
        """déplace MacGyver vers la prochaine case"""
        x, y = self.coord
        next_step = (x + vector_x, y + vector_y)
        if next_step in board.corridors:
            if next_step in board.components:
                board.components.remove(next_step)
                self.backpack += 1
                self.coord = next_step
            elif next_step == board.guard:
                if self.backpack < 3:
                    return 'you lose'
                else:
                    self.coord = next_step
            elif next_step == board.end:
                self.coord = next_step
                return 'you win'
            else:
                self.coord = next_step
            return 'running'
        else:
            return 'running'

def display_txt(txt, size, color, surface, x = 'center', y = 'center'):
    """Affiche le texte au milieu de la surface avec pygame
       (c'est juste pour me simplifier la vie!)"""
    txt = str(txt)
    font = pygame.font.Font('resources/stocky.ttf', size)
    img_txt = font.render(txt, True, color)
    if x == 'center':
        x = int((surface.get_width() - font.size(txt)[0])/2)
    if y == 'center':
        y = int((surface.get_height() - font.size(txt)[1])/2)
    return surface.blit(img_txt, (x, y))

class App:
    """Le jeu dans pygame"""
    def __init__(self):
        # initialise pygame
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        """fonction principale"""
        # initialise le plateau(15 case large, 15 case haut,
        # case de 32px)
        board = Board(15, 15, 32)
        # place les murs, les couloirs, le depart, l'arrivée, le garde... sur le plateau
        board.read_map('resources/structure.json')
        # place les objets sur le plateau
        board.set_components()
        # initialise l'instance de Mac(emplacement de départ)
        macgyver = Macgyver(board.start)
        # la fenetre pygame
        screen = pygame.display.set_mode((board.width, board.height))
        # charge les images depuis le repertoire resources
        wall_image = pygame.image.load('resources/wall.png')
        floor_image = pygame.image.load('resources/floor.png')
        guard_image = pygame.image.load('resources/guard.png')
        component_image = pygame.image.load('resources/dart.png')
        mac_image = pygame.image.load('resources/mac.png')
        # etat du jeu 'you lose'=perdu, 'you win'=gagné, 'running'=aucun des 2
        game_status = 'running'

        while True:
            # boucle d'ecoute d'evenements pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if game_status == 'running':
                        if event.key == pygame.K_UP:
                            game_status = macgyver.move(0, -32, board)
                        elif event.key == pygame.K_LEFT:
                            game_status = macgyver.move(-32, 0, board)
                        elif event.key == pygame.K_DOWN:
                            game_status = macgyver.move(0, +32, board)
                        elif event.key == pygame.K_RIGHT:
                            game_status = macgyver.move(+32, 0, board)
                    else:
                        if event.key == pygame.K_RETURN:
                            return self.main()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
            # affiche les images et rafraichi...
            for coord in board.walls:
                screen.blit(wall_image, coord)
            for coord in board.corridors:
                screen.blit(floor_image, coord)
            for coord in board.components:
                screen.blit(component_image, coord)
            screen.blit(guard_image, board.guard)
            screen.blit(mac_image, macgyver.coord)
            # l'etat du jeu a changé? :
            if game_status != 'running':
                display_txt(game_status, 40, (180, 60, 20), screen, 'center', 100)
                display_txt('Press RETURN to Replay', 14, (25, 25, 25), screen, 'center', 170)
                display_txt('Press ESCAPE to Quit', 14, (25, 25, 25), screen, 'center', 200)

            pygame.display.update()

        return 1

if __name__ == '__main__':
    App().main()
