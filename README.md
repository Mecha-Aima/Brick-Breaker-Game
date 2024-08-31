# Brick Breaker Game

## Overview

This project implements a classic Brick Breaker game using Python and Pygame. The player controls a striker pad to bounce a ball and break bricks across multiple levels. The goal is to clear all bricks while keeping the ball in play.

## Features

- Object-Oriented Design implemented in Python with Pygame
- Multiple levels with increasing difficulty
- High score tracking and persistence
- Lives system with reset per level

## Key Components

### Objects
- Ball: Bounces around the screen, breaking bricks
- Striker: Player-controlled pad for bouncing the ball
- Brick: Destructible objects that the player aims to clear
- Game: Manages overall game state and flow

### Variables
- `score`: Current player score
- `lives`: Number of attempts remaining (3 per level)
- `level`: Current game level
- `high_score`: Highest score achieved

## Game Flow

1. Start Screen
2. Level Initialization
3. Gameplay Loop
4. Level Completion / Game Over
5. Score Display and High Score Update

## Core Mechanics

- Ball physics: Bounces off walls, striker, and bricks
- Striker movement: Horizontal motion based on player input
- Brick destruction: Disappear when hit, increasing the score
- Lives: Lost when ball falls off-screen; game ends at zero lives
- Levels: Complete when all bricks are destroyed; difficulty increases

## Technical Considerations

- Collision detection
- Physics simulation
- User input handling
- Game state management
- File I/O for high score persistence

