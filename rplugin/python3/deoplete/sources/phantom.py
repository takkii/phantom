import gc
import os
import re
import traceback
import yaml
from deoplete.source.base import Base
from operator import itemgetter
from typing import Optional


# Use Config project
class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name: Optional[str] = 'Phantom'
        self.filetypes = ['php']
        mark_synbol: Optional[str] = '[PHP-complete]'
        self.mark = str(mark_synbol)
        php_match = [r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*']
        slash_no_match = [r'[;/[^¥/]\*/]']
        self.input_pattern = '|'.join(php_match + slash_no_match)
        self.rank = 500

    def get_complete_position(self, context):
        php_complete: Optional[str] = '[a-zA-Z0-9_?!]*$'
        m = re.search(php_complete, context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            # Settings, Config path is true/false change.
            config_load: Optional[str] = '~/config/load.yml'
            plug_config: Optional[str] = '~/.neovim/plugged/config/load.yml'

            # Settings, Loading File PATH.
            file_load: Optional[str] = 'PHP_HOME'
            plug_load: Optional[str] = 'PHP_File'

            # Home Folder, Set the dictionary.
            if os.path.exists(os.path.expanduser(config_load)):
                with open(os.path.expanduser(config_load)) as yml:
                    config = yaml.safe_load(yml)

                # Get Receiver/php Method Complete.
                with open(os.path.expanduser(config[file_load])) as r_method:
                    data = list(r_method.readlines())
                    data_php: Optional[list] = [s.rstrip() for s in data]
                    complete: Optional[list] = data_php
                    complete.sort(key=itemgetter(0))
                    return complete

            # Use vim-plug, Set the dictionary.
            elif os.path.exists(os.path.expanduser(plug_config)):
                with open(os.path.expanduser(plug_config)) as yml:
                    config = yaml.safe_load(yml)

                # Get Receiver/php Method Complete.
                with open(os.path.expanduser(config[plug_load])) as r_method:
                    data = list(r_method.readlines())
                    plug_php: Optional[list] = [s.rstrip() for s in data]
                    r_complete: Optional[list] = plug_php
                    r_complete.sort(key=itemgetter(0))
                    return r_complete

            # Config Folder not found.
            else:
                raise ValueError("None, Please Check the Config Folder")

        # TraceBack.
        except Exception:
            # Load/Create LogFile.
            except_folder: Optional[str] = 'PHP_Except_Folder'
            except_file: Optional[str] = 'PHP_Except_File'
            phantom: Optional[str] = os.path.expanduser(config[except_folder])
            debug_word: Optional[str] = os.path.expanduser(config[except_file])

            # Load the dictionary.
            if os.path.isdir(phantom):
                with open(debug_word, 'a') as log_py:
                    traceback.print_exc(file=log_py)

                    # throw except.
                    raise RuntimeError from None

            # Phantom Foler not found.
            else:
                raise ValueError("None, Please Check the Phantom Folder.")

        # Custom Exception.
        except ValueError as ext:
            print(ext)
            raise RuntimeError from None

        # Once Exec.
        finally:
            # GC collection.
            gc.collect()
