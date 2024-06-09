import random


pieceScore = {'K': 0, 'Q': 10, 'R': 5, 'N': 3, 'B': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


'''Picks and returns the random move.'''


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''Helper method to make first recursive call'''


def findBestMove(game_state, validMoves):
    global NextMove, count
    NextMove = None
    count = 0
    findMoveNegaMaxAlphabeta(game_state, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.whiteToMove else -1)
    return NextMove


def findMoveMinMax(game_state, validMoves, depth, whiteToMove):
    global nextMove, count
    count += 1
    if depth == 0:
        return scoreMaterial(game_state.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return minScore


def findMoveNegaMax(game_state, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return scoreMaterial(game_state.board)

    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMax(game_state, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()

    return maxScore


def findMoveNegaMaxAlphabeta(game_state, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, count
    count += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(game_state)

    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphabeta(game_state, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore


'''A positive score is good for white, negative is goor for black'''


def scoreBoard(game_state):
    if game_state.checkmate:
        if game_state.whiteToMove:
            return -CHECKMATE  # black wins
        return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score


'''Scores the board based on material'''


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score
