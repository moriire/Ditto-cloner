from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = 'Gecko Website Cloner/Copier'

setup( 
		name ='ditto', 
		version ='0.0.1', 
		author ='Mobolaji Abdulsalam', 
		author_email ='ibraheemabdulsalam@gmail.com', 
		url ='https://github.com/moriire/Gecko-cloner', 
		description ='Gecko Website Cloner/Copier', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'ditto = ditto.main:cli'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords =long_description, 
		install_requires = requirements, 
		zip_safe = False
) 
