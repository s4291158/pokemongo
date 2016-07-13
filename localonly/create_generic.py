import os
import ast
import re

from pokemongo.settings import BASE_DIR

VIEWSET_LIST = {
    'ReadOnlyModelViewSet': '    \'get\': \'list\',\n',

    'ModelViewSet': '    \'get\': \'list\',\n'
                    '    \'post\': \'create\'\n',
}

VIEWSET_DETAIL = {
    'ReadOnlyModelViewSet': '    \'get\': \'retrieve\',\n',

    'ModelViewSet': '     \'get\': \'retrieve\',\n'
                    '     \'put\': \'update\',\n'
                    '     \'patch\': \'partial_update\',\n'
                    '     \'delete\': \'destroy\'\n',
}

EXTRA_REGEX = re.compile(
    "(# <extra (\w+) (\w+)>"
    "[\s\S]+?"
    "# </extra>\n)"
)


def get_underscore_name(model, joined=True):
    name_list = re.findall('[A-Z][^A-Z]*', model)
    if joined:
        underscore_name = '_'.join(name_list).lower()
    else:
        underscore_name = [x.lower() for x in name_list]

    return underscore_name


def add_extra_imports(blocks, extras):
    if 'imports' in extras:
        blocks.append(extras['imports']['block'])
        blocks.append('\n')
    return blocks


def get_model_list(models, extras, class_type):
    """get a list of models to (re)construct generic files
    :param models: class from models.py and templatemodels.py
    :param extras: dictionary containing all extra info
    :param class_type: either `Serializer`, `ViewSet`
    :return: a list of models (classes)
    """
    if 'classes' in extras and extras['classes']:
        model_list = [x.replace(class_type, '') for x in extras['classes']]
        model_list.extend(set(models) - set(model_list))
    else:
        model_list = models

    return model_list


def create_serializer(model, extras):
    if model in extras:
        extra = extras[model]
    else:
        extra = {}

    block = 'class {0}Serializer(serializers.ModelSerializer):\n' \
            '{1}' \
            '    class Meta:\n' \
            '        model = {0}\n' \
            '{2}' \
            '\n' \
            '\n' \
        .format(model,
                '    ' + extra['fields'] if 'fields' in extra else '',
                '        ' + extra['meta'] if 'meta' in extra else '')
    return block


def create_serializers_import(app, models, extras):
    models_import = []
    templatemodels_import = []
    for model in models:
        if 'Template' in model:
            templatemodels_import.append(model)
        else:
            models_import.append(model)

    blocks = []

    blocks.append(
        'from rest_framework import serializers\n'
        '\n'
    )

    if models_import:
        blocks.append(
            'from {0}.models import (\n'
            '    {1}\n'
            ')\n'
            '\n'
        )

    if templatemodels_import:
        blocks.append(
            'from {0}.templatemodels import (\n'
            '    {2}\n'
            ')\n'
            '\n'
        )

    add_extra_imports(blocks, extras)

    blocks.append('\n')

    block = ''.join(blocks).format(
        app,
        ',\n    '.join(models_import),
        ',\n    '.join(templatemodels_import)
    )

    return block


def write_serializers(models, extras, app, file):
    import_block = create_serializers_import(app, models, extras)
    file.write(import_block)
    model_list = get_model_list(models, extras, 'Serializer')
    for model in model_list:
        file.write(create_serializer(model, extras))


def create_url(models):
    blocks = []
    for model in models:
        underscore_name = get_underscore_name(model, joined=False)
        blocks.append(
            '    url(r\'^{0}/$\', {1}_list, name=\'{1}_list\'),\n'
            '    url(r\'^{0}/(?P<pk>[0-9]+)/?$\', {1}_detail, name=\'{1}_detail\'),\n'
                .format(
                '_'.join(underscore_name),
                '_'.join(underscore_name)
            )
        )

    block = ''.join(blocks)
    return block


def create_urls_import(app, models, extras):
    views_import = []
    for model in models:
        name = get_underscore_name(model)
        views_import.append(name + '_list')
        views_import.append(name + '_detail')

    blocks = []

    blocks.append(
        'from django.conf.urls import url\n'
        '\n'
    )

    if views_import:
        blocks.append(
            'from {0}.views import (\n'
            '    {1}\n'
            ')\n'
            '\n'
        )

    add_extra_imports(blocks, extras)

    blocks.append('\n')

    block = ''.join(blocks).format(
        app,
        ',\n    '.join(views_import),
    )

    return block


def write_urls(models, extras, app, file):
    import_block = create_urls_import(app, models, extras)
    file.write(import_block)

    urls_block = 'urlpatterns = [\n' \
                 '{0}' \
                 '{1}' \
                 ']\n' \
        .format(
        create_url(models),
        '    ' + extras['urls']['block'] if 'urls' in extras else ''
    )
    file.write(urls_block)


