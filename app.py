import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io


def round_percentage(number, total):
    return float(np.round(number / total * 100, decimals=2))


def year_percentage(column):
    return column.apply(lambda row: round_percentage(row, int(column.sum())))


df = pd.read_csv("crime.csv")

st.title("Crimes in Russia from 2003 to 2020 analysis")
st.write("In this project I'll work with a dataset containing crimes committed in Russia from 2003 to 2020. "
         "The data is provided per month and it is sorted into multiple columns with different types of crime.")


st.write("Check if there are empty or 'NaN' cells in the dataset:")
st.dataframe(df.isna().sum())
st.write("Check that data type is correct per column (in particular, for each column "
         "with numbers there are no cells with numbers written not in int/float (no '1M' instead of 1000000 etc.)):")
buffer = io.StringIO()
df.info(buf=buffer)
df_info = buffer.getvalue()
st.text(df_info)


st.write("")
st.write("Before starting to work on the dataset, I'd like to note that number of total crimes != sum of all types, "
         "as types of crimes may intersect:")
df_sum = df.drop("month", axis=1).sum()
st.write("Total crimes minus all types of crimes' sum: ", int(df.Total_crimes.sum()
                                                              - df_sum.drop("Total_crimes", axis=0).sum()))


st.write("After making sure that data is clean, let's look at the general trend of the dataset: number of total crimes "
         "(some descriptive statistics and a plot to visualise the data). As obtained numbers will show "
         "the mean/median/standart deviation of crimes, I will take integer part of them "
         "(for better understanding, as crimes cannot be float).")
st.write("Mean: ", int(df.Total_crimes.mean()))
st.write("Median: ", int(df.Total_crimes.median()))
st.write("Standart deviation: ", int(df.Total_crimes.std()))

st.write("Per year for the whole time presented in the dataset:")
st.write("As at the moment there is no column specifically with years, let's create one (using month column):")
df["year"] = df["month"].apply(lambda item: item[-4:])
st.dataframe(df)
st.write("Now, sum statistics (for each column) for 12 months of each year:")
st.write("Notice that there is only January in 2020 statistics, therefore, to obtain valid data, "
         "we should either exclude 2020 from per year sum statistics or multiply January results by 12 (months) "
         "-- which, of course, would be an assumption and might not correspond with season dependent tendencies and, "
         "consequently, will not be the strategy here (so let's exclude 2020 from per year statistics). "
         "From the dataset (printed above): year 2020 (January) = row (index) 204")
df_yearly = df.drop("month", axis=1).drop(204, axis=0).groupby(["year"]).sum()
st.dataframe(df_yearly)
st.write("Total crimes per year statistics:")
st.write("Mean: ", int(df_yearly.Total_crimes.mean()))
st.write("Median: ", int(df_yearly.Total_crimes.median()))
st.write("Standart deviation: ", int(df_yearly.Total_crimes.std()))

st.write("Now, after calculating some general variables for total crimes data, let's visualize the information. "
         "The data from this column will be presented as number of crimes over time "
         "with an illustration of mean as a horizontal line on the graph.")
st.write("Let's first do it for data per month:")
fig = df.plot(kind="scatter", x="month", y="Total_crimes", figsize=(39, 7), rot=90, color="black",
              title="All crimes over time").figure
plt.axhline(y=int(df.Total_crimes.mean()), color="crimson", label="mean", linewidth=2)
plt.legend(fontsize="18")
st.pyplot(fig)

st.write("Now, per year:")
df_yearly_index = df_yearly.index.astype(int)
xticks = range(df_yearly_index.min(), df_yearly_index.max() + 1)
fig = df_yearly.plot(y="Total_crimes", figsize=(15, 7), color="black", ylabel="number of cases",
                     title="All crimes per year").figure
plt.axhline(y=int(df_yearly.Total_crimes.mean()), color="crimson", label="mean", linewidth=2, ls="--")
plt.legend()
plt.xticks(range(0, 17), xticks)
st.pyplot(fig)
st.write("The crime rate rises from 2003 to 2006 and declines after with a slight rise for 2015 and an even smaller "
         "rise for 2019. It is possible to say that the trend is downward as the number of cases in 2003 is higher "
         "than in 2019.")
st.write("Note that it's not possible to put all months of all the years on x axis (written on the plot). "
         "Also notice that the per year graph represents the general trend (shown on per month graph as well) "
         "but doesn't illustrate yearly fluctuations, which, as can be concluded from comparing per year and "
         "per month plots, is not needed to be presented to understand the trend.")
st.write("So, all further time dependent plots will have years as x axis as it will provide essential information and "
         "not overload the plot with details.")


