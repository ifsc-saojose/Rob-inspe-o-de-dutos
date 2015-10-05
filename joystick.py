import pygame

class joystick():
    pygame.init()
    _j = None
    _key_pressed = [0.0, 0.0, 0.0, 0.0, 0, 0, 0]

    def get_axes(self):
        count = 0
        pygame.event.pump()
        for i in range(0, self._j.get_numaxes()):
                self._key_pressed[count] = self._j.get_axis(i)
                count += 1

    def get_button(self):
        count = 4
        buttons = [4, 5, 9]
        pygame.event.pump()
        for i in range(0, 3):
                self._key_pressed[count] = self._j.get_button(buttons[i])
                count += 1

    def reading(self):
        try:
            self._j = pygame.joystick.Joystick(0)
            self._j.init()
        except:
            try:
                self.j.quit()
            except:
                pass

        self.get_axes()
        self.get_button()
        return self._key_pressed

