import os
import random

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

task = 527


def get_iou_median(age_group):
    # TODO Finish
    return random.random()


def get_dice_score_median(age_group):
    # TODO Finish
    return random.random()


age_groups = \
    [{"age_group": age_group, "iou_median": get_iou_median(age_group),
      "dice_score_median": get_dice_score_median(age_group),
      'comment': '527 was trained with T1/T2 image pairs', 'task': 527}
     for age_group in range(1, 9)]

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("nnn-mmo.md")

for age_group in age_groups:
    month = age_group["age_group"]
    tasks_folder = f'/home/miran045/reine097/projects/abcd-nn-unet/doc/tasks/{task}/by_month/{month}mo'
    Path(tasks_folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(tasks_folder, f"{task}_{month}mo.md")
    content = template.render(
        age_group
    )
    with open(filename, mode="w", encoding="utf-8") as report:
        report.write(content)
        print(f"... wrote {filename}")
