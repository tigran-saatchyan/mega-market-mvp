from datetime import datetime


def save_picture(instance, filename):
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name
    my_date = str(datetime.now().isoformat())

    picture_name = "".join(
        [
            "".join(filename.split('.')[:-1]),
            my_date,
            ".",
            filename.split('.')[-1]
        ]
    )
    return f"{app_name}/{model_name}/{instance.pk}/{instance.pk}_{picture_name}"
