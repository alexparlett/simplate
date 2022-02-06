import argparse
import json
import sys

from simplate.template import Template


def parse_context(context_string):
    return json.loads(context_string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a template.')
    parser.add_argument('template', type=str, help='a template to process')
    parser.add_argument("--context", "-c", dest='ctx', help='a json string containing the context to template with',
                        type=str)

    args = parser.parse_args()

    ctx = parse_context(args.ctx)
    template = Template()
    result = template.render(args.template, ctx)

    sys.stdout.write(result)
    sys.exit(0)
