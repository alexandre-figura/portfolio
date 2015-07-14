============================
Portfolio - Alexandre Figura
============================

.. image:: https://travis-ci.org/alexandre-figura/portfolio.svg?branch=master
    :target: https://travis-ci.org/alexandre-figura/portfolio

This is the second version of my portfolio.

Work in progress...

Content
=======
My portfolio is organized around three categories:

- **specialties**: can be hard or soft skills, but also technology names,
- **projects**: pieces of work demonstrating mastery of the specialties,
- **jobs**: positions held in different companies, during which the projects have been realized.

Relations
=========
Relations between content categories are pretty simple:

- a specialty can be linked to projects or jobs,
- a project can be linked to a job (or not, like pet projects).

In the rest of this documentation, I will use the term *item* when making reference to an element of any category.

Organization
============
Each item is reprensented by a **text file**, which must comply with the reStructuredText_ syntax. Files are organized according to the following global directory tree:

- jobs
- projects
- specialties

Directory and file names (without their extension) are used in URLs of the porfolio. They allow to retrieve the content of a specific item. Hence, it is recommended to use lowercase and avoid special characters. For more information on file naming, please refer to the section how-to-link-items_.

.. _reStructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

Jobs
----
Jobs are regrouped by company. Here is an example of the directory sub-tree:

- company 1

  - job 1.rst

- company 2

  - job 1.rst
  - job 2.rst

A company directory can contain several job descriptions, as several positions can be held during career evolution.

.. _how-to-link-items:

How to link items
=================
When you want to refer to an item from another item, some rules apply to the item's name:

- it is converted to lowercase,
- spaces are replaced with underscores.

The converted name is then used as a reference for opening the corresponding item's file.

Why linking items in this way?
==============================
Mainly to reduce the amount of work needed to update references when an item is renamed:

- company or position names doest not change after a job item is created,
- likewise, project names often remain unchanged,
- but specialties can be reorganized or renamed during career evolution.

Hence, jobs are referenced in projects, and these two item categories are referenced in specialties.
