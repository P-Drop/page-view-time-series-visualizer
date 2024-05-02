import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)

df = df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
df.set_index('date', inplace=True)

# Clean data

top_filter = df['value'] <= df['value'].quantile(0.975)
bottom_filter = df['value'] >= df['value'].quantile(0.025)
df = df[(top_filter) & (bottom_filter)]


def draw_line_plot():
    # Draw line plot

    fig = plt.figure(figsize=(15, 6))

    plt.plot(df, c='tab:red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    date_range = pd.date_range('2016-01-01', '2019-12-03', freq='D')
    df_complete  = df.reindex(date_range).fillna(0)

    df_bar = df_complete.groupby([df_complete.index.year, df_complete.index.month, df_complete.index.month_name()], group_keys=False)[['value']].mean()
    df_bar.index.names = ['year', 'month', 'month_name']
    df_bar.reset_index(inplace=True)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 


    # Draw bar plot

    fig, ax = plt.subplots(figsize=(8,6))

    sns.barplot(
        data = df_bar,
        x = 'year',
        y = 'value',
        hue = 'month_name',
        hue_order = month_list,
        errorbar = None,
        palette = 'tab10',
        ax = ax,
        legend = False
    )

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation= 90)
    ax.legend(title='Months', labels=month_list)




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box['month_num'] = [d.month for d in df_box.date]
    df_box = df_box.sort_values(by=['month_num', 'year'], ascending=True)

    # Draw box plots (using Seaborn)

    fig, (ax1, ax2) = plt.subplots(figsize=(30, 10), nrows=1, ncols=2)

    sns.boxplot(
        data = df_box,
        x = 'year',
        hue = 'year',
        y = 'value',
        palette = 'tab10',
        ax = ax1,
        legend = False
    )

    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    sns.boxplot(
        data = df_box,
        x = 'month',
        hue = 'month',
        y = 'value',
        palette = 'husl',
        ax = ax2,
        legend = False
    )

    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
