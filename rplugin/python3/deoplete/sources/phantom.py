import csv
import gc
import os
import re
import yaml
import traceback
from operator import itemgetter
from deoplete.source.base import Base


# GitHub: config version is v1.3.3
class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'Phantom'
        self.filetypes = ['ruby']
        mark_synbol = '[Phantom]'
        self.mark = str(mark_synbol)
        ruby_match = [r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*']
        slash_no_match = [r'[;/[^¥/]\*/]']
        self.input_pattern = '|'.join(ruby_match + slash_no_match)
        self.rank = 500

    def get_complete_position(self, context):
        m = re.search('[a-zA-Z0-9_?!]*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            # Set the dictionary.
            with open(os.path.expanduser("~/config/load.yml")) as yml:
                config = yaml.safe_load(yml)
            a1 = os.path.expanduser(config['Folder_Load_Path'])

            if os.path.isdir(a1):
                ruby_method = open(os.path.expanduser(
                    config['File_Load_Path']))

            # The dictionary not found.
            else:
                print("Please, Check the path of phantom.")

            # read
            data = list(ruby_method.readlines())
            data_ruby = list(map(lambda s: s.rstrip(), data))
            ruby_method.close()

            # sort and itemgetter
            dic = data_ruby
            dic.sort(key=itemgetter(0))
            return dic

        except Exception:
            traceback.print_exc()
        except OSError as e:
            print(e)
        except ZeroDivisionError as zero_e:
            print(zero_e)
        except TypeError as type_e:
            print(type_e)
        except FileNotFoundError as file_not:
            print(file_not)
        finally:
            gc.enable()
