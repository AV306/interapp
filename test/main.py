import itertools as it;
import glob, os;
from pathlib import Path;
from filters import *;

SOURCE_FILE_EXTENSIONS = ["js", "ts", "jsx", "tsx"];
IGNORE_DIRECTORIES = ["node_modules"];

OUTPUT_FILE_NAME = "relationships.txt";

target_dir_name = "interapp-backend";

imports_adjacency_list = {}; # Files imported - filename: [(object, source), ...]

# "import" statement filter for TS


# Walk the given source directory
for ext in SOURCE_FILE_EXTENSIONS:
    #for fn in glob.iglob( os.path.join( target_dir_name, "**", "*."+ ext ), recursive=True ):
    for file_path in Path.cwd().glob( os.path.join( target_dir_name, "**", "*."+ ext ) ):
        #basename = os.path.splitext( os.path.basename( fn ) )[0];
        filter = IMPORT_FILTERS[ext];

        # Can't get the glob to ignore node_modules so...
        if not any( ignored_dir in file_path.parts for ignored_dir in IGNORE_DIRECTORIES ):
            # Open the file
            with open( file_path, "r" ) as source_file:
                # Look for "import" statements
                for line in source_file:
                    imports = filter( file_path, line.strip() );
                    if imports:
                        #print( f"{basename}: {filter( line.strip() )}" );
                        imports_adjacency_list.setdefault( file_path, [] ).append( imports );


# Dump imports table
with open( OUTPUT_FILE_NAME, "w+" ) as out:
    for file, imports in imports_adjacency_list.items():
        out.write( f"{file}:\n" );
        for obj, imported_file in imports:
            out.write( f"\t{obj} from {imported_file}\n" );