def add_qss(widget, new_qss):
    origin_qss = widget.styleSheet()
    if origin_qss:
        widget.setStyleSheet(origin_qss + " " + new_qss)
    else:
        widget.setStyleSheet(new_qss) 