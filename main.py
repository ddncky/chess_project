"""
Main driver file. It will be responsible for handling user input and displaying current GameState object
"""
import pygame as p
import engine
import ai
import buttons as b
from random import randint


BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
ALLCOLORS = list(p.color.THECOLORS)
random_color = ALLCOLORS[randint(1, len(ALLCOLORS))]
random_color2 = ALLCOLORS[randint(1, len(ALLCOLORS) - 1)]
random_color3 = ALLCOLORS[randint(1, len(ALLCOLORS))]
random_color4 = ALLCOLORS[randint(1, len(ALLCOLORS))]

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(folderName + piece + '.png'), (SQ_SIZE, SQ_SIZE))


"""
The main driver for our program. This will handle user input and updating the graphics
"""


def main():
    p.init()
    start_screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    p.display.set_caption('Main Menu')


    global folderName
    folderName = 'pics/'
    GamePaused = False
    showStartScreen = True
    showStartButton = True
    isUndoMove = True
    isResetGame = True
    global isHighlightMove
    isHighlightMove = True
    global isCustom
    isCustom = False
    isMusicOn = True
    startGame = False
    menu_state = 'main'


    # load buttons
    start_img = p.image.load('buttons/start.png').convert_alpha()
    stop_img = p.image.load('buttons/stop.png').convert_alpha()
    quit_img = p.image.load('buttons/quit.png').convert_alpha()
    resume_img = p.image.load('buttons/resume.png').convert_alpha()
    options_img = p.image.load('buttons/options.png').convert_alpha()
    easy_img = p.image.load('buttons/easy.png').convert_alpha()
    hard_img = p.image.load('buttons/hard.png').convert_alpha()
    back_img = p.image.load('buttons/back.png').convert_alpha()
    help_img = p.image.load('buttons/help.png').convert_alpha()
    blank_img = p.image.load('buttons/blank.png').convert_alpha()
    tutorial_img = p.image.load('buttons/tutorial.png').convert_alpha()
    custom_img = p.image.load('buttons/custom.png').convert_alpha()
    reset_img = p.image.load('buttons/reset.png').convert_alpha()
    random_img = p.image.load('buttons/random.png').convert_alpha()
    victory_img = p.image.load('buttons/victory.png').convert_alpha()
    gameover_img = p.image.load('buttons/gameover.png').convert_alpha()
    music_img = p.image.load('buttons/music.png').convert_alpha()
    music_on_img = p.image.load('buttons/music_on.png').convert_alpha()
    music_off_img = p.image.load('buttons/music_off.png').convert_alpha()
    mainmenu_img = p.image.load('buttons/mainmenu.jpg')
    optionmenu_img = p.image.load('buttons/mainmenu3.jpg')
    custommenu_img = p.image.load('buttons/mainmenu2.jpg')
    musicmenu_img = p.image.load('buttons/mainmenu4.jpeg')



    # create buttons instances
    start_button = b.Buton(235, 50, start_img, 0.5)
    resume_button = b.Buton(280, 85, resume_img, 0.5)
    options_button = b.Buton(289, 180, options_img, 0.5)
    quit_button = b.Buton(269, 275, quit_img, 0.5)
    easy_button = b.Buton(60, 30, easy_img, 0.5)
    hard_button = b.Buton(60, 120, hard_img, 0.6)
    help_button = b.Buton(36, 210, help_img, 0.6)
    music_button = b.Buton(410, -15, music_img, 0.6)
    custom_button = b.Buton(440, 120, custom_img, 0.58)
    blank_button = b.Buton(400, 190, blank_img, 0.62)
    reset_button = b.Buton(255, 310, reset_img, 0.5)
    random_button = b.Buton(158, 200, random_img, 0.7)
    music_on_button = b.Buton(158, 200, music_on_img, 0.7)
    music_off_button = b.Buton(400, 187, music_off_img, 0.75)
    back_button = b.Buton(235, 410, back_img, 0.5)


    p.mixer.music.load('buttons/sound_button.mp3')
    move_sound = p.mixer.Sound('buttons/movesound.wav')



    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()  # Создаем часы;
    screen.fill(p.Color('gray'))  # Это не обязательно, но закрасим пока экран любым цветом.
    moveLogFont = p.font.SysFont('Arial', 14, True, False)

    game_state = engine.GameState()  # Создаем ЭК GameState, чтобы получить доступ к доске.
    validMoves = game_state.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    loadImages()  # Делаем это один раз!

    running = True
    sqSelected = ()  # no square selected, keep track of the last click of the user(tuple: row, column)
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)]
    animate = False  # flag variable for when we should animate a move
    gameOver = False
    playerOne = True  # if a human is playing white, this will be true. if an AI is playing, then false
    playerTwo = True  # same for black



    while running:
        # Отрисовка и работа кнопок при входе в игру и до нажатия паузы.
        if showStartScreen:
            if menu_state == 'main':
                start_screen.blit(mainmenu_img, (0, 0))
                # if menu_state == 'main':
                if showStartButton:
                    if start_button.drawButtons(start_screen):
                        if isMusicOn:
                            p.mixer.music.play(1, 0.2)
                        startGame = True
                        showStartButton = False
                    if options_button.drawButtons(start_screen):
                        if isMusicOn:
                            p.mixer.music.play(1, 0.2)
                        menu_state = 'options'
                    if quit_button.drawButtons(start_screen):
                        if isMusicOn:
                            p.mixer.music.play(1, 0.2)
                        running = False

            elif menu_state == 'options':
                start_screen.blit(optionmenu_img, (0, 0))

                # draw options buttons
                if hard_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isUndoMove = False
                    isHighlightMove = False
                    isResetGame = False
                if easy_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isUndoMove = True
                    isHighlightMove = True
                    isResetGame = True
                if back_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    menu_state = 'main'
                if help_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    playerTwo = False
                if music_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    menu_state = 'music'
                if blank_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    attempt = input('Введи тайное слово...у тебя 1 попытка: ')
                    if attempt == 'aezakmi':
                        folderName = 'pics/'  # в гит решил не добавлять;
                        loadImages()
                if custom_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    menu_state = 'custom'
                if reset_button.drawButtons(start_screen):  # reset everything
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isUndoMove = True
                    isHighlightMove = True
                    playerOne, playerTwo = True, True
                    if folderName == 'pieces/':
                        folderName = 'pics/'
                        loadImages()
                    isCustom = False

            elif menu_state == 'custom':
                start_screen.blit(custommenu_img, (0, 0))
                if random_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isCustom = True
                if back_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    menu_state = 'options'

            elif menu_state == 'music':
                start_screen.blit(musicmenu_img, (0, 0))
                if music_on_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isMusicOn = True

                if music_off_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    isMusicOn = False

                if back_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    menu_state = 'options'

        # Отвечает за запуск игры после нажатия клавиши старт (без этого был баг)
        if startGame:
            drawGameState(screen, game_state, validMoves, sqSelected, moveLogFont)
            showStartScreen = False

        # Отвечает за меню игры после того, как был нажат пробел во время игры.
        if GamePaused:
            startGame = False
            showStartScreen = True
            #     # check menu state
            if menu_state == 'main':
                if resume_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1)
                    GamePaused = False
                    startGame = True
                    showStartScreen = False
                if options_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1)
                    menu_state = 'options'
                if quit_button.drawButtons(start_screen):
                    if isMusicOn:
                        p.mixer.music.play(1)
                    running = False

            elif menu_state == 'options':
                # draw options buttons
                if hard_button.drawButtons(start_screen):
                    isUndoMove = False
                    isHighlightMove = False
                    isResetGame = False
                if easy_button.drawButtons(start_screen):
                    isUndoMove = True
                    isHighlightMove = True
                    isResetGame = True
                if back_button.drawButtons(start_screen):
                    menu_state = 'main'
                if help_button.drawButtons(start_screen):
                    playerTwo = False
                if music_button.drawButtons(start_screen):
                    menu_state = 'music'
                if blank_button.drawButtons(start_screen):
                    attempt = input('Введи тайное слово...у тебя 1 попытка: ')
                    if attempt == 'aezakmi':
                        folderName = 'pieces/'
                        loadImages()
                if custom_button.drawButtons(start_screen):
                    isCustom = True

                if reset_button.drawButtons(start_screen):  # reset everything
                    isUndoMove = True
                    isHighlightMove = True
                    playerOne, playerTwo = True, True
                    if folderName == 'pieces/':
                        folderName = 'pics/'
                        loadImages()
                    isCustom = False

        p.display.update()

        isHumanTurn = (game_state.whiteToMove and playerOne) or (not game_state.whiteToMove and playerTwo)
        for e in p.event.get():  # С помощью данного цикла мы сможем 'тушить свет'
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:  # Здесь в будeщем можно попробовать перетаскивать фигуры!
                if not gameOver and isHumanTurn:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (
                    row, col) or col >= 8:  # the user clicked the same square twice or user clicked the mouse log
                        sqSelected = ()  # deselect
                        playerClicks = []  # clear this also
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks

                    if len(playerClicks) == 2:  # after 2nd click
                        move = engine.Move(playerClicks[0], playerClicks[1], game_state.board)

                        print(move.getChessNotation())

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                game_state.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset user clicks
                                playerClicks = []
                                if isMusicOn:
                                    move_sound.play()

                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    if isUndoMove:
                        game_state.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                if e.key == p.K_r:  # reset the board when r is pressed
                    if isResetGame:
                        game_state = engine.GameState()
                        validMoves = game_state.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                if e.key == p.K_SPACE:
                    if isMusicOn:
                        p.mixer.music.play(1, 0.2)
                    if showStartButton:
                        continue
                    else:
                        GamePaused = True
                if e.key == p.K_RETURN:
                    pass
                    # startGame = True

        # AI move finder
        if not gameOver and not isHumanTurn:
            AIMove = ai.findBestMove(game_state, validMoves)
            if AIMove is None:
                AIMove = ai.findRandomMove(validMoves)
            game_state.makeMove(AIMove)
            if isMusicOn:
                move_sound.play()
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(game_state.movelog[-1], screen, game_state.board, clock)
            validMoves = game_state.getValidMoves()
            moveMade = False
            animate = False

        if game_state.checkmate:
            gameOver = True
            if game_state.whiteToMove:
                screen.blit(gameover_img, (22, 120))
            else:
                screen.blit(victory_img, (22, 120))

            p.display.flip()

        elif game_state.stalemate:
            text = 'Stalemate -_-'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)  # Устанавливаем частоту кадров, чтобы не использовать лишнюю мощность.
        p.display.flip()


