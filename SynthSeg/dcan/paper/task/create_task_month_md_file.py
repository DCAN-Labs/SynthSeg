from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("nnn-mmo.md")

task = 527
months = range(1, 9)
month = 1
tasks_folder = f'/home/miran045/reine097/projects/abcd-nn-unet/doc/tasks/{task}/by_month/{month}mo'
filename = f"{tasks_folder}{task}_{month}mo.md"
iou_median = 0.8579990956943074
dice_score_median = 0.9235467322361468
content = template.render(
    task,
    month=1,
    comment='527 was trained with T1/T2 image pairs',
    iou_median=str(iou_median),
    dice_score_median=str(dice_score_median)
)
with open(filename, mode="w", encoding="utf-8") as report:
    report.write(content)
    print(f"... wrote {filename}")
