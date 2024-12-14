import argparse
import frontmatter
import os
import markdown
import jinja2
import yaml

def parse_fm(src):
    data = []
    for x in os.listdir(src):
        post = frontmatter.load(f"{src}/{x}")
        meta = post.metadata
        meta['file'] = x
        data.append(meta)
    return data

def main():
    parser = argparse.ArgumentParser(description='Website Generator')
    parser.add_argument('-src',help='Source folder',default='src')
    parser.add_argument('-dest',help='Destination folder',default='build')
    args = parser.parse_args()

    print(f"src = {args.src}")
    print(f"dest = {args.dest}")

    os.makedirs(args.dest, exist_ok=True)

    with open(f"{args.src}/config.yml","rt",encoding='utf-8') as y:
        cfg = yaml.safe_load(y)

    data = parse_fm(args.src)
    
    template_dir = 'template'
    for x in os.listdir(args.src):
        if x.endswith('.md'):
            key = x.replace('.md','')
            post = frontmatter.load(f"{args.src}/{x}")

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir)).get_template('page.html')
            print(f"Writing {args.dest}/{key}.html")
            with open(f"{args.dest}/{key}.html","wt",encoding='utf-8') as h:
                result = env.render(data = data,cfg = cfg, content = markdown.markdown(post.content))
                h.write(result)

if __name__=='__main__':
    main()