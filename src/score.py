# score.py

class Score:
    def __init__(self):
        self.lines = []
        self.last_bonus = 0
        self.score = 0

    def add_lines(self, lines):
        self.lines.append(lines)
        self.last_bonus = lines ** 2
        self.score += self.last_bonus

    def get_current_score(self):
        lines = self.lines[-1] if self.lines else 0
        return "Score: {} (+{} point{} for {} line{})".format(
            self.score,
            self.last_bonus, "" if self.last_bonus == 1 else "s",
            lines, "" if  lines == 1 else "s")

    def get_final_score(self):
        lines = sum(self.lines)
        return "Final score: {} ({} resolved line{})".format(
            self.score,
            lines, "" if lines == 1 else "s")