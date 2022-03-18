import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt

import itertools
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster import hierarchy as hc

st.set_page_config(
    layout="wide",
    page_title='Workload Dashboard',
    page_icon='📊'
)

#st.set_option('deprecation.showPyplotGlobalUse', False)

plt.style.use('seaborn-muted')

SYSTEMS = {
    'jump3r': ['time', 'max-resident-size'],
    'kanzi': ['time', 'max-resident-size', 'ratio'],
    'h2': ['throughput'],
    'batik': ['time', 'max-resident-size'],
    'jadx': ['time', 'max-resident-size'],
    'dconvert': ['time', 'max-resident-size'],
}

@st.cache
def load_options(system):
    data = pd.read_csv('models/{}_model.csv'.format(system))
    return data.option.unique()

@st.cache
def load_model(system, option, kpi):
    data = pd.read_csv('models/{}_model.csv'.format(system))
    return data[(data['option'] == option) & (data['kpi'] == kpi)]

@st.cache
def load_perf(system, workload, kpi):
    data = pd.read_csv('datax/{}_measurements.csv'.format(system))
    return data[data['workload'] == workload][kpi]

@st.cache
def load_workloads(system):
    data = pd.read_csv('models/{}_model.csv'.format(system))
    ws = data.workload.unique()
    return ws

@st.cache
def load_code(system, workload, clas, start, end):
    clas = resolve_class(system, clas)
    workload = resolve_workload(system, workload)

    path = 'code/{}/src/{}.java'.format(
        system,
        '/'.join(clas.split('.'))
    )

    with open(path, 'r') as f:
        return '\n'.join(f.read().split('\n')[start-1:end-1])

@st.cache
def resolve_class(system, clas):
    ''' int to str'''
    sqliteConnection = sqlite3.connect("./db/{}.sqlite".format(system))
    sqliteCursor = sqliteConnection.cursor()

    command = 'select class from classes where class_index = "{}"'.format(clas)
    sqliteCursor.execute(command)
    result = sqliteCursor.fetchone()[0]
    return result

@st.cache
def resolve_workload(system, workload):
    ''' str to int'''
    sqliteConnection = sqlite3.connect("./db/{}.sqlite".format(system))
    sqliteCursor = sqliteConnection.cursor()

    command = 'select workload_index from workloads where workload = "{}"'.format(workload)
    sqliteCursor.execute(command)
    result = sqliteCursor.fetchone()
    print(command)
    return result[0]

@st.cache
def load_workload_coverage(system, option, workload):
    workload = resolve_workload(system, workload)
    df = pd.read_csv('cache/{}/{}-workload-{}-option-{}.csv'.format(system, system,  workload, option))
    return df

@st.cache
def load_coverage(system, option):
    df = pd.read_csv('cache/{}/{}-option-{}.csv'.format(system, system,  option))
    return df

def jaccard(list1, list2):
    s1 = list1
    s2 = list2
    if len(s1) == 0 or len(s2) == 0:
        return 0.0
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def workload_plot(system, option):
    #feature_code = load_coverage(system, option).sort_values(by='class')
    workloads = load_workloads(system)

    wcovs = {w: load_workload_coverage(system, option, w) for w in workloads}

    corr = pd.DataFrame(np.zeros(shape=(len(workloads), len(workloads))),
        index=workloads, columns=workloads)

    for v, w in itertools.combinations(workloads, 2):
        s1 = df_to_set(wcovs[v])
        s2 = df_to_set(wcovs[w])
        #st.write(s1)
        sim = jaccard(s1, s2)
        const = 0.0
        corr[v].loc[w] = 1 - sim + const
        corr[w].loc[v] = 1 - sim + const

    fig = plt.figure(figsize=(3, 2))
    #plt.suptitle('Jaccard Similarity')
    plt.ylabel('$Workload$')
    plt.xlabel('$Jaccard$ $distance$')
    corr_condensed = hc.distance.squareform(corr) # convert to condensed
    z = hc.linkage(corr_condensed, method='complete')
    dendrogram = hc.dendrogram(z, labels=corr.columns, orientation='right')
    plt.yticks(rotation=0, fontsize=10)
    plt.xlim(-0.1, 1.1)
    return fig

def code_frequency_plot(system, option, workload):

    fig = plt.figure()

    cov = load_coverage(system, option)
    covv = cov.groupby('class').count().to_dict()['line']
    covv = {resolve_class(system, c):v for c,v in covv.items()}
    plt.barh(list(covv.keys()), list(covv.values()), edgecolor='black', color='white')

    wcov = load_workload_coverage(system, option, workload)
    covv = wcov.groupby('class').count().to_dict()['line']
    covv = {resolve_class(system, c):v for c,v in covv.items()}
    plt.barh(list(covv.keys()), list(covv.values()), edgecolor='black', color='#0000ff', alpha=0.3)

    return fig

