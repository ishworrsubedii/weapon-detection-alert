"""
Created By: ishwor subedi
Date: 2023-12-30
"""
from services.alert_service.alert_service import AlertService

if __name__ == '__main__':
    alert_service = AlertService("resources/alert/alert.mp3")
    alert_service.play_alert()
