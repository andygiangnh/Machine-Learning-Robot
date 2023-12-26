import pygame, math, numpy

# constant based on lidar resolution
LIDAR_RESOLUTION = 360
# Selected positions in a frame (result of the Sklearn SelectKBest function)
POSITIONS_PER_FRAME = [141, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 203, 204, 205, 206, 207]


def get_data_from_arduino(line):
    # [:-3] get rid of end of line sign and additional comma separator that is sent from arduino
    # data = line[:-3]
    data = line[:]
    print(data)
    d_list = data.split(",")
    return d_list


"""
Return the (x,y) position for the point when circle radius of 1
"""


def generate_baseline_positions():
    lines = []
    for x in range(LIDAR_RESOLUTION):
        lines.append([math.cos(x / 180 * math.pi),
                      math.sin(x / 180 * math.pi)])
    return lines


def run():
    pygame.init()

    line_positions = generate_baseline_positions()
    for line_position in line_positions:
        print(line_position)

    # Set up the drawing window
    screen = pygame.display.set_mode([800, 800])
    sys_font = pygame.font.get_default_font()
    font1 = pygame.font.SysFont(sys_font, 72)

    file1 = open('../data/out2.txt', 'r')
    lines = file1.readlines()
    running = True
    counter = 0
    paused = False
    inspect_mode = False
    while counter < len(lines):
        line = lines[counter]
        if inspect_mode:
            paused = True
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    print('PAUSE STATUS: {}'.format(paused))
                elif event.key == pygame.K_i:
                    """
                    Press 'i' keyboard will turn on inspection mode,
                    which run frame by frame
                    """
                    inspect_mode = not inspect_mode
                    print('INSPECT MODE: {}'.format(inspect_mode))
                elif event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.QUIT:
                # Press 'X' button on window will close the program
                running = False

        if not running:
            break
        elif paused:
            continue

        distances = get_data_from_arduino(line)
        # print(len(distances))
        if len(distances) == LIDAR_RESOLUTION:
            # Fill the background with white
            screen.fill((250, 250, 250))

            for x in range(LIDAR_RESOLUTION):
                a = float(distances[x]) / 2
                if x in POSITIONS_PER_FRAME:
                    # Draw the important point with RED color
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (line_positions[x][0] * a + 400, line_positions[x][1] * a + 400),
                                       3)
                else:
                    # Draw the ordinary point with BLACK color
                    pygame.draw.circle(screen, (0, 0, 0),
                                       (line_positions[x][0] * a + 400, line_positions[x][1] * a + 400),
                                       2)
                    # print('Position x:{}, y:{}'
                    #       .format(line_positions[x][0] * a + 400, line_positions[x][1] * a + 400))

            pygame.draw.circle(screen, (252, 132, 3), (400, 400), 12)
            # Flip the display
            pygame.display.flip()
            pygame.time.wait(50)
            counter += 1

    pygame.quit()


if __name__ == '__main__':
    run()
