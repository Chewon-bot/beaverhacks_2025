#Importing basic packages:
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from csv import DictWriter
from csv import DictReader


#import given dataset as :
kbeauty_100_korea = pd.read_csv('products.csv')
kbeauty_100_usa = pd.read_csv('soko_glam.csv')
kbeauty_100_korea = kbeauty_100_korea.drop(columns=['name_kor'])
kbeauty_100_usa = kbeauty_100_usa.drop(columns=['photo'])
kbeauty_100_korea.columns = [col + '_k' for col in kbeauty_100_korea.columns]
kbeauty_100_usa.columns = [col + '_u' for col in kbeauty_100_usa.columns]
kbeauty_total = pd.concat([kbeauty_100_korea, kbeauty_100_usa], axis=1)

def brand_overlap(row):
    a = str(row['brand_k']).lower()
    b = str(row['brand_u']).lower()
    return a in b or b in a
kbeauty_total = kbeauty_total[kbeauty_total.apply(brand_overlap, axis=1)]
kbeauty_total = kbeauty_total.reset_index(drop=True)
price_remove = ['US', '$', '₩', ',']

for col in kbeauty_total.columns:
    if kbeauty_total[col].dtype == 'object':
        for symbol in price_remove:
            kbeauty_total[col] = kbeauty_total[col].str.replace(symbol, '', regex=False)
        kbeauty_total[col] = kbeauty_total[col].str.strip()

kbeauty_total['discounted_price_k'] = pd.to_numeric(kbeauty_total['discounted_price_k'], errors='coerce')
kbeauty_total['full_price_u'] = pd.to_numeric(kbeauty_total['full_price_u'], errors='coerce')
# kbeauty_total = kbeauty_total[kbeauty_total['brand_k'].str. lower() == kbeauty_total['brand_u'].str.lower()]
kbeauty_total_full = kbeauty_total.dropna().reset_index(drop=True)
kbeauty_total_full = kbeauty_total_full.reset_index(drop=True)

#How many top 100 K-Beauty items were available in the website of the United States?
print(len(kbeauty_total_full))

#Boxplot
sns.set(style="whitegrid")
custom_palette = {'Korea': '#66c2a5', 'USA': '#fc8d62'}

for_boxplot = kbeauty_total_full[['discounted_price_k', 'full_price_u']].copy()
for_boxplot.columns = ['Korea', 'USA']
plot_melted = for_boxplot.melt(var_name='Country', value_name='Price')

plt.figure(figsize=(8, 6))
sns.boxplot(x='Country', y='Price', data=plot_melted, palette=custom_palette)
plt.title("Price comparison between Korea and U.S. websites of Top 100 K-beauty Products")
plt.xlabel("Country")
plt.ylabel("Price (USD)")
plt.show()


#Scatterplot

plot_long = kbeauty_total_full[['discounted_price_k', 'full_price_u']].copy()
plot_long = plot_long.rename(columns={'discounted_price_k': 'Korea', 'full_price_u': 'USA'})
plot_long = plot_long.melt(var_name='Country', value_name='Price')

plot_long['x'] = 'All Prices'

plt.figure(figsize=(8, 6))
sns.stripplot(x='x', y='Price', hue='Country', data=plot_long,
              palette='Set2', alpha=0.6, jitter=0.25)

plt.title("Price comparison between Korea and U.S. websites of Top 100 K-beauty Products")
plt.xlabel("")
plt.ylabel("Price (USD)")
plt.legend(title='Country')
plt.grid(True)
plt.show()

# Line Plot
plot_df = kbeauty_total_full[['discounted_price_k', 'full_price_u']].copy()
plot_df = plot_df.dropna().reset_index(drop=True)

plt.figure(figsize=(12, 6))
plt.plot(plot_df.index, plot_df['discounted_price_k'], label='Korea', marker='o', color='skyblue')
plt.plot(plot_df.index, plot_df['full_price_u'], label='U.S.', marker='o', color='salmon')

plt.title("1:1 Price Comparison of Korean vs U.S. Sites for K-beauty Products")
plt.xlabel("Ranking (High to Low)")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# print(kbeauty_total_full.columns)

# Wordcloud: Trend of Top 100 K-Beauty Products in Korea
product_word_k = kbeauty_total_full['name_k']

text_k = ' '.join(product_word_k.dropna().astype(str))

wordcloud_k = WordCloud(background_color='white',
                      width=800,
                      height=400).generate(text_k)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud_k, interpolation='bilinear')
plt.axis('off')
plt.text(0.5, -0.08, "Wordcloud: Trend of Top 100 K-Beauty Products in Korea",
         fontsize=16, ha='center', va='top', fontname='Calibri', transform=plt.gca().transAxes)
plt.show()

# Wordcloud: Wordcloud: Trend of Top 100 K-Beauty Products in U.S.
product_word_u = kbeauty_total_full['name_u']

text_u = ' '.join(product_word_u.dropna().astype(str))

wordcloud_u = WordCloud(background_color='white',
                      width=800,
                      height=400).generate(text_u)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud_u, interpolation='bilinear')
plt.axis('off')
plt.text(0.5, -0.08, f"Wordcloud: Trend of Top 100 K-Beauty Products in U.S. (only {len(kbeauty_total_full)} items available)",
         fontsize=16, ha='center', va='top', fontname='Calibri', transform=plt.gca().transAxes)
plt.show()
