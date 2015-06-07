import subprocess


def watch_sass_stylesheets(sass_folder, css_folder, output_style='expanded'):
    """Run the Sass watcher to automatically update CSS stylesheets from their Sass sources.

    :param sass_folder: folder path where are stored the Sass source files.
    :param css_folder: folder path where will be generated the CSS stylesheets.
    :param output_style: the style (e.g., expanded, compressed) used by Sass to generate the CSS stylesheet.
    """
    subprocess.call(
        [
            'sass',
            '--watch', '{}:{}'.format(sass_folder, css_folder),
            '--style', output_style,
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
