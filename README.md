Abstract
We want to predict the difficulty grade (V0 - V17) of climbs when given only a representation of the route. These routes will be sourced from a number of climbing boards, these boards are fixed width and height walls that have identical holds.

Users are able to create routes by selecting certain holds from the board. Green holds represent starting holds, which climbers must start with their hands on. Orange holds are footholds only. Blue holds are the intermediate positions, available to both hand and foot. Pink holds are the ending holds, where climbers must have two hands on to finish the climb. Our goal is to “grade” or classify given training board routes on their difficulty (V0 - V17) given the data above.

Data
Each route is represented by a string. For example, p1083r15p1117r15p1164r12p1185r12p1233r13p1282r13p1303r13p1372r13p1392r14p1505r15 represents the climb above. This string can be divided into each hold starting with p.

(p1083r15, p1117r15, p1164r12, p1185r12, p1233r13, p1282r13, p1303r13, p1372r13, p1392r14, p1505r15)

where:
r12 — 2 (green)
r13 — 4 (blue)
r14 — 1 (purple)
r15 — 3 (yellow)

The p{4 digit number} represents a hold ID which corresponds to the holds x and y coordinates, and the r{2 digit number} represents a color (green for start, blue for hand, etc.). The string-based route can be represented as a sparse matrix.

Given the string-based route, we plan to use a similar approach as Recurrent Neural Network for MoonBoard Climbing Route Classification and Generation and preprocess our data to capture the nuances of climbing difficulty. This would proposedly involve calculating a difficulty feature vector for each climb based on a number of factors, including the difficulty of the route’s path, the difficulty of the route’s holds, foot placement along the climb, wall angle, distance between holds, and more. 

Challenges
How can we effectively translate our route and difficulty feature vector into spikes?

