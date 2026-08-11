import nbformat
import copy
import os
import signal


class CellTimeout(Exception):
    pass


def _alarm_handler(signum, frame):
    raise CellTimeout("cell execution timed out")


def _exec_cell(source, namespace, timeout=15):
    previous_handler = signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(timeout)
    try:
        exec(source, namespace)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)


def import_notebook(path):
    # Change to the main directory (one level up from the test directory)
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(main_dir)
    
    notebook = nbformat.read(str(path), as_version=nbformat.NO_CONVERT)
    namespace = {}
    section_data = {}  # Dictionary to store variables by section
    current_section = None  # To track the current section tag
    
    for cell in notebook["cells"]:
        cell_error = None
        if cell["cell_type"] == "code":
            try:
                _exec_cell(cell["source"], namespace)
            except Exception as exc:  # Ignore any cell that has any error
                cell_error = f"{type(exc).__name__}: {exc}"

        # Get the section tag, if any, or set to None if not present
        tags = cell.get("metadata", {}).get("tags", [])
        section = tags[0] if tags else None
        if section is None:
            continue
        # Check if the section has changed
        if section and section != current_section:
            current_section = section

        # Initialize section data if not already present
        if current_section not in section_data:
            section_data[current_section] = {"variables": {}, "source": "", "errors": []}

        # Save the source code of the cell
        section_data[current_section]["source"] += cell["source"] + "\n"

        if cell_error:
            section_data[current_section]["errors"].append(cell_error)

        # Save a snapshot of the variables to section_data
        for var_name in namespace:
            try:
                section_data[current_section]["variables"][var_name] = copy.deepcopy(namespace[var_name])
            except TypeError:
                # Skip variables that cannot be deepcopied
                pass


    return section_data, namespace