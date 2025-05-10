import os
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QMessageBox

def update_image_files_list(path, viewer):
    directory = os.path.dirname(path)
    viewer.image_files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.heic', '.heif')):
            full_path = os.path.join(directory, filename)
            viewer.image_files.append(full_path)
    viewer.image_files.sort()
    try:
        viewer.current_index = viewer.image_files.index(path)
    except ValueError:
        viewer.current_index = -1

def navigate_next(viewer):
    if not viewer.image_files or viewer.current_index == -1:
        return
        
    viewer.current_index = (viewer.current_index + 1) % len(viewer.image_files)
    viewer.open_heic_file(viewer.image_files[viewer.current_index])
    
def navigate_prev(viewer):
    if not viewer.image_files or viewer.current_index == -1:
        return
        
    viewer.current_index = (viewer.current_index - 1) % len(viewer.image_files)
    viewer.open_heic_file(viewer.image_files[viewer.current_index])

def get_relative_position(pos, image_label, scroll_area):
    if not image_label.pixmap() or not pos:
        return None
    
    viewport = scroll_area.viewport()
    label = image_label
    pixmap = label.pixmap()
    label_pos = label.mapTo(viewport, QPoint(0, 0))
    img_width = pixmap.width()
    img_height = pixmap.height()
    
    x_offset = 0
    y_offset = 0
    if img_width < viewport.width():
        x_offset = (viewport.width() - img_width) / 2
    if img_height < viewport.height():
        y_offset = (viewport.height() - img_height) / 2
    
    rel_x = (pos.x() - label_pos.x() - x_offset) / img_width
    rel_y = (pos.y() - label_pos.y() - y_offset) / img_height
    rel_x = max(0.0, min(1.0, rel_x))
    rel_y = max(0.0, min(1.0, rel_y))
    return rel_x, rel_y

def adjust_scroll_position(rel_pos, scroll_area, image_label):
    if not rel_pos:
        return
    
    rel_x, rel_y = rel_pos
    h_bar = scroll_area.horizontalScrollBar()
    v_bar = scroll_area.verticalScrollBar()
    pixmap = image_label.pixmap()
    new_width = pixmap.width()
    new_height = pixmap.height()
    viewport = scroll_area.viewport()
    viewport_width = viewport.width()
    viewport_height = viewport.height()
    
    new_x = int(rel_x * new_width - rel_x * viewport_width)
    new_y = int(rel_y * new_height - rel_y * viewport_height)
    
    h_bar.setValue(max(0, new_x))
    v_bar.setValue(max(0, new_y))
