## Bibliometric Graphs Generator

The codes present in this repository aim to create a web framework for generating graphs and statistical resources related to a scopus database.

##

### Analyzes and their results

###### 1. Language analysis:
It will perform an analysis based on the writing language of the documents, returning a pie chart with the percentages equivalent to each one of them:

```python
languages_analysis.languages_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/8c0bf6d6-4d38-40bf-bd49-4035628d5d05">
</p>

##

### Remider

At first, the framework will perform analyzes only on files derived from the **scopus** database, later, I will add treatment for the **web of science** and **IEEE** databases.