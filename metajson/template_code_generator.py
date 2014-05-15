import os
import datetime
import time

class TemplateCodeGenerator :

    TEMPLATE_EXT = ".mustache"
    DEFAULT_TEMPLATE_PATH = "./metajson/templates"

    def __init__(self, template_path = DEFAULT_TEMPLATE_PATH, output_path = "classes", project_prefix = "S2M"):
        self.project_prefix = project_prefix
        self.template_path = template_path
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        self.output_path = output_path
        self.read_template()

    def read_template(self):
        self.json_template_files = []
        self.general_template_files = []
        for root, dirs, files in os.walk(self.template_path):
            if root == self.template_path:
                for name in files:
                    filepath = os.path.join(root, name)
                    basename, extension = os.path.splitext(filepath)
                    if extension == TemplateCodeGenerator.TEMPLATE_EXT:
                        template_basename, template_extension = os.path.splitext(basename)
                        if template_basename != basename:
                            self.json_template_files.append(filepath)
            else:
                for name in files:
                    filepath = os.path.join(root, name)
                    self.general_template_files.append(filepath)

    def create_output_file(self, filename):
        start = filename.find(self.template_path)

        if start == -1:
            new_filename = filename
        else:
            new_filename = filename[len(self.template_path):]
        directories, new_filename = os.path.split(new_filename)

        # customize output filename
        today = datetime.date.fromtimestamp(time.time())
        new_filename = self.replace_variables(new_filename, today)

        if directories.startswith("/"):
            directories = directories[1:]

        end_dir = os.path.join(self.output_path, directories)
        if not os.path.exists(end_dir):
            os.makedirs(end_dir)
        return open(os.path.join(end_dir, new_filename), 'w')

    def write_general_template_files(self):
        for input_file in self.general_template_files:
            print input_file
            output_file = self.create_output_file(input_file)
            if output_file:
                self.write_template(input_file, output_file)
            else:
                print "skip " + input_file

    def replace_variables(self, text, today):
        newtext = text.replace('_DATE_', "")
        newtext = newtext.replace('_YEAR_', str(today.year))
        newtext = newtext.replace('_PREFIX_', self.project_prefix)
        return newtext

    def write_template(self, template, output):
        today = datetime.date.fromtimestamp(time.time())
        # write content to ouptut
        try:
            for line in open(template):
                newLine = self.replace_variables(line, today)
                output.write(newLine)
        finally :
            output.close()
