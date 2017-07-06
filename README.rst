What the Benchmark tool is about
==================



.. code-block:: console

    $ pip install benchsuite.controller

.. DANGER::
   Beware killer rabbits!


-- A fully computerized solution
 	
-- Ideal for the remote submitting of existing performance test
 
-- Multi-provider
	
-- Impletemented for the VM response-time calculation
 	
-- Can be extended to several application fields

-- Optimized for the obtained data analysis
 	
-- Based on metrics defined by the user


Functionalities included in this version
----

-- 	Creation/Distruction of instances on several cloud providers (Amazon EC2, Trystack, oVirt, Flexiant, Azure, Openstack)

-- Execution of existing performance workload
- DaCapo tool for java-based applications
- CloudSuite Data Caching tool for web application caching
- Dwarfs suite for CPUs benchmark
- Filebench for file system and storage benchmarks
- YCSB for the database evaluation

-- Data output parsing and database storing 

-- Integration with GUI interface    

Known issues of this version:
----
-- Dwarfs suite does not run properly on Debian

-- CloudSuite parser could not work correctly



# Getting Started

The Benchmarking Suite Controller is available on PyPI. To install just issue:

~~~
pip install benchsuite.controller
~~~

Before starting to use the Controller, it is necessary to create the configuration

~~~
git clone https://github.com/benchmarking-suite/benchsuite-configuration.git
export BENCHSUITE_CONFIG_FOLDER=`pwd`/benchsuite-configuration
~~~

This will download a basic configuration from which you can start. However this not include any working configuration for
cloud providers only examples. 


You can add the configuration to your .bashrc for convenience 

~~~
echo "export BENCHSUITE_CONFIG_FOLDER=`pwd`/benchsuite-configuration" >> ~/.bashrc
source ~/.bashrc
~~~

Functionality expected in next versions
----

-- Implementation of more Cloud Providers connectors (e.g.,GAE)
````````
Reference to the user/installation manual
----
Chapter 5 of the following document:

http://www.artist-project.eu/sites/default/files/D7.2.3_Cloud_services_modeling_and_performance_analysis_framework_M30_31032015.pdf

Reference for the download
----
The binary of the tool can be found at the following link:
https://github.com/artist-project/ARTIST/blob/master/binary/BenchmarkingSuite/Benchmarking%20Controller--3.0.0-0.tar.gz

Version
----

3.0

License
----

Apache 2.0


**Free Software, Hell Yeah!**


