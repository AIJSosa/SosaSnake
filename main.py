# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Sosa",  # TODO: Your Battlesnake Username
        "color": "#1bf72a",  # TODO: Choose color
        "head": "pixel",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def getPotentialMoves(x, y):
    return {
        "up": {"x": x, "y" : y + 1},
        "down": {"x": x, "y" : y - 1},
        "left": {"x": x - 1, "y" : y},
        "right": {"x": x + 1, "y" : y}
    }

def is_safe(x, y, board_width, board_height, snakes, mySnake):
    mySnakeLength = mySnake["length"]
    if x < 0 or x >= board_width or y < 0 or y >= board_height:
        return False
    for enemy in snakes:
        for bodyNode in enemy['body']:
            if x == bodyNode["x"] and y == bodyNode["y"]:
                return False
        #prevent continuing if this is my snake
        if enemy["id"] == mySnake["id"]:
            continue
        if mySnakeLength <= enemy["length"]:
            enemyMoves = getPotentialMoves(enemy["body"][0]["x"], enemy["body"][0]["y"])
            for _,enemyMove in enemyMoves.items():
                if enemyMove["x"] == x and enemyMove["y"] == y:
                    return False
    return True

def outOfBounds(x, y, board_width, board_height):
    return (x < 0 or x >= board_width or y < 0 or y >= board_height)

def betterIsSafe(x, y, boardSafety):
    if (boardSafety[x][y] == 0):
        return False;
    if not onBoard(x, y, boardSafety):
        return False;
    surroundingSquares = getPotentialMoves(x, y);
    badSurrounded = 0;
    for _, surroundingSquare in surroundingSquares.items():
        if not onBoard(surroundingSquare["x"], surroundingSquare["y"], boardSafety):
            badSurrounded += 1
        elif boardSafety[surroundingSquare["x"]][surroundingSquare["y"]] == 0:
            badSurrounded += 1
    return badSurrounded < 3

def getOpeningShout():
    return random.choice(
        [
            "For Narnia!!!!!",
            "For Sparta!!!",
            "For the Gods!!!",
            "For Valhalla!!!!",
            "To the last breath!!!",
            "In Honor and Glory!!!",
            "For the Kingdom!",
            "For the Empire!",
            "For Honor!",
            "For the Republic!",
            "Til Death do us Part!",
            "To Victory or Death!",
            "For the future of our children!",
            "For King and Country!",
            "Might makes right!",
            "101010101010011010101011010!"
        ]
    )

def updateBoardTile(x, y, boardSafety):
    if not onBoard(x, y, boardSafety) or (boardSafety[x][y] <= 0):
        return boardSafety;
    if not betterIsSafe(x, y, boardSafety):
        boardSafety[x][y] = 0;
        potentialMoves = getPotentialMoves(x, y)
        for _, move in potentialMoves.items():
            boardSafety = updateBoardTile(move["x"], move["y"], boardSafety)
    return boardSafety
        

def updateBoardSafety(boardSafety):
    #For each key in 2D boardSafety, if surrounded on 3 sides by non-safe squares, mark 0
    for x in boardSafety:
        for y in boardSafety[x]:
            boardSafety = updateBoardTile(x, y, boardSafety)
    return boardSafety;

def onBoard(x, y, boardSafety):
    if not x in boardSafety:
        return False;
    if not y in boardSafety[x]:
        return False;
    return True 

