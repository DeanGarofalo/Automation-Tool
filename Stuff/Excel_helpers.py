
def get_cell_fill_color(sheet, row, column):
    cell = sheet.cell(row, column)
    fill = cell.fill
    if fill.start_color.index:
        return fill.start_color.index
    return None

def is_cell_green(sheet, row, column) -> bool:
    cell = sheet.cell(row, column)
    fill = cell.fill
    try:
        if fill.start_color.index == "FFC6EFCE":
            return True
    except AttributeError:
        return False
    return False

def is_cell_orange(sheet, row, column) -> bool:
    cell = sheet.cell(row, column)
    fill = cell.fill
    try:
        if fill.start_color.index == "FFFFCC99":
            return True
    except AttributeError:
        return False
    return False
    
def is_good_app(app: str):
    if app in ["SMGR", "SM"]:
        return False
    return True