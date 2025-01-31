# Bank Transaction Shortest Path Finder

Overview

This project is a graphical simulation of a bank transaction network that finds the shortest transaction path between two banks using Dijkstra's Algorithm. The application is built with Pygame and provides an interactive way to select source and destination banks to visualize the shortest path.

Features

Dynamic Window Resizing: The layout adjusts when the window size changes.

Graphical Representation: Nodes represent banks, and edges indicate transaction costs.

Dijkstra's Algorithm: Calculates the shortest transaction path between banks.

Interactive Selection: Click on banks to set the source and destination.

Reset Functionality: Reset the selection to try different paths.

Technologies Used

Python

Pygame

Dijkstra's Algorithm

Installation

Prerequisites

Ensure you have Python installed on your system. You can check by running:

python --version

Install Pygame if you haven't already:

pip install pygame

Running the Application

Clone this repository:

git clone https://github.com/your-username/bank-transaction-shortest-path.git

Navigate to the project directory:

cd bank-transaction-shortest-path

Run the script:

python main.py

You can also specify a custom window size:

python main.py 1200 800

How to Use

Run the application.

Click on a bank node to select it as the source.

Click on another bank node to set it as the destination.

The shortest transaction path will be highlighted along with the total cost.

Click the Reset button to start over.

Graph Representation

Nodes represent banks.

Edges represent transaction paths with associated costs.

The shortest path is highlighted in green.

Example Graph

Banks: ICICI, SBI, HDFC, Axis, Kotak Mahindra, Bank of Baroda, Yes Bank, Federal Bank

Sample Transaction Costs:

ICICI → HDFC: Rs. 200

HDFC → Axis: Rs. 150

Axis → Yes Bank: Rs. 150

Screenshots

(Include some images of the application running)

Future Enhancements

Add more banks and transaction paths.

Implement real-world transaction data integration.

Enhance UI/UX with animations.

License

This project is licensed under the MIT License.