st.write("We obtained a tendency in the amount of all crimes committed from 2003 to 2019. I think that while the "
         "general trend is such, it is not true for some particular types of crimes. As an example, "
         "let's analyse fraud. Assumption: on the contrary to the general trend, the number of scams has significantly "
         "grown during these years.")
st.write("Mean per month: ", int(df.Fraud_scam.mean()))
st.write("Median per month: ", int(df.Fraud_scam.median()))
st.write("Standart deviation per month: ", int(df.Fraud_scam.std()))
st.write("Mean per year: ", int(df_yearly.Fraud_scam.mean()))
st.write("Median per year: ", int(df_yearly.Fraud_scam.median()))
st.write("Standart deviation per year: ", int(df_yearly.Fraud_scam.std()))
fig = df_yearly.plot.area(y="Fraud_scam", figsize=(15, 7), color="gray", ylabel="number of cases",
                                        title="Fraud per year").figure
plt.axhline(y=int(df_yearly.Fraud_scam.mean()), color="crimson", label="mean", linewidth=3, ls="--")
plt.legend()
plt.xticks(range(0, 17), xticks)
st.pyplot(fig)
st.write("On the graph we can see an overall rise of fraud from 2003 to 2019 with a peak in 2006 "
         "(or, we can say, a drop from 2006 to 2017). So the assumption was true.")


st.write("Let's now see whether the discovered trend for all crimes applies to serious crimes. Firstly, on the whole.")
st.write("Mean per month: ", int(df.Serious.mean()))
st.write("Median per month: ", int(df.Serious.median()))
st.write("Standart deviation per month: ", int(df.Serious.std()))
st.write("Mean per year: ", int(df_yearly.Serious.mean()))
st.write("Median per year: ", int(df_yearly.Serious.median()))
st.write("Standart deviation per year: ", int(df_yearly.Serious.std()))
fig = df_yearly.plot(y="Serious", figsize=(15, 7), color="black", ylabel="number of cases",
                     title="Serious crimes per year").figure
plt.axhline(y=int(df_yearly.Serious.mean()), color="crimson", label="mean", linewidth=2, ls="--")
plt.legend()
plt.xticks(range(0, 17), xticks)
st.pyplot(fig)
st.write("The number of serious crimes generally declines from 2003 to 2019. "
         "There is no peak in 2006 like for all crimes but there is a drop in 2004 and "
         "in 2005 the figure bounces back to nearly (*) 2003 value.")
st.write("*: ", int(df_yearly.Serious[0]), int(df_yearly.Serious[2]))


st.write("Secondly, for some particular types of serious crime, such as murder, crime causing serious harm to health "
         "(drievous bodily harm) and rape. To compare the data, let's illustrate it on one graph. "
         "For a fuller picture, I'll also add data on all serious crimes and on all crimes. "
         "For better comparison, I'll use not numbers but percentage (of cases of each type of crime per year"
         " out of all cases of according type from 2003 to 2019).")
st.write("Proportions:")
crimes = int(df_yearly.Total_crimes.sum())
serious = int(df_yearly.Serious.sum())
st.write("What percentage are serious crimes out of all: ", round_percentage(serious, crimes))
murder = int(df_yearly.Murder.sum())
harm_to_health = int(df_yearly.Harm_to_health.sum())
rape = int(df_yearly.Rape.sum())
st.write("Murder, causing harm to health and rape out of serious: ",
         round_percentage(murder, serious), round_percentage(harm_to_health, serious), round_percentage(rape, serious))
st.write("Now, the plot:")

list_to_plot = [year_percentage(df_yearly["Total_crimes"]), year_percentage(df_yearly["Serious"]),
                year_percentage(df_yearly["Murder"]),year_percentage(df_yearly["Harm_to_health"]),
                year_percentage(df_yearly["Rape"])]
df_percent = pd.concat(list_to_plot, axis=1)
st.dataframe(df_percent)
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_percent.plot(ax=ax, y=["Total_crimes", "Serious", "Murder", "Harm_to_health", "Rape"], rot=0,
                color=["gray", "lightpink", "darkred", "black", "crimson"],
                ylabel="percentage of cases per year", title="Serious crimes comparison")
ax.set_xticks(range(0, 17), xticks)
st.pyplot(fig)
st.write("Line graph was for better illustration, bar chart is more convenient for description of trends")
fig, axes = plt.subplots(nrows=2, figsize=(15, 14))
df_percent.plot.bar(ax = axes[0], y = ["Total_crimes", "Serious"], color=["gray", "lightpink"], rot=0,
                    ylabel="percentage of cases per year", title="Serious and all crimes comparison")
df_percent.plot.bar(ax = axes[1], y = ["Total_crimes", "Serious", "Murder", "Harm_to_health", "Rape"], rot=0,
                    color=["darkred", "brown", "indianred", "lightcoral", "pink"],
                    ylabel="percentage of cases per year", title="Serious crimes comparison")
