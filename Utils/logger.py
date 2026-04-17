class Logger:
    COLORS = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "END": "\033[0m"
    }

    def __init__(self, name):
        self.name = name

    def _log(self, level, msg):
        color = self.COLORS.get(level, "")
        print(f"{color}[{level}] [{self.name}] {msg}{self.COLORS['END']}")

    def info(self, msg):
        self._log("INFO", msg)

    def success(self, msg):
        self._log("SUCCESS", msg)

    def warning(self, msg):
        self._log("WARNING", msg)

    def error(self, msg):
        self._log("ERROR", msg)
