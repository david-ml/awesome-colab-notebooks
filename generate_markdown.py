from collections import defaultdict
from datetime import datetime
from json import load
from os.path import join

badges = {'colab', 'youtube', 'git', 'wiki', 'kaggle', 'arxiv', 'tf', 'pt', 'medium', 'reddit', 'neurips', 'paperswithcode', 'huggingface'}

def colab_url(url):
    return f'[![Open In Colab](images/colab.svg)]({url})'

def parse_link(link_tuple, height=20):
    name, url = link_tuple
    if name in badges:
        return f'[<img src="images/{name}.svg" alt="{name}" height={height}/>]({url})'
    return f'[{name}]({url})'

def parse_links(list_of_links):
    if len(list_of_links) == 0:
        return ''
    d = defaultdict(list)
    for name,url in list_of_links:
        d[name].append(url)
    if len(d) == 1:
        return ', '.join(parse_link(link_tuple) for link_tuple in list_of_links)
    return '<ul>' + ''.join('<li>' + ', '.join(parse_link((name, url)) for url in d[name]) + '</li>' for name in d.keys()) + '</ul>'

def generate_table(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        data = load(f)
    colabs = sorted(data, key=lambda kv: kv['update'], reverse=True)

    print('| name | description | authors | links | colaboratory | update |')
    print('|------|-------------|:--------|:------|:------------:|:------:|')
    for line in colabs:
        if len(line['author']) > 1:
            line['author'] = '<ul>' + ' '.join(f'<li>[{author}]({link})</li>' for author,link in line['author']) + '</ul>'
        else:
            if len(line['author'][0]) == 2:
                line['author'] = '[{}]({})'.format(*line['author'][0])
            else:
                line['author'] = line['author'][0][0]
        line['links'] = parse_links(sorted(line['links'], key=lambda x: x[0]))
        line['url'] = colab_url(line['colab'])
        line['update'] = datetime.fromtimestamp(line['update']).strftime('%d.%m.%Y')
        print('| {name} | {description} | {author} | {links} | {url} | {update} |'.format(**line))

def generate_markdown():
    print('# Awesome colab notebooks collection for ML experiments')
    print('## Research')
    generate_table(join('data', 'research.json'))
    print('## Tutorials')
    generate_table(join('data', 'tutorials.json'))
    print('\n[![Stargazers over time](https://starchart.cc/amrzv/awesome-colab-notebooks.svg)](https://starchart.cc/amrzv/awesome-colab-notebooks)')
    print(f'\n(generated by [generate_markdown.py](generate_markdown.py) based on [research.json](data/research.json) and [tutorials.json](data/tutorials.json))')

def main():
    generate_markdown()

if __name__ == '__main__':
    main()