st.pyplot(fig)

st.write("From year 2015 the per year percentage of all crimes stays the highest (from 2010 -- higher than serious "
         "in total). This means that the relative amount of serious crimes (on the whole and for each illustrated "
         "type) has lowered more than crimes have in general. At the same time, less crimes out af all committed from "
         "2003 to 2019 were committed from 2003 to 2007 than serious (out of all serious from 2003 to 2009) were "
         "committed in that period of time: the darkest column is lower than others from 2003 to 2007. So the 2006 "
         "peak in all crimes was created not by serious crimes, except for maybe rape (the only peaking in 2006 here,"
         " but its percentage out of all is too small to cause the peak for all crimes*). So serious crimes have "
         "approximately the same tendency as crimes on the whole from 2007 to 2015. The most drastic decline was in "
         "murder (the middle in color chart): from the highest of all in percentage to the lowest. A slight drop of "
         "serious crimes in 2004 was not a decrease in murder, rape or causing serious harm to health crimes "
         "(there is drop in the column for serious crimes and no drop in murder, rape or causing serious harm to"
         " health crimes).")
st.write("*: ", round_percentage(rape, crimes))


st.write("Let's then compare all crimes and ones not considered major. To obtain such statistics, "
         "I'll substract serious from total (so it will approximately (due to the possible intersection) "
         "be 'non-serious', minor).")
df["Minor"] = df["Total_crimes"] - df["Serious"]
df_yearly["Minor"] = df_yearly["Total_crimes"] - df_yearly["Serious"]
st.dataframe(df_yearly)

st.write("Proportion:")
minor = int(df_yearly.Minor.sum())
st.write(round_percentage(minor, crimes))
st.write("Plots:")
df_percent["Minor"] = year_percentage(df_yearly["Minor"])

fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_percent.plot(ax=ax, y=["Total_crimes", "Minor"], figsize=(15, 7), color=["gray", "lightpink"],
                rot=0, ylabel="percentage of cases per year", title="Minor and all crimes comparison")
ax.set_xticks(range(0, 17), xticks)
st.pyplot(fig)

fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_percent.plot.bar(ax=ax, y=["Total_crimes", "Minor"], figsize=(15, 7), color=["gray", "lightpink"],
                    rot=0, ylabel="percentage of cases per year", title="Minor and all crimes comparison")
st.pyplot(fig)

st.write("Being the major part of crimes in total (73.31%), crimes not considered serious in the dataset follow the "
         "same trend as crimes on the whole, the peak in 2006 included. We can notice that from 2010 bigger "
         "percentages of non-serious crimes out of all non-serious (from 2003 to 2019) are committed per year than "
         "the percentages of crimes in total out of all crimes committed (minor column higher than total). The "
         "opposite is true for 2003-2007. This verifies information from previous plots.")


st.write("Now I'll try to analyse fluctuations depending on the month of the year (seasonal).")
st.write("Here, hypothesis: the amount of rape is higher in colder season than in warmer season each year.")
st.write("Firstly, let's look at statistics for each month:")

df["month"] = pd.to_datetime(df["month"], dayfirst=True)

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15, 7)
ax.plot(df["month"], df["Rape"], color="black")
ax.set_title("Rape over time")
ax.set_ylabel("number of cases")
ax.xaxis.set_major_locator(mdates.YearLocator())
for i in range(0, 205, 12):
    ax.axvline(x=df.month[i], ymin=0, ymax=1, color="crimson", linewidth=0.5, ls="--")
st.pyplot(fig)

st.write("Each yearly fluctuation peaks in the middle of the year, so nearly each year the quantity of the crime is "
         "the lowest closer to the start and to the end and the highest in the middle, so is lower around January and "
         "higher around July. Although the general tendency is such, there are a few exceptions: the highest number "
         "of 2016 is in the beginning of the year; 2016 also has a peak nearer its end; 2019 has a rise at the "
         "beginning (though the figure is still not as high as in the middle); 2019 ends with an increase; in 2005 and "
         "2006 there is a drop (with immediate rise) in the middle of the year.")
st.write("Let's then calculate average statistic for each month:")
st.write("I'll create a column specifically for months, then group the data by month and create a 'seasonal' dataset:")
df["month_only"] = df["month"].apply(lambda item: item.strftime("%b"))
st.dataframe(df)
# Only January in 2020 in the dataset, so in order to have valid data delete it
df_seasonal = df.drop(204, axis=0).drop("month", axis=1).drop("year", axis=1).groupby(["month_only"], sort=False).sum()
# For selected crime, get average from the already obtained sum:
df_for_hypothesis = df_seasonal["Rape"] // (2019-2003+1)
st.dataframe(df_for_hypothesis)
mean = int(df_for_hypothesis.mean())
st.write("Mean: ", mean)

