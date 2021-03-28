from distutils.core import setup
setup(
  name = 'uranium-quantum',         
  packages = ['uranium-quantum'],   
  version = '0.1.0',     
  license='MIT', 
  description = 'This package contains support Python libraries for the Uranium Quantum Computing Platform.',  
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