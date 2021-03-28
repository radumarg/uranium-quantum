from distutils.core import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
  name = 'uranium-quantum',         
  packages = ['uranium_quantum'],   
  version = '0.1.0',     
  license='MIT', 
  description = 'Support libraries for the Uranium quantum computing platform.',  
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Radu Marginean',                   
  author_email = 'radu.marg@gmail.com',     
  url = 'https://github.com/radumarg/uranium-quantum',   
  download_url = 'https://github.com/radumarg/uranium-quantum/archive/refs/tags/v0.1.0.tar.gz',    
  keywords = ['quantum', 'computing', 'uranium platform'],  
  install_requires=[            
          'click',
          'pyyaml'
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)