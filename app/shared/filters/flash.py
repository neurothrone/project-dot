bg_colors = {
    "error": "bg-danger",
    "warning": "bg-warning",
    "success": "bg-success",
    "info": "bg-info",
    "primary": "bg-primary",
    "secondary": "bg-secondary",
}


def flash_category_color(category: str) -> str:
    return bg_colors.get(category, "bg-info")
