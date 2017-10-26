import os
import sys
import shlex
import subprocess

MIXPANEL_SCRIPT_ACCESSORY_FILES = ['paginator.py']
MIXPANEL_MAIN_FILE = ['__init__.py']
def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def get_mixpanel_module():
	mixpanel_text = ''
	import mixpanel_api
	module_directory = os.path.dirname(mixpanel_api.__file__)
	files = get_filepaths(module_directory)
	print files
	for f in files:
		for accessory in MIXPANEL_SCRIPT_ACCESSORY_FILES:
			if accessory in f and '.pyc' not in f:
				print f
				with open(f) as file_to_be_read:
					for l in file_to_be_read:
						mixpanel_text += l

	m_init = [x for x in files if '__init__.py' in x and '.pyc' not in x]
	print m_init
	with open(m_init[0]) as file_to_be_read:
		for l in file_to_be_read:
			if 'from paginator' not in l:
				mixpanel_text += l
	return mixpanel_text

def process_script(script):
	divider = '''
################################################################################
# Below this is the actual written script above is the mixpanel_api module #####
################################################################################
	'''

	compiled_script = ''
	compiled_script += get_mixpanel_module() + '\n'
	compiled_script += divider
	compiled_script += '\n'
	with open(script) as fi:
		for line in fi:
			if 'mixpanel_api' not in line and 'import' not in line:
				compiled_script += line

	return compiled_script


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Usage: python process_script.py script_name api_secret \n Please provide the api secret for this project as well"
		sys.exit()
	input_script = sys.argv[1]
	api_secret = sys.argv[2]
	processed_script = process_script(input_script)
	processed_name = input_script.split('.py')[0] + '_proc.py'
	print processed_name
	with open(processed_name,'w') as out:
		out.write(processed_script)
	cmd_str = 'zip -P %s %s.zip %s' %(api_secret,processed_name,processed_name)
	subprocess.check_call(shlex.split(cmd_str))