"""Responsible for all te graphics within a current game state"""


def drawGameState(screen, game_state, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # Draw squares on the board
    if isHighlightMove:
        highlightSquares(screen, game_state, validMoves, sqSelected)
    drawPieces(screen, game_state.board)  # Draw pieces on top of the squares
    drawMoveLog(screen, game_state, moveLogFont)


"""Draws the squares on the board"""


def drawBoard(screen):
    global colors
    colors = [p.Color('burlywood4' if not isCustom else random_color),
              p.Color('wheat' if not isCustom else random_color2)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""Draws the pieces on the board using the current GameState.board"""


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''Draws the move log'''


def drawMoveLog(screen, game_state, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH,
                         MOVE_LOG_PANEL_HEIGHT)  # можно сделать меню игры потом (15 урок)
    p.draw.rect(screen, p.Color('gray'), moveLogRect)
    moveLog = game_state.movelog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + '. ' + str(moveLog[i]) + ' '
        if i + 1 < len(moveLog):  # make sure black made a move
            moveString += str(moveLog[i + 1]) + ' '
        moveTexts.append(moveString)
    movesPerRow = 2
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ''
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color('Black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


'''Highlight square selected and moves for piece selected'''


def highlightSquares(screen, game_state, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if game_state.board[row][col][0] == ('w' if game_state.whiteToMove else 'b'):  # sqSelected is a piece
            # highlight selected square                                                # that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transperancy value -> 0 transparent, 255 opaque
            s.fill(p.Color('purple4' if not isCustom else random_color3))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('darkslategray1' if not isCustom else random_color4))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


'''Animating a move'''


def animateMove(move, screen, board, clock):
    global colors
    coords = []  # list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 7  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moves to its endinig square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enpassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    font = p.font.SysFont('arial', 32, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Gray'))
    screen.blit(textObject, textLocation.move(2, 2))


def drawMainScreenText(start_screen, text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    start_screen.blit(img, (x, y))


if __name__ == '__main__':
    main()
