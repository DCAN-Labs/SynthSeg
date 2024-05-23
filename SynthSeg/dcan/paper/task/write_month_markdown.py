import argparse
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from dcan.paper.iou_dice_score import get_medians


def main(ground_truth_folder, predictions_folder, task, task_comment):
    def get_iou_median(age_group):
        return get_medians(ground_truth_folder, predictions_folder, month=age_group)['iou_median']

    def get_dice_score_median(age_group):
        return get_medians(ground_truth_folder, predictions_folder, month=age_group)['dice_score_median']

    def get_count(age_group):
        return get_medians(ground_truth_folder, predictions_folder, month=age_group)['count']

    age_groups = \
        [{"age_group": age_group, "count": get_count(age_group), "iou_median": get_iou_median(age_group),
          "dice_score_median": get_dice_score_median(age_group),
          'comment': task_comment, 'task': task}
         for age_group in range(9)]

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='WriteMonthMarkdown',
        description='Creates markdown files for reports by age group.',
        epilog='Contact reine097 if you have questions or run into problems.')
    parser.add_argument('ground_truth_folder', help='Folder containing ground truth segmentations')
    parser.add_argument('predictions_folder', help='Folder containing inferred segmentations')
    parser.add_argument('task', help="Task number")
    parser.add_argument('task_comment', help="Explanatory text for task")
    args = parser.parse_args()
    ground_truth_folder = args.ground_truth_folder
    predictions_folder = args.predictions_folder
    task = int(args.task)
    task_comment = args.task_comment
    main(ground_truth_folder, predictions_folder, task, task_comment)
