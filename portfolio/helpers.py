from docutils.core import publish_parts


def rst_to_html(text):
    return publish_parts(text, writer_name='html')['html_body']
