# Some imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import math
import streamlit as st
import random

st.header('Natural Selection Simulator')
st.write('Read a technical explanation here: https://docs.google.com/document/d/1QvGz8YKz-xLVddxuC2ExDUw0CIDVOkTzRr3YkFb91yg/edit?usp=sharing')
# Defining the starting points
number_of_aa = st.slider("How many aa (light-color) moths do you want to start with?",5,40,10)
number_of_Aa = st.slider("How many Aa (dark-color with ability to pass on light colored genes) moths do you want to start with?",5,100,20)
number_of_AA = st.slider("How many AA (dark-color) moths do you want to start with?",50,300,100)
survival_rate_dark = st.slider("Pick a survival rate following predation for the Aa and AA moths (percent)",0,90,50)/100
survival_rate_light = st.slider("Pick a survival rate follwing predation for the aa moths (percent)",0,90,80)/100
options = ["Deterministic expectations", "Stochastic mating"]
choice = st.radio("Select one option for mating method. Deterministic expectations just means it goes off of pure, pre-computed probabilities, whereas stochastic mating (MUCH slower) takes a sample of the males and females, shuffles them, mates them, and then scales to generalize to the full population. Stochastic is more random and detrministic is smoother.", options)
list_of_counts = []
final_list = []
aa_list = []
Aa_list = []
AA_list = []

# Making a reproduction function
def reproduce(a,b,c):
    # every mother has 4 children
    m = 0
    n = 0
    l = 0
    
    # a block
    m += 4 * a * (a/(a+b+c)) * 1/2
    m += 2 * a * (b/(a+b+c)) * 1/2
    n += 2 * a * (b/(a+b+c)) * 1/2
    n += 4 * a * (c/(a+b+c)) * 1/2

    # b block
    m += 2 * b * (a/(a+b+c)) * 1/2
    n += 2 * b * (a/(a+b+c)) * 1/2
    m += 1 * b * (b/(a+b+c)) * 1/2
    n += 2 * b * (b/(a+b+c)) * 1/2
    l += 1 * b * (b/(a+b+c)) * 1/2
    l += 2 * b * (c/(a+b+c)) * 1/2
    n += 2 * b * (c/(a+b+c)) * 1/2

    # c block
    n += 4 * c * (a/(a+b+c)) * 1/2
    l += 2 * c * (b/(a+b+c)) * 1/2
    m += 2 * c * (b/(a+b+c)) * 1/2
    l += 4 * c * (c/(a+b+c)) * 1/2

    list_of_counts.append([math.floor(m),math.floor(n),math.floor(l)])
    
    
    return a + math.floor(m), b + math.floor(n), c + math.floor(l)
    
def a_reproduce(a,b,c):
    # every mother has 4 children
    m = 0
    n = 0
    l = 0

    if math.log10(a/2) > 4:
        x = math.ceil(math.log10(a/2))
        ml = [1]*math.floor(a/(2*(10**(x-4)))) + [2]*math.floor(b/(2*(10**(x-4)))) + [3]*math.floor(c/(2*(10**(x-4))))
    else:
        ml = [1]*math.floor(a/2) + [2]*math.floor(b/2) + [3]*math.floor(c/2)
    fl = ml.copy()
    random.shuffle(ml)
    random.shuffle(fl)
    zipped = list(zip(ml, fl))

    count12 = sum(1 for x in zipped if x in [(1,2), (2,1)])
    count13 = sum(1 for x in zipped if x in [(1,3), (3,1)])
    count23 = sum(1 for x in zipped if x in [(2,3), (3,2)])
    count11 = sum(1 for x in zipped if x in [(1,1)])
    count22 = sum(1 for x in zipped if x in [(2,2)])
    count33 = sum(1 for x in zipped if x in [(3,3)])


    if math.log10(a/2) > 4:
        m = (2*count12 + 4*count11 + 1*count22) * (10**(x-4))
        n = (2*count12 + 2*count23 + 4*count13 + 2*count22) * (10**(x-4))
        l = (2*count23 + 1*count22 + 4*count33) * (10**(x-4))
    else:
        m = (2*count12 + 4*count11 + 1*count22)
        n = (2*count12 + 2*count23 + 4*count13 + 2*count22)
        l = (2*count23 + 1*count22 + 4*count33)
    
    list_of_counts.append([math.floor(m),math.floor(n),math.floor(l)])
    
    return a + math.floor(m), b + math.floor(n), c + math.floor(l)
    
