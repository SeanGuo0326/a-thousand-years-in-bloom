# Process

This project developed through several visual and technical iterations. I used AI as a coding and development assistant, but I tested the results myself and made decisions about the visual direction, data communication, animation and performance.

## Tools

I used Python, Matplotlib and NumPy to create the visualisation and animation. I used `requests` in `fetch.py` to download the original CSV file and saved the raw data locally before visualising it.

I also used ChatGPT during development. It helped me understand the CSV structure, write and revise Python code, debug errors, and explore different ways of representing the data. A substantial part of the plotting and animation code was developed with AI assistance. I tested each version, compared the results visually, and decided what to keep, change or reject.

The project went through several stages:

1. **Initial data plot**  
   I first parsed the Kyoto cherry blossom dataset and checked that the year and flowering-day values could be read correctly. The first visualisation was closer to a conventional scatter plot.

2. **Flower representation**  
   I experimented with replacing ordinary points with blossom shapes. Several flower designs were tested before I chose a simple five-petal blossom. This made the data points visually connected to the phenomenon rather than looking like generic markers.

3. **Timeline animation**  
   I created an animated version in which the historical records appear from 812 to 2015. The first version technically worked, but I realised that a viewer might not understand what each flower represented or why the flowers appeared at different heights.

4. **Improving data communication**  
   I added the explanation “Each blossom = one recorded year of full bloom”, an EARLIER/LATER guide for the full-bloom date, historical year markers and a changing year display. I also changed the flowers so that they gradually bloom instead of suddenly appearing.

5. **Falling transition and loop**  
   After the complete dataset appears, the blossoms fall away before the history begins again. This falling movement is decorative and does not represent another data variable. I added it to give the animation an ending and make the loop feel connected to the seasonal subject.

6. **Performance optimisation**  
   During testing, I noticed that the animation became increasingly slow as more records appeared. The earlier version recreated thousands of individual Matplotlib patches every frame because every blossom used five petals and a centre. I changed the rendering method so that the blossoms use a reusable scatter collection instead. This made the timeline much smoother while preserving the same data mapping and visual concept.

   After this optimisation, I noticed another small problem: the blossoms moved sideways slightly before beginning to fall. I traced this to the starting value of the sway calculation and changed it so that the falling movement begins from the blossom's original position. This removed the visible jump between the full-bloom and falling phases.

## Kept

One AI suggestion I kept was using a five-petal blossom instead of a normal scatter point. I kept this because the shape communicates the subject immediately while still allowing every flower to function as an individual data mark.

I also kept the idea of animating the records chronologically. A static image shows the overall distribution, but the animation makes the historical duration more noticeable because the viewer watches the records accumulate from 812 to 2015.

Another suggestion I kept was optimising the animation with a reusable scatter collection. The earlier animation became noticeably slower as more flowers appeared. The optimised version was much smoother and produced almost the same visual result.

## Rejected

I rejected an earlier visual direction that placed the blossoms around a branching tree structure. The branches looked too mechanical and started to resemble a fish skeleton. More importantly, the tree structure made the relationship between year and flowering date less direct. I returned to a clearer timeline layout where year controls horizontal position and full-bloom date controls vertical position.

I also rejected the idea of keeping decorative blossoms visible before their historical year appeared. Although they made the composition look fuller, they confused the meaning of the animation because viewers could not tell which flowers represented real data. In the final version, the animated blossoms are tied to actual records.

During the process I also avoided adding interaction only for decoration. I considered interactive controls, but decided that the timeline, bloom and falling sequence already communicated the main idea clearly. Adding interaction without a meaningful relationship to the data would have made the project more complicated without improving the explanation of the phenomenon.