st.write("Let's visualize the data:")
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_for_hypothesis.plot.bar(color="gray", rot=0, xlabel="months", title="Seasonal dependence of rape")
df_for_hypothesis.plot(color="black", linewidth=2, rot=0, xlabel="months", ylabel="average number of cases")
plt.axhline(y=mean, color="crimson", label="mean", linewidth=3, ls="--")
st.pyplot(fig)

st.write("The hypothesis seems to be true: the amount of cases of rape in average for each month of the year increases "
         "from January to July (with an exception of April being slightly lower than March (*)) and decreases "
         "from July to December. The biggest figure is in July and the lowest is in January. Higher than mean are"
         " months from May to October(**).")
st.write("*: ", int(df_for_hypothesis.Apr), int(df_for_hypothesis.Mar))
st.write("** October and mean: ", int(df_for_hypothesis.Oct), mean)

st.write("Pie chart:")
# different color for the highest/the lowest, then colors for 2 around it, then depending on higher/lower than mean.
colors = ["darkred", "brown", "indianred", "indianred", "lightcoral", "pink", "mistyrose", "pink",
          "lightcoral", "lightcoral", "indianred", "brown"]
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_for_hypothesis.plot.pie(colors=colors, title="Seasonal distribution of rape")
ax.set_ylabel("")
st.pyplot(fig)
st.write("So, the closer the month to winter the less rape committed "
         "(small exception: in April slightly less. Then, if we assume that the middle month of the coldest /"
         " the warmest season is the coldest / the warmest, the colder the weather the less rape committed.")
st.write("So, the hypothesis was proved to be generally true, though with exception for some years and for "
         "the difference between March and April.")


st.write("Another hypothesis concerning seasonal fluctuations: the highest number of cases of murder is on the first "
         "of January, so, speaking for months, in January.")
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15, 7)
ax.plot(df["month"], df["Murder"], color="black")
ax.set_title("Murder over time")
ax.set_ylabel("number of cases")
ax.xaxis.set_major_locator(mdates.YearLocator())
for i in range(0, 205, 12):
    ax.axvline(x=df.month[i], ymin=0, ymax=1, color="crimson", linewidth=0.5, ls="--")
st.pyplot(fig)

st.write("Generally the beginning of the year has higher rates than the end. It partially correlates with an overall "
         "downward trend, but after a drop in the middle of the year or closer to its end, the numbers rise again,"
         " so the described tendency cannot be a result of only the general decrease.")
df_for_hypothesis2 = df_seasonal["Murder"] // (2019-2003+1)
st.dataframe(df_for_hypothesis2)
mean2 = int(df_for_hypothesis2.mean())
st.write("Mean: ", mean2)
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
df_for_hypothesis2.plot.bar(color="gray", rot=0, xlabel="months", title="Seasonal dependence of murder")
df_for_hypothesis2.plot(color="black", linewidth=2, rot=0, xlabel="months", ylabel="average number of cases")
plt.axhline(y=mean, color="crimson", label="mean", linewidth=3, ls="--")
st.pyplot(fig)

st.write("The highest are columns for spring months and January. Overall, the second part of the year has lower "
         "number of cases than the first, as the second is lower than the mean and the first is higher. "
         "So there is on average less murder after June. So, as the trend for a year on average corresponds "
         "with the general downward trend of murder from 2003 to 2019, the results cannot clearly imply seasonal "
         "dependency such as higher in the first part of the year and lower in the second. At the same time, I think "
         "that the hypothesis can be considered partially true: the conclusion from the bar chart is that the highest "
         "number of cases of murder of the year happen in January and in spring (the highest is in March).")

st.write("Conclusion:")
st.write("The tendencies in the amount of crimes of various types committed from 2003 to 2019 (January of 2020) "
         "can be divided into two categories: over time and seasonal. Firstly, about the first category. "
         "The overall crime rate was down from from 2003 to 2019 but with a peak in 2006. Not all crimes follow "
         "the same trend, for example, there was a rise in fraud. The amount of cases of serious crimes decreased "
         "more than the amount of crimes on the whole, from being higher to being lower than them. Secondly, I tried "
         "to analyse two types of crimes for seasonal dependency (having set two hypothesis). On average, more rape "
         "was committed in summer than in winter: the closer the month was to January (from July), the more rape was "
         "committed on average during that month. Concerning murder, in my opinion, it is more difficult to say what "
         "is its month dependent tendency and what follows from its overall drop. However, statistically more murder "
         "was on average committed in spring and January.")