# Killing off things that die of old age
def death_by_natural_causes(a,b,c,list_of_counts,index):
    return a - list_of_counts[index-4][0], b - list_of_counts[index-4][1], c - list_of_counts[index-4][2]


# Killing off things that die by predation
def death_by_predation(a,b,c):
    # Ensuring we don't double-kill by scaling each generation appropriately, which are 
    # then the values we give to the old age function
    for i in list_of_counts:
        i[0] = math.floor(i[0]*survival_rate_light)
        i[1] = math.floor(i[1]*(survival_rate_dark))
        i[2] = math.floor(i[2]*(survival_rate_dark))
    return math.floor(a*survival_rate_light), math.floor(b*survival_rate_dark), math.floor(c*survival_rate_dark)


if st.button('Generate animation'):
    for i in range(150):
        if choice == 'Deterministic expectations':
            number_of_aa, number_of_Aa, number_of_AA = reproduce(number_of_aa, number_of_Aa, number_of_AA)
        else:
            number_of_aa, number_of_Aa, number_of_AA = a_reproduce(number_of_aa, number_of_Aa, number_of_AA)
    
        number_of_aa, number_of_Aa, number_of_AA = death_by_predation(number_of_aa,number_of_Aa,number_of_AA)
    
        if i > 3:
            number_of_aa, number_of_Aa, number_of_AA = death_by_natural_causes(number_of_aa, number_of_Aa, number_of_AA, list_of_counts,i)
    
        # No negative populations!!
        if number_of_AA < 0:
            number_of_AA = 0
        if number_of_Aa < 0:
            number_of_Aa = 0
        if number_of_aa < 0:
            number_of_aa = 0
    
        # making the data for the animated chart
        final_list.append([number_of_aa,number_of_Aa,number_of_AA])
        aa_list.append(number_of_aa)
        Aa_list.append(number_of_Aa)
        AA_list.append(number_of_AA)
    with st.expander("Your graph is being generated. This may take up to 20 seconds. Please be patient! In the mean time, here's a non-technical overview of the algorithm used in this model."):
        st.write(""" This model loops over reproduction, predation, and death by old age 150 times, saving population counts at the end of each cycle to create the animation and graphs you are about to see. Reproduction follows Mendelian riles (i.e. Punett squares) and assumed each mother has 4 children, while death by predation is user-determined and death by old age occurs after 4 cycles. """)
    st.subheader("Animation")

    years_per_frame = 1     # change this if 1 frame != 1 year
    start_year = 0
    
    fig, ax = plt.subplots()
    x = np.array([1, 2, 3])
    artists = []
    fps = 7
    
    for i, frame in enumerate(final_list):
        data = np.array(frame, dtype=float)
        data = np.log1p(data)
    
        bars = ax.barh(x, data, color=['tab:blue', 'tab:red', 'tab:green'])
        tick_labels = ['aa', 'Aa', 'AA']
        ax.set_yticks(x)     
        ax.set_yticklabels(tick_labels)
    
        # compute and draw the year label for this frame
        year = start_year + i * years_per_frame
        txt = ax.text(
            0.98, 0.95, f"Year {year:,}",
            transform=ax.transAxes, ha='right', va='top',
            fontsize=12,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7),
            animated=True  # important when using blit=True
        )
    
        # include text in this frame's artist list
        artists.append(list(bars) + [txt])

        ax.set_xlabel('Natural log of population')

    ani = animation.ArtistAnimation(fig, artists, interval=int(1000/fps), blit=True, repeat=False)
    
    # Save to GIF using Pillow
    gif_path = "pop_anim.gif"
    ani.save(gif_path, writer="pillow", fps=fps)
    st.image(gif_path)

    
    # X-axis is just the index (time steps)
    x = range(len(aa_list))
    
    # Create a new figure
    fig, ax = plt.subplots(3, 1, figsize=(8, 24))

    # Blue (aa)
    ax[0].plot(x, aa_list, marker='o', linestyle='-',color='blue')

    
    # Add labels and title
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Value")
    ax[0].set_title("Change Over Time for Moths with aa Alleles")

    # Red (Aa)
    ax[1].plot(x, Aa_list, marker='o', linestyle='-',color='red')

    
    # Add labels and title
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Value")
    ax[1].set_title("Change Over Time for Moths with Aa Alleles")

    # Gree (AA)
    ax[2].plot(x, AA_list, marker='o', linestyle='-',color='green')

    
    # Add labels and title
    ax[2].set_xlabel("Time")
    ax[2].set_ylabel("Value")
    ax[2].set_title("Change Over Time for Moths with AA Alleles")
    
    # Render in Streamlit
    st.pyplot(fig)
