---
title: Timelines
status: draft
date: 2024-01-01
tags:
---

## Todos
### Geographic Locations
#### africa
#### australasia
#### china
#### central_america
#### europe
#### north_america
#### russia
#### south_america

### Politics
#### british_politics
#### french_politics
#### usa_politics
#### wars
#### monarchies

### Humanities
#### art
#### authors
#### law
#### food
#### music
#### philosophers

### Sociology
#### crime
#### murderers
#### religions
#### technology

### Misc
#### dk

## Timeline Format
```
# Ext: .timeline

# For file global tags:
:tags ....

# Form One: Event
year       event country person* :desc .... :tags ... :wiki ....

# Form Two: Period:
year -> year event country person_surname* :tags ... :wiki .... :desc ....

1922 -> 1933 "a period of time"      england blah_bloo bloo_blee :tags blah,blee,blah :link blah
2003         "an event"              usa     a_person            :tags politics       :link https://blah :desc
```
