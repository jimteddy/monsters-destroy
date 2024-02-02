import os
from pathlib import Path
import json


class Scoring:
    def __init__(self):
        self.scores = []

    @property
    def best_score(self):
        with open(self.path, "r") as f:
            donnee = json.load(f)
            if len(donnee) == 0:
                return 0
            return max(donnee)

    def load_score(self):
        with open(self.path, "r") as f:
            donnee = json.load(f)
            self.scores = donnee
        self.scores.reverse()
        return self.scores

    def sort_best_score(self, new_score: int):
        self.load_score()
        if len(self.scores) <= 4:
            self.scores.append(new_score)
        else:
            self.scores.sort()
            if new_score > self.scores[0]:
                self.scores[0] = new_score
        self.scores.sort()

    @property
    def path(self):
        return os.path.join(Path.home(), "scores.json")

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.scores, f, indent=4, ensure_ascii=True)


if '__main__' == __name__:
    score = Scoring()
    print(score.scores)
    score.sort_best_score(100)
    score.save()
    score.load_score()
    score.sort_best_score(50)
    score.save()
    score.load_score()
    score.sort_best_score(60)
    score.save()
    score.load_score()
    score.sort_best_score(40)
    score.save()
    score.load_score()
    score.sort_best_score(10)
    score.save()
    score.load_score()
    score.sort_best_score(80)
    score.save()
    score.load_score()
    score.sort_best_score(90)
    score.save()
    score.load_score()
    score.sort_best_score(30)
    score.save()
    score.load_score()
    print(score.scores)
