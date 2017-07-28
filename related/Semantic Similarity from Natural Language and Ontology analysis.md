# Survey: semantic Similarity from Natural Language and Ontology analysis
---


### Notes:
- Definitions of semantic measures and related vocabulary
    - Definitons of semantic measures
        - *Semantic measures* are mathematical tools used to estimate the strength of the semantic relationship between units of language, concepts or instances, through a (numerical) description obtained according to the comparison of information supporting their meaning.
    - Related vocabulary
        - *Semantic similarity*: subset of the notion of semantic relatedness only considering taxonomic relationships in the evaluation of the semantic interaction between two elements.
        - *Semantic relatedness*: the strength of the semantic interactions between two elements with no restrictions on the types of the semantic links considered.
        - Knowledge graph
            ![related vocabulary][1]
- Research status
    ![research status][2]


- Methods:
    - corpus-based process
        ![corpus-based process][3]
    - knowledge-based process
        strongly depending on the qulitity of ontologies.
        - Measures adapted to semantic graphs composed of (multiple) predicate(s) which potentially induce cycles.
            - Measures based on graph traversal.
                1. shortest path
                2. random-walk
                3. other interconnection measures
            - Measures based on graph property model.
        - Measures adapted to taxonomies, i.e., acyclic semantic graphs composed of a unique predicate inducing transitivity.


- Reference
    - Euzenat and Shvaiko, 2013
    

English expression:
- is not considered to be the root of sth.
- to stress the point
- for the sake of clarity


[1]: https://github.com/trajepl/pando/blob/master/related/fig/related-vocabulary.png?raw=true "related vocabulary"
[2]: https://github.com/trajepl/pando/blob/master/related/fig/research-status.png?raw=true "research status"
[3]: https://github.com/trajepl/pando/blob/master/related/fig/corpus-based-process.png?raw=true "General process commonly adopted for the definition of corpus-based semantic measures"