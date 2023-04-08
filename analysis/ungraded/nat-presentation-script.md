Hey there, my name is Nat, and together with Sami, we have spent the last semester studying queer geography using the gaybourhoods dataset from media agency The Pudding, which attempts to measure queerness by neighbourhood in 15 cities across the United States. I'll take a few minutes to discuss the research questions I sought to answer before handing it off to Sami.

In the first, we asked if there's a correlation between geographical stratums & being LGBT. In the second, we wanted to know if there was a correlation between political alignment and living in a neighbourhood with a large LGBT population.

Before we could fully tackle these two questions we needed to establish some additional metrics that would make the data more approchable. The fact that our data is continuous complicated numerical studies, so we decided to discretize the observations by dividing the range into 7 chunks, which we call the observation's Kinsey index.

For our first research question, we were interested not only in a given neighbourhood's kinsey index, but also the kinsey index of any adjacent neighbourhoods. This can be well-represented visually, but we also wanted to find a way to represent it numerically. To do this, we designed an algorithm that calculates an approximate average kinsey index of a small set of observations about the original, which we call the nighbourhood kinsey index.

Down in the left corner here, we have a bar graph comparing the average neighbourhood kinsey index per kinsey index, where a higher kinsey index represents a neighbourhood with a larger number of gay and lesbian residents. The trend here indicates that relationship between the two variables is proportional.

Similarly, to the right, we have a scatterplot illustrating the neighbourhood kinsey index versus the same-sex index, representing the density of gay and lesbian residents. It's clear that while the trend is still present, there's a lot of variance in the data.

Altogether, we have strong numerical evidence that queer communities tend to concentrate in space.

The third graph we have along the bottom tackles our second research question, quantitatively showing the relationship between a neighbourhood's kinsey index and the percentage of the population who voted democrat in the 2012 American presidential election. We see that on average, neighbourhoods that have a high kinsey index tend to vote more democrat.

These two phenomena can also be visualized spatially. This is where Tableau shines for the issues we're tackling with this project. For the dashboard, we chose to take a more interactive approach. Both maps illustrate a density map of all observations; the one on the left is filtered by minimum kinsey index and the one on the right is filtered by the minimum percent of the population who voted democrat.

Here, the filters serve as the third dimention of the data. To compare the peaks of queer and democrat population density, we can adjust the filters on the respective graphs.
