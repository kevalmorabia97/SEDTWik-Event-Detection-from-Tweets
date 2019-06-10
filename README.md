# SEDTWik: Event Detection from Tweets
Implementation of my paper: **SEDTWik: Segmentation-based Event Detection from Tweets using WIKipedia** which is available [here](https://www.aclweb.org/anthology/papers/N/N19/N19-3011/)

<p align="center">
    <img src="https://github.com/kevalmorabia97/SEDTWik-Event-Detection-from-Tweets/blob/master/img/sedtwik.jpg"/>
    <b>SEDTWik Architecture</b>
</p>

## The process of Event detection can be divided into 4 parts:
### 1. Tweet Segmentation
Split a given tweet into non-overlapping meaningful segments, giving more weight to hashtags (𝐻). Filter out words not present as a Wikipedia page title.

| Tweet                   | Segmentation (with 𝐻 = 3)               |
| ----------------------- | --------------------------------------- |
|Joe Biden and Paul Ryan will be seated at the debate tonight _#VpDebate_|[joe biden], [paul ryan], [seated], [debate], [tonight], [vp debate]x3|
|Amanda Todd took her own life due to cyber bullying _#RipAmandaTodd_ _#NoMoreBullying_|[amanda todd], [cyber bullying], [rip amanda todd]x3, [no more bullying]x3|


### 2. Bursty Segment Extraction
Score segments based on their bursty probability (𝑃<sub>𝑏</sub>), and follower count (𝑓𝑐), retweet count (𝑟𝑐), and count of unique users using them (𝑢). Select top 𝐾=√(𝑁<sub>𝑡</sub> ) segments based on 𝑆𝑐𝑜𝑟𝑒 (𝑁<sub>𝑡</sub> = total number of tweets in current time window).<br>
𝑃<sub>𝑏</sub>(s) measures how frequent a segment is occurring compared to its expected probability of occurrence.<br>
Score<sub>s</sub> = 𝑃<sub>b</sub>(𝑠) × log⁡(𝑢<sub>s</sub>) × log(rc<sub>s</sub>) × log⁡(log⁡(𝑓𝑐<sub>s</sub>)).


### 3. Bursty Segment Clustering
Variation of Jarvis-Patrick Clustering algorithm.<br>
Segments considered as nodes in a graph and 2 segments belong to same cluster if both are in 𝑘-NN of each other.<br>
Segment similarity: 𝑡𝑓−𝑖𝑑𝑓 similarity between contents of tweets containing the segment.


### 4. Event Summarization
TEXT TEXT TEXT

## Cite
```
@inproceedings{morabia-etal-2019-sedtwik,
    title = "{SEDTW}ik: Segmentation-based Event Detection from Tweets Using {W}ikipedia",
    author = "Morabia, Keval  and
      Bhanu Murthy, Neti Lalita  and
      Malapati, Aruna  and
      Samant, Surender",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Student Research Workshop",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-3011",
    pages = "77--85",
}
```
**Abstract:**
<br>Event Detection has been one of the research areas in Text Mining that has attracted attention during this decade due to the widespread availability of social media data specifically twitter data. Twitter has become a major source for information about real-world events because of the use of hashtags and the small word limit of Twitter that ensures concise presentation of events. Previous works on event detection from tweets are either applicable to detect localized events or breaking news only or miss out on many important events. This paper presents the problems associated with event detection from tweets and a tweet-segmentation based system for event detection called SEDTWik, an extension to a previous work, that is able to detect newsworthy events occurring at different locations of the world from a wide range of categories. The main idea is to split each tweet and hash-tag into segments, extract bursty segments, cluster them, and summarize them. We evaluated our results on the well-known Events2012 corpus and achieved state-of-the-art results
