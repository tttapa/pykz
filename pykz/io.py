"""Reading and writing to files.
"""
import os


def __export_to_tempfile(code: str) -> str:
    """Export latex code to temp file"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        print("Writing to tempfile")
        f.write(code)
        # f.flush()
    return f.name


def build_latex_code(code: str) -> str:
    file = __export_to_tempfile(code)
    return build_latex_file(file)


def build_latex_file(path: str) -> str:
    import subprocess
    from pykz.exceptions import PDFlatexNotFoundError, CompilationError
    import os
    working_dir = os.path.dirname(path)

    try:
        # Run pdflatex command
        print("Running pdflatex")
        subprocess.run(['pdflatex', "-interaction=nonstopmode", "-halt-on-error", path],
                       capture_output=True,
                       cwd=working_dir,
                       check=True)
        print("Pdflatex done!")
    except FileNotFoundError:
        raise PDFlatexNotFoundError("pdflatex command not found. Please make sure it is installed and accessible in the system's PATH.")
    except subprocess.CalledProcessError as e:
        error_message = f"{e.stdout.decode('UTF-8')}\n\nCompilation failed with the error above ☝️ "
        raise CompilationError(error_message)
    import os

    for ext in {".aux", ".log"}:
        try:
            os.remove(path + ext)
        except FileNotFoundError():
            ...
    return f"{path}.pdf"


def open_pdf_file(file_path: str):
    import sys
    import subprocess
    print("Opening pdf file")

    if sys.platform.startswith('darwin'):  # macOS
        result = subprocess.run(['open', file_path], capture_output=True, text=True)
    elif sys.platform.startswith('win32'):  # Windows
        import os
        result = os.startfile(file_path)
    elif sys.platform.startswith('linux'):  # Linux
        result = subprocess.run(['xdg-open', file_path], capture_output=True, text=True)
    else:
        print("Unsupported platform. Unable to open PDF file.")
    input("Press any key to continue.")
    if result.returncode != 0:
        print(sys.stdout)


def preview_latex_doc(code: str) -> str:
    pdf_path = build_latex_code(code)
    print(pdf_path)
    open_pdf_file(pdf_path)
    try:
        os.remove(pdf_path)
    except FileNotFoundError():
        ...


if __name__ == "__main__":

    TEX_STRING = r"""
    \documentclass{article}
    \begin{document}
        hello world.
    \end{document}
    """
    preview_latex_doc(TEX_STRING)
