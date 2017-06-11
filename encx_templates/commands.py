from encxlib.commands import BasePlugin

import logging
import jinja2
import yaml

import os

class Renderer(BasePlugin):
    name = 'renderer'
    commands = {
        'render': {
            'parser': 'parse_render',
            'run': 'render',
            'help': 'Render a template using the data from an encx file',
        },
    }

    def parse_render(self, parser):
        parser.add_argument('source', nargs="?", help='A encx file source')
        parser.add_argument('-k', '--key', dest='key', help='Key to use to decrypt', default=None)
        parser.add_argument('-f', '--file', help='A file to render as template')
        parser.add_argument('-t', '--template', help='A string to render as template')

    def render(self, args):
        payload, _ = self.client.decrypt_file(args.source, key=args.key)
        try:
            payload.decode('utf-8')
        except ValueError:
            logging.error('Could not render source encx file as it was not utf-8')
            return False

        data = yaml.safe_load(payload)
        if not isinstance(data, dict):
            logging.error('Data source did not load a dictionary as its root object. Invalid context :(')
            return False

        if not args.template and not args.file:
            logging.error('You must specify either a file or a template string')
            return False
        if args.template:
            template_text = args.template
        else:
            template_path = os.path.expanduser(args.file)
            with open(template_path) as template_file:
                template_text = template_file.read()

        template = jinja2.Template(template_text)
        output = template.render(data)
        self.client.write_file('-', output.encode('utf-8'))
