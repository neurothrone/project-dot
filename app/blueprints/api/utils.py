from flask import jsonify


def jsonify_not_found(item: str):
    return jsonify(dict(detail=f"{item} not found"))
