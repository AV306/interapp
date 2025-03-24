import re, os;
from collections import namedtuple;
from pathlib import Path;

Import = namedtuple( "Import", "object_name imported_file_name" );
# TODO: can add more classes for additional import info
REMOVAL_PATTERN = re.compile( "[\';,{}\n]+" );

def ts_import_filter( source_file_path: Path, line ) -> Import:
    """Extract imported objects and their source files from TS/JS files"""
    # e.g. import a from 'foo'
    imported_objects = [];
    if "import" in line and "from" in line:
        tokens = line.split( " " );
        # TODO: shoould we split "," as a token?

        # Handle multiple imports
        for token in tokens[1:]:
            if token == "from": # Break on "from", indicating end of objects to import
                break;

            token = REMOVAL_PATTERN.sub( '', token ); # Remove unwanted characters
            if token:
                imported_objects.append( token );

        imported_file_path = REMOVAL_PATTERN.sub( '', tokens[-1] );
        if "@" not in imported_file_path:
            # Not a module, resolve relative path to absolute
            imported_file_path = Path( os.path.relpath( source_file_path.parent, start=imported_file_path ) ).resolve();

        return Import( imported_objects, imported_file_path );



IMPORT_FILTERS = {
    "ts": ts_import_filter,
    "tsx": ts_import_filter,
    "js": ts_import_filter,
    "jsx": ts_import_filter
}

"""FILE_LOCATORS = {
    "ts": ts_file_locator,
    "tsx": ts_file_locator,
    "js": ts_file_locator,
    "jsx": ts_file_locator
}"""