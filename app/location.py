import platform

if platform.system() == "Android":
    from plyer import gps

    class LocationProvider:
        def __init__(self):
            self.lat = None
            self.lon = None
            self._callback = None

        def start(self, callback):
            self._callback = callback
            try:
                gps.configure(on_location=self._on_location, on_status=self._on_status)
                gps.start(minTime=1000, minDistance=0)
            except NotImplementedError:
                pass

        def stop(self):
            try:
                gps.stop()
            except NotImplementedError:
                pass

        def _on_location(self, **kwargs):
            self.lat = kwargs.get("lat")
            self.lon = kwargs.get("lon")
            if self._callback:
                self._callback(self.lat, self.lon)

        def _on_status(self, stype, status):
            pass

        def get_location(self):
            return self.lat, self.lon

else:

    class LocationProvider:
        def __init__(self):
            self.lat = None
            self.lon = None

        def start(self, callback):
            pass

        def stop(self):
            pass

        def get_location(self):
            return self.lat, self.lon