def lastDitch(game_state):
    mySnake = game_state["you"]
    myBody = mySnake["body"]
    my_head = myBody[0]  # Coordinates of your head

    headX = my_head["x"];
    headY = my_head["y"];
    potentialMoves = getPotentialMoves(headX, headY);

    xLimit = game_state['board']['width']
    yLimit = game_state['board']['height']

    boardSafety = {}
    for boardX in range(xLimit):
        if boardX not in boardSafety:
            boardSafety[boardX] = {}
        for boardY in range(yLimit):
            boardSafety[boardX][boardY] = 1;

    for snake in game_state['board']['snakes']:
        for bodyNode in snake['body']:
            boardSafety[bodyNode["x"]][bodyNode["y"]] = 0
        if snake["id"] == mySnake["id"]:
            boardSafety[snake['body'][0]['x']][snake['body'][0]['y']] = -1
            continue
        if mySnake["length"] < snake["length"]:
            enemyMoves = getPotentialMoves(snake["body"][0]["x"], snake["body"][0]["y"])
            for _,enemyMove in enemyMoves.items():
                if onBoard(enemyMove["x"], enemyMove["y"], boardSafety):
                    boardSafety[enemyMove["x"]][enemyMove["y"]] = 0

    hazards = [];
    for x in boardSafety:
        for y in boardSafety[x]:
            if boardSafety[x][y] == 0:
                hazards.append({"x": x, "y": y})

    moveScores = {};
    for move, potentialMove in potentialMoves.items():
        moveX = potentialMove["x"]
        moveY = potentialMove["y"]

        if (not onBoard(moveX, moveY, boardSafety)) or (boardSafety[moveX][moveY] == 0):
            continue;
        # get manhattan distance to hazard
        hazardDistanceSum = 0;
        for hazard in hazards:
            hazardDistanceSum += abs(hazard["x"] - moveX) + abs(hazard["y"] - moveY)
        hazardScore = hazardDistanceSum / len(hazards)
        moveScores[move] = hazardScore;

    safe_moves = []
    for move in moveScores:
        safe_moves.append(move);

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected at all...")
        return {"move": "up", "shout": "C'est la vie"}

    return {"move": random.choice(safe_moves)};

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    mySnake = game_state["you"]
    myBody = mySnake["body"]
    myHealth = mySnake["health"]

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = myBody[0]  # Coordinates of your head

    headX = my_head["x"];
    headY = my_head["y"];

    potentialMoves = getPotentialMoves(headX, headY);

    xLimit = game_state['board']['width']
    yLimit = game_state['board']['height']

    boardSafety = {}
    for boardX in range(xLimit):
        if boardX not in boardSafety:
            boardSafety[boardX] = {}
        for boardY in range(yLimit):
            boardSafety[boardX][boardY] = 1;

    for snake in game_state['board']['snakes']:
        for bodyNode in snake['body']:
            boardSafety[bodyNode["x"]][bodyNode["y"]] = 0
        if snake["id"] == mySnake["id"]:
            boardSafety[snake['body'][0]['x']][snake['body'][0]['y']] = -1
            continue
        if mySnake["length"] < snake["length"]:
            enemyMoves = getPotentialMoves(snake["body"][0]["x"], snake["body"][0]["y"])
            for _,enemyMove in enemyMoves.items():
                if onBoard(enemyMove["x"], enemyMove["y"], boardSafety):
                    boardSafety[enemyMove["x"]][enemyMove["y"]] = 0

    boardSafety = updateBoardSafety(boardSafety)

    for hazard in game_state['board']['hazards']:
        boardSafety[hazard["x"]][hazard["y"]] = 0

    for food in game_state['board']['food']:
        if boardSafety[food["x"]][food["y"]] == 1:
            boardSafety[food["x"]][food["y"]] = 2;

    hazards = [];
    food = [];
    for x in boardSafety:
        for y in boardSafety[x]:
            if boardSafety[x][y] < 1:
                hazards.append({"x": x, "y": y})
            if boardSafety[x][y] > 1:
                food.append({"x": x, "y": y})

    # Now add board edges to hazards
    for x in range(xLimit):
        hazards.append({"x": x, "y": -1})
        hazards.append({"x": x, "y": yLimit})
    for y in range(yLimit):
        hazards.append({"x": -1, "y": y})
        hazards.append({"x": xLimit, "y": y})
            


    moveScores = {};
    moveFoodDistances = {};
    for move, potentialMove in potentialMoves.items():
        moveX = potentialMove["x"]
        moveY = potentialMove["y"]

        if (not onBoard(moveX, moveY, boardSafety)) or (boardSafety[moveX][moveY] == 0):
            continue;
        # get manhattan distance to hazard
        hazardDistanceSum = 0;
        for hazard in hazards:
            hazardDistanceSum += abs(hazard["x"] - moveX) + abs(hazard["y"] - moveY)
        hazardScore = hazardDistanceSum / len(hazards)
        moveScores[move] = hazardScore;

        # get closest food
        closesFoodDistance = 1000;
        for foodNode in food:
            foodDistance = abs(foodNode["x"] - moveX) + abs(foodNode["y"] - moveY)
            if foodDistance < closesFoodDistance:
                closesFoodDistance = foodDistance
                moveFoodDistances[move] = foodDistance

    if myHealth < (xLimit + yLimit + 8):
        # go toward the nearest food
        lowestFoodDistance = 1000;
        lowestFoodMove = '';
        for move, foodDistance in moveFoodDistances.items():
            if foodDistance < lowestFoodDistance:
                lowestFoodDistance = foodDistance
                lowestFoodMove = move
        print("Prioritizing food")
        return {"move": lowestFoodMove}

    #print move scores and move distances
    #print(moveScores)
    #print(moveFoodDistances)

    # Are there any safe moves left?
    safe_moves = []
    for move in moveScores:
        safe_moves.append(move);

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Time for last ditch")
        return lastDitch(game_state)

    if len(safe_moves) == 1:
        print(f"MOVE {game_state['turn']}: Only one safe move detected! Moving {safe_moves[0]}")
        return {"move": safe_moves[0], "shout": "If I must"}
    
    #Now get the two moves with the best scores
    bestTwoMoves = {};
    bestMove = '';
    secondbestMove = '';
    for move,score in moveScores.items():
        if len(bestTwoMoves) < 2:
            bestTwoMoves[move] = score
            if bestMove == '':
                bestMove = move
            else:
                if score > bestTwoMoves[bestMove]:
                    secondbestMove = bestMove
                    bestMove = move
                else: 
                    secondbestMove = move;
        else:
            if score > bestTwoMoves[bestMove]:
                del bestTwoMoves[secondbestMove]
                secondbestMove = bestMove
                bestMove = move
                bestTwoMoves[move] = score
            elif score > bestTwoMoves[secondbestMove]:
                del bestTwoMoves[secondbestMove]
                secondbestMove = move;
                bestTwoMoves[move] = score;

    #print(bestTwoMoves);
                
    if secondbestMove == '':
        secondbestMove = bestMove

    best_moves = [];
    for move in bestTwoMoves:
        best_moves.append(move);

    next_move = '';
    if (best_moves[0] not in moveFoodDistances) or (best_moves[1] not in moveFoodDistances):
        return {"move": bestMove}
    
    if moveFoodDistances[best_moves[0]] < moveFoodDistances[best_moves[1]]:
        next_move = best_moves[1];
    else:
        next_move = best_moves[0];
    
    response = {"move": next_move}


    if (game_state["turn"] == 0):
        response["shout"] = getOpeningShout();

    print(f"MOVE {game_state['turn']}: {next_move}")
    if ("shout" in response):
        print(response["shout"])
    return response


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
