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
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['qauntum', 'computing'],  
  install_requires=[            
          'click',
          'pyyaml'
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)