def create_view(model, extras, viewset_type):
    if model in extras:
        extra = extras[model]
    else:
        extra = {}

    blocks = []

    blocks.append(
        'class {0}ViewSet(viewsets.{2}):\n'
        '    queryset = {0}.objects.all()\n'
        '    serializer_class = {0}Serializer\n'
        '{5}'
        '\n'
        '\n'
    )

    blocks.append(
        '{1}_list = {0}ViewSet.as_view({{\n'
        '{3}'
        '}})\n'
        '\n'
    )

    blocks.append(
        '{1}_detail = {0}ViewSet.as_view({{\n'
        '{4}'
        '}})\n'
        '\n'
        '\n'
    )

    block = ''.join(blocks).format(
        model,
        get_underscore_name(model),
        viewset_type,
        VIEWSET_LIST[viewset_type],
        VIEWSET_DETAIL[viewset_type],
        '    ' + extra['block'] if 'block' in extra else ''
    )

    return block


def create_views_import(app, models, extras):
    models_import = []
    templatemodels_import = []
    serializers_import = []
    for model in models:
        serializers_import.append(model + 'Serializer')
        if 'Template' in model:
            templatemodels_import.append(model)
        else:
            models_import.append(model)

    blocks = []

    blocks.append(
        'from rest_framework import viewsets\n'
        '\n'
    )

    if models_import:
        blocks.append(
            'from {0}.models import (\n'
            '    {1}\n'
            ')\n'
            '\n'
        )

    if templatemodels_import:
        blocks.append(
            'from {0}.templatemodels import (\n'
            '    {2}\n'
            ')\n'
            '\n'
        )

    if serializers_import:
        blocks.append(
            'from {0}.serializers import (\n'
            '    {3}\n'
            ')\n'
            '\n'
        )

    add_extra_imports(blocks, extras)

    blocks.append('\n')

    block = ''.join(blocks).format(
        app,
        ',\n    '.join(models_import),
        ',\n    '.join(templatemodels_import),
        ',\n    '.join(serializers_import)
    )

    return block


def write_views(models, extras, app, file):
    import_block = create_views_import(app, models, extras)
    file.write(import_block)
    model_list = get_model_list(models, extras, 'ViewSet')

    for model in model_list:
        if 'template' in model.lower() and 'skill' not in model.lower():
            file.write(create_view(model, extras, 'ReadOnlyModelViewSet'))
        else:
            file.write(create_view(model, extras, 'ModelViewSet'))

    if 'views' in extras:
        file.write(extras['views']['block'])


def get_app_path(app):
    return os.path.join(BASE_DIR, app)


def get_extras_from_file(file_path):
    extras = {}
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

            blocks = EXTRA_REGEX.findall(file_content)

            class_regex = re.compile(
                "class (\w+)\("
            )
            extras['classes'] = class_regex.findall(file_content)

            for i, match in enumerate(blocks):
                if match[1] in extras:
                    extras[match[1]][match[2]] = match[0]
                else:
                    extras[match[1]] = {
                        match[2]: match[0]
                    }

    except FileNotFoundError:
        pass

    return extras


def get_classes_from_file(file_path):
    extras = {}
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            e = re.compile(
                "class (\w+)\("
            )
            matches = e.findall(file_content)

            for i, match in enumerate(matches):

                j = {
                    'type': match[2],
                    'content': match[0]
                }

                if match[1] in extras:
                    extras[match[1]][match[2]] = match[0]
                else:
                    extras[match[1]] = {
                        match[2]: match[0]
                    }

    except FileNotFoundError:
        pass

    return extras


def write_all_files(models, app, app_path, target_file, test):
    file_types = ['serializers', 'urls', 'views']
    for file_type in file_types:
        if target_file and target_file != file_type:
            continue
        if test:
            path = os.path.join(app_path, 'test_' + file_type + '.py')
        else:
            path = os.path.join(app_path, file_type + '.py')

        print('creating {} ...'.format(path), end='')

        extras = get_extras_from_file(path)
        file = open(path, 'w+')
        if 'serializers' in path:
            write_serializers(models, extras, app, file)
        elif 'urls' in path:
            write_urls(models, extras, app, file)
        elif 'views' in path:
            write_views(models, extras, app, file)
        file.close()

        print('OK')


def get_models_from_file(models_path):
    try:
        models = [node.name for node in ast.walk(
            ast.parse(open(models_path).read())
        ) if isinstance(node, ast.ClassDef) and node.name != 'Meta']

    except FileNotFoundError:
        models = []

    return models


def get_models_from_app(app_path):
    models_path = os.path.join(app_path, 'models.py')
    templatemodels_path = os.path.join(app_path, 'templatemodels.py')

    models = []
    models.extend(
        get_models_from_file(models_path)
    )
    models.extend(
        get_models_from_file(templatemodels_path)
    )

    return models


def loop_apps(target_app=None, target_file=None, test=True, count=False):
    counter = 0
    for app in os.listdir(BASE_DIR):
        app_path = get_app_path(app)
        try:
            # enable specific app
            if target_app and target_app != app:
                continue

            models = get_models_from_app(app_path)
            # skip app if no models found
            if not models:
                continue
            else:
                counter += len(models)

            if not count:
                write_all_files(models, app, app_path, target_file, test)

        except NotADirectoryError:
            pass

    if count:
        print(counter)
