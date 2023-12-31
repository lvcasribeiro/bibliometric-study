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

###### 2. Year analysis:
It will perform an analysis based on the publications years of the documents, returning a bar chart with the total amount of each one of them:

```python
year_analysis.year_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/12329fd3-dbc5-43cf-8158-cbdd5e6dcf96">
</p>

##

###### 3. Evolution of publications per year analysis:
It will perform an analysis based on the publications years of the documents, returning a line chart with the evolution of publications per year:

```python
evolution_analysis.evolution_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/5f411e09-b72b-4bd2-8d4b-87a3c1fe91a5">
</p>

##

###### 4. Documents type analysis:
It will perform an analysis based on the documents type, returning a pie chart with all types identified and a caption box at the top right corner:

```python
type_analysis.type_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/b870cf14-0743-4a65-b656-f16831bcf9af">
</p>

##

###### 5. Word cloud analysis:
It will perform an analysis based on the main keywords from title and abstract, returning a word map with the most relevant keywords related to the document, the most relevant being displayed in larger sizes:

```python
wordmap_analysis.wordmap_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/65f0b6c4-e52d-4f46-8269-76aeb93cc411">
</p>

##

###### 6. Keywords analysis:
It will perform an analysis based on the keywords, returning a bar chart with the 10 most relevant keywords related to the document:

```python
keywords_analysis.keywords_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/9f687edc-659d-499c-9fbe-ad5f3a8d66b4">
</p>

##

###### 7. Periodics analysis:
It will perform an analysis based on the publishers or periodics, returning a bar chart with the 10 most relevant publishers, based on the total amount of publications:

```python
periodics_analysis.periodics_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/058e01b0-1b5a-4ad7-9e1d-0acffa6cad8e">
</p>

##

###### 8. Citations analysis:
It will perform an analysis based on the citations of each document, returning a bar chart with the 10 most relevant papers, based on the total amount of citations:

```python
citations_analysis.citations_analysis(scopus_dataframe);
```

<p align="center">
    <img src="https://github.com/lvcasribeiro/bibliometric-study/assets/96185134/00338528-5db4-425c-be37-55c9365e1e5a">
</p>

##

### Remider

At first, the framework will perform analyzes only on files derived from the **scopus** database, later, I will add treatment for the **web of science** and **IEEE** databases.