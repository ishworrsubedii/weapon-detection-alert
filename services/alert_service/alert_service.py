"""
Created By: ishwor subedi
Date: 2023-12-30
"""

import pygame


class AlertService:
    def __init__(self, alert_sound_path):
        self.alert_sound_path = alert_sound_path
        pygame.init()

    def play_alert(self):
        """
        This function help us to play the alert sound
        :return:
        """
        try:
            pygame.mixer.init()
            alert_sound = pygame.mixer.Sound(self.alert_sound_path)
            alert_sound.play()
            pygame.time.wait(int(alert_sound.get_length() * 1000))  # Wait for the sound to finish playing
        except pygame.error as e:
            print(f"Error playing alert sound: {e}")


# if __name__ == '__main__':
#     alert_service = AlertService("resources/alert/alert.mp3")
#     alert_service.play_alert()
