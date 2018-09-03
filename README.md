## Product finder with Scrapy

This project shows an example of website crawling with [Scrapy](https://doc.scrapy.org/en/latest) framework. 

First of all it is better to create a folder that will hold your whole project. After that you should enter this folder and it is recommended to use virtual environment

```
pip install virtualenv
```

Install Scrapy with

```
pip install Scrapy
```

> Note that sometimes this may require solving compilation issues for some Scrapy dependencies depending on your operating system, so be > sure to check the [Platform specific installation notes](https://doc.scrapy.org/en/latest/intro/install.html#intro-install-platform-notes) 

Now you are ready to start the project

```
scrapy startproject yourpoject
```

It creates a directory with such structure

```
yourpoject/
    scrapy.cfg            # deploy configuration file

    yourpoject/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

To put this spider to work, go to the project’s top level directory and run:

```
scrapy crawl dior_spider -o links.csv -t csv
```
> or depending on your prefernces and future tasks
```
scrapy crawl dior_spider -o goods.json 
```

Results will be saved to goods.json file. Further analysis can be performed with help of [Pandas](https://pandas.pydata.org/) library.


### CONTACT

Please send you feedback to

  max.savin3@gmail.com
