## Semantic Proximity Search on Heterogeneous Graph by Proximity Embedding

Paper:
- *Motivation*: Many real-world networks have a rich collection of objects. The semantics of 
these objects allows us to capture different class of proximities, thus enabling an important
task of semantic proximity search. As the core of semantic proximity search, we have to measure 
the proximity on a heterogeneous graph, whose nodes are various types of objects. Most of the 
existing methods rely on **engineering features about the graph structure** between two nodes to 
measure  their proximity. With recent development on graph embedding, **we see a good chance to 
avoid feature engineering for semantic proximity search**. There is very little work on using graph
embedding for semantic proximity search. We also observe that graph embedding methods typically 
focus on embedding node, which is an "indirect" approach to learn the proximity.

        Keywords: semantic proximity search, lstm, heterogeneous graph

- Methods: 
    ![Overview][1]

English:
- words:
    - proximity (接近 接近度)
    - advisor/advisee(顾问/指导老师)
    - deliberately (故意地 谨慎地 慎重地)
    - straightforward (直截了当地/坦率地 直截了当的/坦率的)
    - symmetric/asymmetric (对称/非对称)
    - explicit/implicit (明确的/含蓄的)
    - immediate (立即的 直接的)
    - various/varying (各种各样的)
    - trivially (琐碎地 平凡地)
    - emphasize (强调)
    - enforce (实施 执行 请破)
    - vanish (消失)
    - explode (爆炸)
    - intermediate (中间物)
    - pool (合并 联营)
    - aggregate (集合 聚集 合计)
    - unified (统一的)
    - ultimate (终极 基本原则 最终的)
    - accumulate (累积 积聚)

- sentences:
    - be of various type 各种各样的
    - be of varing length 各种长度的


[1]: https://github.com/trajepl/pando/blob/master/related/fig/proximity-embedding.png?raw=true "proximity embedding"