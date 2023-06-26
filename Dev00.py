from raylibpy.raylib import init_window, set_target_fps, window_should_close, begin_drawing, clear_background, draw_text, end_drawing, close_window, RAYWHITE, LIGHTGRAY

def main():

    init_window(800, 450, "raylib [core] example - basic window")

    set_target_fps(60)

    while not window_should_close():

        begin_drawing()
        clear_background(RAYWHITE)
        draw_text("Congrats! You created your first window!", 190, 200, 20, LIGHTGRAY)
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()