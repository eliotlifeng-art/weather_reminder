import platform

if platform.system() == "Android":
    from plyer import notification as plyer_notification

    def send_notification(title, message):
        try:
            plyer_notification.notify(title=title, message=message, timeout=10)
        except Exception:
            pass

else:
    def send_notification(title, message):
        print(f"[NOTIFICATION] {title}: {message}")
        try:
            from plyer import notification as plyer_notification
            plyer_notification.notify(title=title, message=message, timeout=10)
        except Exception:
            pass
