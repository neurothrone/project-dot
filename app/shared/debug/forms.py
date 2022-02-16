from flask_wtf import FlaskForm


def print_form_errors(form: FlaskForm) -> None:
    for field, errors in form.errors.items():
        for error in errors:
            print(f"Form Field Error:"
                  f"\n\tField: {getattr(form, field).label.text}"
                  f"\n\tError: {error}")