def compact(xs, diff=5):
    xs = sorted(xs)
    xdiff = [0] + [xs[i+1] - xs[i] for i in range(len(xs) - 1)]
    ys = []
    last = 0
    for i, y in enumerate(xdiff):
        if y > diff:
            zzz = (xs[last], xs[i-1])
            last = i
            ys.append(zzz)
    ys.append((xs[last], xs[-1]))
    return ys

def df_to_set(df):
    df = set([str(tuple(row[1].values)) for row in df.iterrows()])
    return df

with st.sidebar:
    st.title('Settings')

    system = st.selectbox('Subject System', SYSTEMS.keys())
    options = load_options(system)
    option = st.selectbox('Configuration Option', load_options(system))
    kpi = st.selectbox('Performance Metric', SYSTEMS[system])
    workload = st.selectbox('Workload', load_workloads(system))
    perf = st.checkbox('Show Performance Influence per Workload', True)
    coverage = st.checkbox('Show Coverage Dendrogram', True)
    code = st.checkbox('Show Code Coverage under Option/Workload', False)

    with st.expander('Appearance'):
        positive_color = st.color_picker('Positive influence', '#ed2a07', on_change=None)
        negative_color = st.color_picker('Negative influence', '#0d6332', on_change=None)

    with st.expander('Code Retrieval'):
        prepend = st.slider('Prepended lines', 0, 10, 2)
        append = st.slider('Appended lines', 0, 10, 2)


coef = load_model(system, option, kpi)

col1, col2 = st.columns([1,1])
if perf:
    with col1:
        st.markdown('### Performance Influence per Workload', unsafe_allow_html=True)
        #col1.header('Performance')
        fig2 = plt.figure(figsize=(3, 2))
        f = coef.sort_values(by='influence')[['workload', 'influence']]
        f_pos = f[f['influence'] > 0]
        f_neg = f[f['influence'] < 0]
        for w in f.workload.unique(): plt.axhline(w, color='black', zorder=0, linewidth=0.5, linestyle=':')
        plt.barh(f_neg['workload'], f_neg['influence'], color=negative_color, alpha=1)
        plt.barh(f_pos['workload'], f_pos['influence'], color=positive_color, alpha=1)
        #plt.suptitle('Relative Performance Influence')
        plt.xlabel('$Standardized~regression~coefficient$')

        plt.ylabel('$Workload$')
        #plt.title(system + ': ' + kpi + ' influence of option "' + option + '"')
        plt.axvline(0, color='black')
        col1.pyplot(fig2)
        #fig2.savefig('plots/{}_{}_influences.pdf'.format(system, option), bbox_inches='tight')

    with col2:
        st.markdown('### Coverage Dendrogram', unsafe_allow_html=True)
        try:
            figg = workload_plot(system, option)
            #figg.savefig('plots/{}_{}_workloads.pdf'.format(system, option), bbox_inches='tight')
            st.pyplot(figg)
        except FileNotFoundError as e:
            t = "<div>Coverage dendrogramm unavailable for numeric configuration option «<b>{}</b>»</div>".format(option)
            st.markdown(t, unsafe_allow_html=True)
        #hist_bins = st.slider('Histogram bins', 10, 250,100)
        # = st.color_picker('Histogram bin color', '#3483eb', on_change=None)

            t = "<br /><div>This is due to missing coverage data for numeric options, which we can not enable/disable, only select specific values for.</div>".format(option)
            st.markdown(t, unsafe_allow_html=True)


if code:

    try:
        cov = load_coverage(system, option)
        covs = {}

        st.markdown('In this view, we show what code sections (specific to option <b>{}</b>) are covered under the selected workload <b>{}</b>. The green and red squares (🟩 and 🟥) indicate whether a line was covered or not, respectively.'.format(option, workload), unsafe_allow_html=True)
        for c, cg in cov.groupby('class'):
            lines = sorted(cg['line'].values)
            chunks = compact(lines, 35)
            class_name = str(resolve_class(system, c))
            class_path = 'code/{}/src/'.format(system) + '/'.join(class_name.split('.')) + '.java'
            try:
                with open(class_path, 'r') as f:
                    content = f.read().split('\n')
            except FileNotFoundError as e:
                pass

            for chunk in chunks:
                try:
                    with st.expander(class_name + ' ({} to {})'.format(chunk[0], chunk[1])):

                        # only for visualization
                        start = max(chunk[0] - prepend, 1)
                        end = min(chunk[1] + append, len(content) - 1)

                        display_lines = list(filter(lambda line: line <= end, lines))
                        display_lines = [line - start for line in display_lines]
                        display_code = content[start:end]
                        display_code = ['🟩 ' + dc_line if i in display_lines else '🟥 ' + dc_line for i, dc_line in enumerate(display_code)]

                        st.code('\n'.join(display_code))
                except FileNotFoundError as e:
                    pass
    except FileNotFoundError as e:
        t = "<div color='red'><it>Code unavailable for numeric options.</it></div>"
        st.markdown(t, unsafe_allow_html=True)

    with col5:
        pass
