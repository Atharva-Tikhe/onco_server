import json
import pickle
import re
import string
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
import pandas as pd
import plotly.express as px
import plotly
import plotly.tools as tls
from gensim.models.keyedvectors import KeyedVectors
from nltk import FreqDist
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud


class PlotDispatch:
    def __init__(self, file) -> None:
        self.file = file

        # self.df = pd.read_csv(rf"{sys.argv[0]}")
        self.df = pd.read_csv(rf"{file}")
        self.abst_list = self.df['Abstract'].values.astype('U')

        self.nopunc = str.maketrans('', '', string.punctuation)
        self.lem = WordNetLemmatizer()
        self.custom_stopwords = set(stopwords.words("english") + ["study", "group", "patient", "used", "gene", "protein", "drug", "chemical", "biomarker"
                                                                  "disease", "tcga" "effect", "method", "also",
                                                                  "result", "two", "may", "level",
                                                                  "participant", "treatment", "associated"
                                                                  "risk", "however", "year",
                                                                  "the", "this", "using", "showed", "analysis"])
        self.custom_stopwords = [self.lem.lemmatize(
            word) for word in self.custom_stopwords]

        self.abstract_list = self.preprocess(self.abst_list)

        self.abstract_tokens = self.tokenizer(self.abstract_list)

        # Word Vectorization
        self.vectorizer = KeyedVectors.load_word2vec_format(
            r'E:\MIT\OncoOmics_portal\pubmed_ml\PubMed-w2v.bin', binary=True)

        # text_vectors = self.w2v_vectorizer(self.abstract_tokens, self.vectorizer)

        # Model building¶
        # checking for optimal number of clusters
        self.sse = []
        self.list_k = list(range(2, 10))

        # Top words from each cluster
        self.df['preprocessed_abstract'] = self.abstract_list
        # self.df['labels'] = self.k_means.labels_
        # # self.df['labels'].value_counts()

    def preprocess(self, abst_list):
        abstracts = []
        for line in abst_list:
            line.replace("\n", "")
            line = line.lower()
            line = line.translate(self.nopunc)
            line = re.sub('[^A-Za-z]', ' ', line)
            new = ' '
            for word in line.split():
                word = self.lem.lemmatize(word)
                if word not in self.custom_stopwords and len(word) > 3:
                    new = new + ' ' + word
            abstracts.append(new)
        return abstracts

    def tokenizer(self, abst_list):
        abstract_tokens = []
        for line in abst_list:
            tokens = word_tokenize(line)
            tokens = [t for t in tokens if len(t) > 3]
            abstract_tokens.append(tokens)
        return abstract_tokens

    def w2v_vectorizer(self, list_of_docs, model):
        features = []

        for tokens in list_of_docs:
            zero_vector = np.zeros(model.vector_size)
            vectors = []
            for token in tokens:
                if token in model:
                    try:
                        vectors.append(model[token])
                    except KeyError:
                        continue
            if vectors:
                vectors = np.asarray(vectors)
                avg_vec = vectors.mean(axis=0)
                features.append(avg_vec)
            else:
                features.append(zero_vector)
        return features

    def plot_elbow(self):
        self.text_vectors = self.w2v_vectorizer(
            self.abstract_tokens, self.vectorizer)
        for k in self.list_k:
            km = MiniBatchKMeans(init='k-means++', n_clusters=k,
                                 random_state=0, n_init=20, max_iter=1000)
            km.fit(self.text_vectors)

            self.sse.append(km.inertia_)

        self.fig_elbow = plt.figure(figsize=(6, 6))
        plt.plot(self.list_k, self.sse, '-o')
        plt.xlabel('Number of clusters k')
        plt.ylabel('sum of squared distance')
        plt.title('Elbow Method For Optimal k')

        plotly_fig = tls.mpl_to_plotly(self.fig_elbow)

        graphJSON = json.dumps(plotly_fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def clustering_and_pca(self):
        self.text_vectors = self.w2v_vectorizer(
            self.abstract_tokens, self.vectorizer)
        k = 6
        self.k_means = MiniBatchKMeans(init='k-means++', n_clusters=k,
                                       random_state=0, n_init=20, max_iter=1000)
        self.k_means.fit(self.text_vectors)

        self.df['labels'] = self.k_means.labels_

        # visualization
        pca = PCA(n_components=2, random_state=0)
        reduced_vectors = pca.fit_transform(self.text_vectors)
        reduced_clusters = pca.fit_transform(self.k_means.cluster_centers_)

        self.clusters = plt.figure(figsize=(6, 6))
        plt.scatter(reduced_vectors[:, 0],
                    reduced_vectors[:, 1], c=self.k_means.labels_)
        plt.scatter(reduced_clusters[:, 0],
                    reduced_clusters[:, 1], marker='x', s=150, c='r')

        plotly_fig = tls.mpl_to_plotly(self.clusters)

        graphJSON = json.dumps(plotly_fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def get_top_n_words(self, corpus, n):
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx])
                      for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        return words_freq[:n]

    def get_wordcloud(self, text):
        word_cloud = WordCloud(
            collocations=False, background_color='white').generate(text)
        plotly_fig = px.imshow(word_cloud)
        # plot = plt.imshow(word_cloud, interpolation='bilinear')
        # plt.axis("off")

        # plotly_fig = tls.mpl_to_plotly(plot)

        graphJSON = json.dumps(plotly_fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def impl_word_cloud(self):

        word_cloud_texts = []

        for clus in range(2):
            self.text = ' '
            df2 = self.df.loc[self.df["labels"] == clus]

            # wordcloud
            for abst in df2.preprocessed_abstract:
                self.text += abst
            # word_cloud_texts.append(self.get_wordcloud(self.text))

            # top10words
            words = []
            for i, j in self.get_top_n_words(df2["preprocessed_abstract"], 10):
                words.append(i)
            # print("Top 10 words from cluster", clus, ":")
            # print(words)

        # return word_cloud_texts
        return self.text

    def save_model(self):
        # saving the model¶
        with open('clustererbreast_model.pkl', 'wb') as f:
            pickle.dump(self.k_means, f)

        mod = pickle.load(open('clusterer_model.pkl', 'rb'))

    def frequency_dist(self):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        self.fdlist = FreqDist(self.abstract_list)
        # count = len(self.fdlist)

        fig = make_subplots(rows=1, cols=2)
        # self.fdlist.most_common(10)

        tokenized_word = word_tokenize(self.text)
        # print(tokenized_word)

        fdist = FreqDist(tokenized_word)
        # print(fdist)
        # fdist.most_common(2)

        fdist_plots = []

        fdist_30 = fdist.plot(30, cumulative=False)
        # plt.show()

        # plotly_fig = tls.mpl_to_plotly(fdist_30)
        # plotly_fig = px.imshow(fdist_30)
        fig.add_trace(go.Scatter(fdist_30), row=1, col=1)

        graph_30 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        fdist_plots.append(graph_30)

        # fdist_10 = fdist.plot(10, cumulative=False)
        # plt.show()

        # plotly_fig = tls.mpl_to_plotly(fdist_10)
        # plotly_fig = px.imshow(fdist_10)
        # plotly_fig = asarray(fdist_10)

        # graph_10 = json.dumps(plotly_fig, cls=plotly.utils.PlotlyJSONEncoder)

        # fdist_plots.append(graph_10)

        return fdist_plots


# kmeans_fdist = PlotDispatch('Breast.csv')
# kmeans_fdist = PlotDispatch(
#     r'E:\MIT\OncoOmics_portal\pubmed\medicinal database_results.csv')

    # // var fdist1 = {{freq[0] | safe}};
    # // Plotly.plot('fdist1',fdist1,{});

    # // var fdist2 = {{freq[1] | safe}};
    # // Plotly.plot('fdist2',fdist2,{});
