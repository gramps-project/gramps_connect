Gramps Connect
==============

Current Status

General
-------
- [x] Delete with confirm
- [x] Image viewer
- [x] Paged view for all
- [ ] Validation and redo (insure unique, give error messages, retry)
- [ ] Actions
  - [x] List, search, view
  - [ ] Where do they go? How to notify? In background?
  - [x] Reports
  - [x] Exports
  - [ ] Imports
- [ ] User settings (password, theme, database, superuser, rw, access to tree, preferred output format (html, pdf, svg))
- [x] Search

Forms - add, edit, view list
-----------------
- [x] Person (except bools and lists)
- [ ] Family
  - [x] List
  - [ ] View and Edit
- [ ] Citation/Source (form should be shared)
  - [ ] List
  - [ ] View and Edit
- [ ] Source
  - [ ] List
  - [ ] View and Edit
- [ ] Event
  - [ ] List
  - [ ] View and Edit
- [ ] Media
  - [ ] List
  - [ ] View and Edit
- [ ] Place
  - [ ] List
  - [ ] View and Edit
- [ ] Repository
  - [ ] List
  - [ ] View and Edit
- [x] Note
  - [ ] List
  - [ ] View and Edit
- [ ] Tag
  - [ ] List
  - [ ] View and Edit

Editing
-------
- [ ] Lists (tags, etc)
- [ ] Types (pick list with override)
- [ ] Gender

Tabs
------
- [ ] Address
- [ ] Association
- [ ] Attribute
- [ ] Children (for Family)
- [ ] Citation
- [ ] Citation Reference
- [ ] Data
- [ ] Event Reference
- [x] Event (needs link)
- [ ] Internet (for Repository)
- [ ] LDS
- [ ] Location
- [ ] Media
- [ ] Media Reference
- [ ] Name
- [ ] Note
- [ ] Note Reference
- [ ] Person Reference
- [ ] Place Reference
- [ ] Repository Reference
- [ ] Repository
- [ ] Source Reference
- [ ] Surname
- [ ] Tag Reference

Issues
------
- [x] Tables sort order. Apparently, Gramps Gtk will resort the entire
      table to get tke order correctly. We should be able to do better,
      for this and Gramps Gtk. get_XXX_handles(sort_handles=True)
      This order is a rough surname-ordered, only used for picklists.