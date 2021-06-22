from jinja2 import Environment, BaseLoader


class TMLParserEnvironment(Environment):
    """
    Extension on top of the jinja2 Environment altered for TML
    """
    def __init__(self, *args, **kwargs):
        super().__init__(finalize=lambda x: x if x is not None else '', *args, **kwargs)

    def load_file(self, file):
        """
        Load a file into the environment and return a jinja2 Template.

        Args:
            file: BytesIO file

        Returns: jinja2 Template

        """
        self.loader = self.FileLoader(file)
        return self.get_template(file.name)

    def add_object_to_globals(self, obj):
        """
        Globals are callable directly from template.
        """
        self.globals[obj.__name__] = obj

    class FileLoader(BaseLoader):
        """
        Loads a template from a BytesIO file as an extension of BaseLoader
        """

        def __init__(self, file, encoding='utf-8'):
            self.file = file
            self.encoding = encoding

        def get_source(self, environment, template):
            source = self.file.read().decode(self.encoding)
            return source, None, None

        def list_templates(self):
            return self.file.name
