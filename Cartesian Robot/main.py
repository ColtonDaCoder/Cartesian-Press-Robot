from threading import Thread
import ui
import robot
class main:
    def __init__(self):
        user_interface = Thread(target=main.start_ui, daemon=False)
        robot_control = Thread(target=main.start_robot, daemon=True)

        robot_control.start()
        user_interface.start()
    def start_ui():
        ui.main_win().mainloop()
    def start_robot():
        robot.robot()
if __name__ == '__main__':
    m = main()