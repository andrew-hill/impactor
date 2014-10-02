impactor
========

Simple script to search academic journal impact factors from http://www.citefactor.org/

* Search by ISSN or partial title
* Downloads full listing from citefactor.org and can save to local database for repeat searching
* Sorting of output table

dependencies
------------

* Python 2.7.8 or thereabouts (untested on any other version)
* BeautifulSoup4 (http://www.crummy.com/software/BeautifulSoup/)
* PrettyTable (https://code.google.com/p/prettytable/)

example usage
-------------

```
% ./impactor.py --db journals.db -s 2013/2014 robotics
+-------+-------------------------------------------------------------------------+-----------+-----------+-------+-------+-------+-------+-------+
| INDEX |                                 JOURNAL                                 |    ISSN   | 2013/2014 |  2008 |  2009 |  2011 |  2010 |  2012 |
+-------+-------------------------------------------------------------------------+-----------+-----------+-------+-------+-------+-------+-------+
|  4153 |                International Journal Of Humanoid Robotics               | 0219-8436 |   0.408   | 0.542 |  1.23 | 0.373 | 0.879 | 0.368 |
|  305  |                            Advanced Robotics                            | 0169-1864 |   0.562   | 0.737 | 0.629 | 0.571 | 0.653 |  0.51 |
|  4289 |              International Journal Of Robotics & Automation             | 0826-8185 |   0.658   | 0.409 | 0.339 | 0.288 | 0.206 | 0.494 |
|  5390 |       Journal of Mechanisms and Robotics-Transactions of the ASME       | 1942-4302 |   0.863   |   -   |   -   | 1.062 |   -   | 0.967 |
|  8048 |                     Robotics And Autonomous Systems                     | 0921-8890 |   1.105   | 1.214 | 1.361 | 1.056 | 1.313 | 1.156 |
|  4188 | International Journal Of Medical Robotics And Computer Assisted Surgery | 1478-5951 |   1.532   | 1.043 | 1.376 | 1.588 | 1.257 | 1.488 |
|  8049 |              Robotics And Computer-Integrated Manufacturing             | 0736-5845 |   1.839   | 1.371 | 1.687 | 1.173 | 1.254 |  1.23 |
|  5054 |                        Journal of Field Robotics                        | 1556-4959 |    1.88   | 2.684 | 1.989 | 2.244 |  3.58 | 2.152 |
|  3712 |                   Ieee Robotics & Automation Magazine                   | 1070-9932 |   2.319   |   3   |  2.09 | 1.985 | 2.173 | 2.484 |
|  4290 |                International Journal Of Robotics Research               | 0278-3649 |   2.503   | 2.882 | 1.993 | 3.107 | 4.095 | 2.863 |
|  3787 |                      IEEE Transactions on Robotics                      | 1552-3098 |   2.649   | 2.656 | 2.035 | 2.536 | 3.063 | 2.571 |
+-------+-------------------------------------------------------------------------+-----------+-----------+-------+-------+-------+-------+-------+
```
